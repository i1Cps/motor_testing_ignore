import time

from STservo_sdk import PortHandler, sts, COMM_SUCCESS


PORT = "/dev/ttyUSB0"
BAUD = 115200
MIN_POS = 0
MAX_POS = 4095
SPEEDS = [1000, 2500, 4000]
ACC = 80
MOVE_DELAY = 0.5
READ_DELAY = 0.2
IDS = [1, 2, 3, 4, 5]


def main():
    port = PortHandler(PORT)
    packet = sts(port)

    if not port.openPort():
        raise RuntimeError("Failed to open port")
    if not port.setBaudRate(BAUD):
        raise RuntimeError("Failed to set baudrate")

    try:
        for speed in SPEEDS:
            print(f"Testing motors at speed: {speed}")
            for sid in IDS:
                for target in (MIN_POS, MAX_POS, MIN_POS):
                    print(f"motor ID {sid}: move to {target}")
                    result, err = packet.WritePosEx(sid, target, speed, ACC)
                    if result != COMM_SUCCESS:
                        print(f"ID {sid}: {packet.getTxRxResult(result)}")
                    if err:
                        print(f"ID {sid}: {packet.getRxPacketError(err)}")
                    time.sleep(READ_DELAY)
                    pos, r_result, r_err = packet.ReadPos(sid)
                    if r_result == COMM_SUCCESS and r_err == 0:
                        print(f"motor ID {sid}: target {target} pos {pos}")
                    else:
                        if r_result != COMM_SUCCESS:
                            print(f"ID {sid}: {packet.getTxRxResult(r_result)}")
                        if r_err:
                            print(f"ID {sid}: {packet.getRxPacketError(r_err)}")
                    time.sleep(MOVE_DELAY)
    except KeyboardInterrupt:
        pass
    finally:
        print("Test finished")
        port.closePort()


if __name__ == "__main__":
    main()
