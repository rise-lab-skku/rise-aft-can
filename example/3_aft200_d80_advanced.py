import time
from canlib import canlib
from rise_aft_can.sensors import AFT200D80
from rise_aft_can.utils import prettify

channel = 0

# Timeout for CAN read (sec)
timeout = 0.5

# Message tick time when no message received (sec)
ticktime = 1.0
tick_countup = 0.0


with AFT200D80(channel) as aft:
    aft.set_bias_setting()
    aft.wait_for_bias_info(timeout=1.0)

    aft.set_continuous_transmitting()

    print("\nListening...")
    while True:
        try:
            data: list = aft.read(timeout=int(timeout * 1000))
            print(f"[{time.time():.3f}] {prettify(data)}")

        except canlib.CanNoMsg:
            tick_countup += timeout
            while tick_countup > ticktime:
                print(f"[{time.time():.3f}] no message")
                tick_countup -= ticktime

        except KeyboardInterrupt:
            print("Stop.")
            break

    # aft.set_bias_clear()
