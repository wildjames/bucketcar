import asyncio

import aiortc
from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.signaling import (BYE, add_signaling_arguments,
                                      create_signaling)


async def consume_signaling(pc, signaling):
    '''Waits for an object to be recieved, and either parses it 
    or quits, if the session is over.'''
    while True:
        obj = await signaling.receive()

        # Session descriptions get bounced back at their origins
        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj) # Set my sending target to the signal origin

            if obj.type == "offer":
                # send answer
                await pc.setLocalDescription(await pc.createAnswer())
                await signaling.send(pc.localDescription)

        elif isinstance(obj, RTCIceCandidate):
            pc.addIceCandidate(obj)

        elif obj is BYE:
            print("Exiting")
            break



async def run_answer(pc, signaling):
    '''Sets up a data channel, and waits for someone to connect to it.
    When a message is recieved, print it and reply with "pong"
    '''
    print("Setting up answerer")

    await signaling.connect()

    @pc.on("datachannel")
    def on_datachannel(channel):
        print("{} created by remote party".format(channel))

        @channel.on("message")
        def on_message(message):
            print("{} < {}".format(channel, message))

            if isinstance(message, str) and message.startswith("ping"):
                # reply
                msg = "pong" + message[4:]
                print("{} > {}".format(channel, msg))
                channel.send(msg)

    await consume_signaling(pc, signaling)



async def run_offer(pc, signaling):
    '''sends a ping'''
    print("Setting up offerer")
    await signaling.connect()

    channel = pc.createDataChannel("chat")
    print("{} - {}".format(channel, "created by local party"))

    async def send_pings():
        while True:
            msg = "ping"
            channel.send(msg)
            await asyncio.sleep(1)

    @channel.on("open")
    def on_open():
        asyncio.ensure_future(send_pings())

    @channel.on("message")
    def on_message(message):
        print("{} < {}".format(channel, message))

        if isinstance(message, str) and message.startswith("pong"):
            print("Ponged their Ping\n")
        else:
            print("Got a non-str message:")
            print(message)
            print("\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")

    # send offer
    await pc.setLocalDescription(await pc.createOffer())
    await signaling.send(pc.localDescription)

    # Wait for an object to be recieved. 
    await consume_signaling(pc, signaling)



