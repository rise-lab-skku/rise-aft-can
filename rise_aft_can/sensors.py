from abc import ABCMeta, abstractmethod
import time
from canlib import canlib, Frame
from rise_aft_can import utils


class AFTSensor(metaclass=ABCMeta):
    def __init__(
        self, channel: int = None, can_id: int = None, bitrate: canlib.Bitrate = None
    ):
        self.channel = channel
        self.bitrate = bitrate
        self.can_id = can_id
        self.ch = None
        # Last received data
        self.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    def __enter__(self):
        """Enter with statement."""
        self.setup_channel()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit with statement."""
        self.teardown_channel()

    def setup_channel(self):
        # Check configured
        if self.bitrate is None:
            raise ValueError("bitrate is not configured.")
        # Setup channel
        self.ch = utils.setup_channel(self.channel, self.bitrate)

    def teardown_channel(self):
        utils.teardown_channel(self.ch)

    @abstractmethod
    def read(self) -> list:
        """Return [Fx, Fy, Fz, Tx, Ty, Tz]"""
        pass


class AFT200D80(AFTSensor):
    def __init__(self, channel: int = 0, can_id: int = 1):
        super().__init__(
            channel=channel, can_id=can_id, bitrate=canlib.Bitrate.BITRATE_1M
        )

    def read(self, timeout=1000) -> list:
        """Read Fx, Fy, Fz, Tx, Ty, Tz. (timeout: ms)"""
        # Received frame ID will be 1 or 2 (1 -> 2 -> 1 -> 2 -> ...)
        # But we don't know which frame will be received first.
        # The first frame is always ID 1.
        # However, we can create AFT200D80 object while the sensor is already transmitting.
        first_id = self._handle_received_frame(timeout=timeout)
        second_id = self._handle_received_frame(timeout=timeout)
        if first_id == second_id:
            raise RuntimeWarning(
                f"Some frames are lost. First ID: {first_id}, Second ID: {second_id}"
            )
        return self.data

    def _handle_received_frame(self, timeout=1000) -> int:
        """Handle the received frame. Return the frame ID handled."""
        # Read a bytearray
        frame = self.ch.read(timeout=timeout)
        # Convert data to force and torque
        # Data format:
        #     [ID, d[0], d[1], d[2], d[3], d[4], d[5], xx, xx]
        # ID: 1 (Force [N] = output/100 - 300)
        # ID: 2 (Torque [Nm] = output/500 - 50)])
        Vx = frame.data[0] * 256 + frame.data[1]
        Vy = frame.data[2] * 256 + frame.data[3]
        Vz = frame.data[4] * 256 + frame.data[5]
        if frame.id == 1:
            # Force
            self.data[0] = Vx / 100 - 300
            self.data[1] = Vy / 100 - 300
            self.data[2] = Vz / 100 - 300
        elif frame.id == 2:
            # Torque
            self.data[3] = Vx / 500 - 50
            self.data[4] = Vy / 500 - 50
            self.data[5] = Vz / 500 - 50
        else:
            raise ValueError(f"Received frame ID is not 1 or 2: {frame.id}")
        return frame.id

    def can_write(self, data_field: list):
        self.ch.write(
            Frame(
                id_=0x102,
                data=data_field,
                flags=canlib.MessageFlag.STD,
            )
        )

    def set_can_id(self, new_id: int):
        print(f"Change CAN ID from {self.can_id} to {new_id}")
        self.can_write([self.can_id, 0x01, new_id, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.can_id = new_id
        print(f"CAN ID is changed to {self.can_id}.")

    def set_bias_setting(self, sleep=1.0):
        self.can_write([self.can_id, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])
        # Sleep more than 1 sec to wait for the bias setting to be completed.
        # If you don't sleep, `canlib.CanNoMsg` will be raised continuously.
        sleep = 1.0 if sleep < 1.0 else sleep
        print(f"Sleep {sleep} sec to wait for the bias setting to be completed.")
        time.sleep(sleep)
        print("Bias setting is completed.")

    def set_bias_clear(self):
        self.can_write([self.can_id, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00])
        print("Bias is cleared.")

    def set_continuous_transmitting(self):
        self.can_write([self.can_id, 0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00])
        print("Continuous transmitting is set.")

    def set_sampling_rate(self, hz: int = 1000):
        rate_param: int = 1_000_000 // hz
        applied_hz: int = 1_000_000 // rate_param
        print(f"Request: {hz} Hz, Applied: {applied_hz} Hz")
        field_2 = rate_param // 256
        field_3 = rate_param % 256
        self.can_write([self.can_id, 0x05, field_2, field_3, 0x00, 0x00, 0x00, 0x00])

    def reset_can_id_of_all_sensors(self):
        answer = ""
        while answer not in ["y", "n"]:
            print("Reset CAN ID of all connected sensors. Are you sure? (y/n)")
            answer = input()
        if answer == "y":
            self.can_write([0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            print("CAN ID of all connected sensors is reset.")
        else:
            print("Canceled.")

    def set_info_transmitting(self):
        # ID, SN, release confirming mode
        raise NotImplementedError


# ====================================================
# import shutil
# import time

# width, height = shutil.get_terminal_size((80, 20))

# def printframe(frame):
#     global width
#     form = '═^' + str(width - 1)
#     print(format(" Frame received ", form))
#     print(frame)
#     print(f"  id: {frame.id}")
#     print(f"  data: {bytes(frame.data)}")
#     print(f"  dlc: {frame.dlc}")
#     print(f"  flags: {frame.flags}")
#     print(f"  timestamp: {frame.timestamp}")