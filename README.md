# BucketCar

A car, that will probably end up living in a bucket.


## What's the plan?

I want to, in essence, take one of those plastic storage containers and fill it with big chunky batteries. Then, slap four wheels and a motor on it, a servo for steering, and a raspberry pi (probably 4?) for brains. Then, I want to send the pi directions over the internet. Initially, this is probably gonna be over a local wifi hotspot that the pi and my laptop both connect to, but I want to either use a cheap android or [this]() to give the pi 4G LTE, and see how far I can get this bad boy to go. 

Also, mount a webcam on another stepper and a servo so I can look around with it. Probably gonna need a GPS reciever too, so I know where the car is (self-driving capabilities..?)

Yes, I know that [RTCbot](https://github.com/dkumor/rtcbot) exists. But I want to design this myself, as a project. 

Parts list: [HERE](https://docs.google.com/spreadsheets/d/1hJXBGtgOUzoiMhmMpQXa8KYEWCtUkvLedHiXm8dd3HM/edit#gid=0)

### Progress log / roadmap

  - I need to first learn how to communicate between scripts over the internet. I'm gonna do this in python, since that's what I know. [aiortc](https://github.com/aiortc) looks perfect for what I want to do.
    - Get two scripts communicating over a network [[DONE]](network_comm_testing/sender.py)
    - Have the car stream video and operating data back to the client
    - Have the client send commands to the car
    - Impliment a TURN server (i.e. wildjames.com) that facilitates linking the two
      - For the love of god, don't forget to make this require a PASSWORD! or who knows who'll end up controlling the damn thing.

  - I need to write control software for the motor and servos. 
    - This shouldn't be hard - the motors that hobbyist R/C cars use have a controller board that you just send PWM signals to. 
    - Servos are easy-peasy, but I'll need a fairly beefy one. 25kg is likely overkill, and they're cheap enough, so I'm not worried. 
    - However! If I want this to be long-range, I need to be concerned about power draw!
    - Car class, motor class, servo class. Use the pi's GPIOzero library to drive pins. Easy.

  - Capture input from an xbox controller on the client side
    - I just think it'd be better than having keyboard input
    - The `inputs` module should be perfect for this, but I did some initial testing and can't get wireless controllers to connect to it... They work fine in everything else! Very annoying.
  
  - [Long Term] Bundle the whole thing up into a browser