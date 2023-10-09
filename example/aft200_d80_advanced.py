import time
from canlib import canlib
from rise_aft_can.sensors import AFT200D80


def prettier_print(data: list):
    ft_string = [f"{f:.3f}" for f in data]
    f = f"Fx[N]: {ft_string[0]:>9}  | Fy[N]: {ft_string[1]:>9}  | Fz[N]: {ft_string[2]:>9}"
    t = f"Tx[Nm]: {ft_string[3]:>9}  | Ty[Nm]: {ft_string[4]:>9}  | Tz[Nm]: {ft_string[5]:>9}"
    print(f"[{time.time():.3f}] {f}  | {t}")


channel = 0

timeout = 0.5  # sec
ticktime = 1.0
tick_countup = 0.0


with AFT200D80(channel) as aft:
    aft.set_bias_setting()
    # Sleep more than 1 sec to wait for the bias setting to be completed.
    # If you don't sleep, `canlib.CanNoMsg` will be raised continuously.
    time.sleep(1)

    aft.set_continuous_transmitting()

    print("\nListening...")
    while True:
        try:
            data: list = aft.read(timeout=int(timeout * 1000))
            prettier_print(data)
        except canlib.CanNoMsg:
            tick_countup += timeout
            while tick_countup > ticktime:
                print(f"[{time.time():.3f}] no message")
                tick_countup -= ticktime
        except KeyboardInterrupt:
            print("Stop.")
            break

    # aft.set_bias_clear()
