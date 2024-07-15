from canlib import canlib, Frame
import shutil


def prettify(ft_data: list) -> str:
    """ft_data: [Fx, Fy, Fz, Tx, Ty, Tz]"""
    ft_string = [f"{f:.3f}" for f in ft_data]
    f = f"Fx[N]: {ft_string[0]:>9}  | Fy[N]: {ft_string[1]:>9}  | Fz[N]: {ft_string[2]:>9}"
    t = f"Tx[Nm]: {ft_string[3]:>9}  | Ty[Nm]: {ft_string[4]:>9}  | Tz[Nm]: {ft_string[5]:>9}"
    return f"{f}  | {t}"


def print_pretty_raw_frame(frame: Frame) -> str:
    width, height = shutil.get_terminal_size((80, 20))
    form = '═^' + str(width - 1)
    print(format(" Frame received ", form))
    print(f"  id: {frame.id}")
    print(f"  data: {bytes(frame.data).hex(' ')}")
    print(f"  dlc: {frame.dlc}")
    print(f"  flags: {frame.flags}")
    print(f"  timestamp: {frame.timestamp}")


def setup_channel(channel_number: int, bitrate: canlib.Bitrate) -> canlib.Channel:
    channel_data = canlib.ChannelData(channel_number)
    channel_name = channel_data.channel_name
    card_upc_no = channel_data.card_upc_no
    card_serial_no = channel_data.card_serial_no
    print(f"Using channel: {channel_name}, EAN: {card_upc_no}, Serial: {card_serial_no}")

    open_flags = canlib.canOPEN_ACCEPT_VIRTUAL
    try:
        ch = canlib.openChannel(channel_number, open_flags)
        ch.setBusOutputControl(canlib.canDRIVER_NORMAL)
        ch.setBusParams(bitrate)
        ch.busOn()
    except canlib.canError as e:
        print(f"Failed to open channel: {e}")
        raise
    return ch


def teardown_channel(ch: canlib.Channel):
    print(f"Closing channel: {ch.channel_data.channel_name}")
    try:
        ch.busOff()
        ch.close()
    except canlib.canError as e:
        print(f"Failed to close channel: {e}")
        raise
    print("Channel closed.")
