"""monitor.py -- Print all data received on a CAN channel

This script uses canlib.canlib to listen on a channel and print all data
received.

It requires a CANlib channel with a connected device capable of receiving CAN
messages and some source of CAN messages.

The source of the messages may be e.g. the pinger.py example script.

Also see the dbmonitor.py example script for how to look up the messages
received in a database.

"""
import shutil
import time
from canlib import canlib, Frame


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


def printframe(frame, width):
    """
    Receive data format:
        [ID, d[0], d[1], d[2], d[3], d[4], d[5], xx, xx]

    ID: 1 (Force [N] = output/100 - 300)
        output_x = d[0] * 256 + d[1]
        output_y = d[2] * 256 + d[3]
        output_z = d[4] * 256 + d[5]

    ID: 2 (Torque [Nm] = output/500 - 50)])
        output_x = d[0] * 256 + d[1]
        output_y = d[2] * 256 + d[3]
        output_z = d[4] * 256 + d[5]
    """
    form = '═^' + str(width - 1)
    print(format(" Frame received ", form))
    print(frame)
    print(f"  id: {frame.id}")
    print(f"  data: {bytes(frame.data)}")
    print(f"  dlc: {frame.dlc}")
    print(f"  flags: {frame.flags}")
    print(f"  timestamp: {frame.timestamp}")
    # Convert data to force and torque
    if frame.id == 1:
        # Force
        Fx = frame.data[0] * 256 + frame.data[1]
        Fy = frame.data[2] * 256 + frame.data[3]
        Fz = frame.data[4] * 256 + frame.data[5]
        Fx = Fx / 100 - 300
        Fy = Fy / 100 - 300
        Fz = Fz / 100 - 300
        Fstr = ['{:.3f}'.format(Fx), '{:.3f}'.format(Fy), '{:.3f}'.format(Fz)]
        print(f"  Fx: {Fstr[0]:>9} N   Fy: {Fstr[1]:>9} N   Fz: {Fstr[2]:>9} N")
    elif frame.id == 2:
        # Torque
        Tx = frame.data[0] * 256 + frame.data[1]
        Ty = frame.data[2] * 256 + frame.data[3]
        Tz = frame.data[4] * 256 + frame.data[5]
        Tx = Tx / 500 - 50
        Ty = Ty / 500 - 50
        Tz = Tz / 500 - 50
        Tstr = ['{:.3f}'.format(Tx), '{:.3f}'.format(Ty), '{:.3f}'.format(Tz)]
        print(f"  Tx: {Tstr[0]:>9} Nm  Ty: {Tstr[1]:>9} Nm  Tz: {Tstr[2]:>9} Nm")


def monitor_channel(ch, ticktime):
    width, height = shutil.get_terminal_size((80, 20))

    # Transmit a message

    # Bias setting (Set the current to zero)
    # frame = Frame(
    #     id_=0x102,
    #     data=[0x01, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00],
    #     flags=canlib.MessageFlag.STD,
    # )
    # ch.write(frame)

    # Continuous transmitting mode
    frame = Frame(
        id_=0x102,
        data=[0x01, 0x03, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00],
        flags=canlib.MessageFlag.STD,
    )
    ch.write(frame)

    # Receive messages

    timeout = 0.5
    tick_countup = 0
    if ticktime <= 0:
        ticktime = None
    elif ticktime < timeout:
        timeout = ticktime

    print("Listening...")
    while True:
        try:
            frame = ch.read(timeout=int(timeout * 1000))
            printframe(frame, width)
        except canlib.CanNoMsg:
            if ticktime is not None:
                tick_countup += timeout
                while tick_countup > ticktime:
                    print(f"[{time.time():.3f}] no message")
                    tick_countup -= ticktime
        except KeyboardInterrupt:
            print("Stop.")
            break


if __name__ == '__main__':
    print("canlib version:", canlib.dllversion())

    ch = setup_channel(0, canlib.Bitrate.BITRATE_1M)
    monitor_channel(ch, 1)
    teardown_channel(ch)
