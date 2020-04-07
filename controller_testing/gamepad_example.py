"""Simple example showing how to get gamepad events."""

from inputs import get_gamepad

def main():
    while 1:
        events = get_gamepad()
        for event in events:
            print(event.ev_type, event.code, event.state)


if __name__ in "__main__":
    main()
