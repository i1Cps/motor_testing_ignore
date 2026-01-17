import argparse
import time

from STservo_sdk import PortHandler, sts, COMM_SUCCESS


BAUD = 1_000_000
MIN_POS = 0
MAX_POS = 4095
SPEED = 1000
ACC = 50
INTERVAL = 1.0


def main():
    parser = argparse.ArgumentParser(description="Periodic rotate demo for STS3215 servo motors ID 1")
    parser.add_argument("--port", required=True, help="Serial port, e.g. /dev/ttyUSB0 or /dev/ttyACM0")
    args = parser.parse_args()

    port = PortHandler(args.port)
    packet = sts(port)

    if not port.openPort():
        raise RuntimeError("Failed to open port")
    if not port.setBaudRate(BAUD):
        raise RuntimeError("Failed to set baudrate")

    positions = [MIN_POS, MAX_POS]
    idx = 0

    try:
        while True:
            target = positions[idx]
            result, err = packet.WritePosEx(1, target, SPEED, ACC)
            if result != COMM_SUCCESS:
                print(packet.getTxRxResult(result))
            if err:
                print(packet.getRxPacketError(err))

            idx = 1 - idx
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        pass
    finally:
        port.closePort()


if __name__ == "__main__":
    main()
