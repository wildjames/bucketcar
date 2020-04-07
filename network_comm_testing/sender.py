import argparse

import asyncio
import aiortc
from aiortc.contrib.signaling import add_signaling_arguments, create_signaling

from example_funcs import consume_signaling, run_offer


# This works with TCP!
if __name__ in "__main__":
    parser = argparse.ArgumentParser("Demo ping/pong script. This is the sender.")
    add_signaling_arguments(parser)

    args = parser.parse_args()

    # Create the RTC connection
    pc = aiortc.RTCPeerConnection()

    # Create the signaler
    signaling = create_signaling(args)

    # Set up the offering functions on the pc
    offerer = run_offer(pc, signaling)

    # Fetch the event loop, so I can handle it
    loop = asyncio.get_event_loop()


    # Start the event loop
    try:
        loop.run_until_complete(offerer)
    except KeyboardInterrupt:
        print("Keyboard interrupt!")
    finally:
        # Perform shutdowns.
        loop.run_until_complete(pc.close())
        loop.run_until_complete(signaling.close())

