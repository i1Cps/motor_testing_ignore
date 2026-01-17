import argparse
import time

from STservo_sdk import PortHandler, sts, COMM_SUCCESS


BAUD = 1_000_000
MIN_POS = 0
MAX_POS = 4095
SPEEDS = [1000, 2500, 4000]
ACC = 80
MOVE_DELAY = 0.5
IDS = [1, 2, 3, 4, 5]


def main():
    parser = argparse.ArgumentParser(description="Test motors")
    parser.add_argument("--port", required=True)
    args = parser.parse_args()

    port = PortHandler(args.port)
    packet = sts(port)

    if not port.openPort():
        raise RuntimeError("Failed to open port")
    if not port.setBaudRate(BAUD):
        raise RuntimeError("Failed to set baudrate")

    try:
        for speed in SPEEDS:
            for sid in IDS:
                for target in (MIN_POS, MAX_POS, MIN_POS):
                    result, err = packet.WritePosEx(sid, target, speed, ACC)
                    if result != COMM_SUCCESS:
                        print(f"ID {sid}: {packet.getTxRxResult(result)}")
                    if err:
                        print(f"ID {sid}: {packet.getRxPacketError(err)}")
                    time.sleep(MOVE_DELAY)
    except KeyboardInterrupt:
        pass
    finally:
        port.closePort()


if __name__ == "__main__":
    main()
