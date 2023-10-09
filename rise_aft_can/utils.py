from canlib import canlib


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
