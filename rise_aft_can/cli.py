import argparse
from canlib import canlib, connected_devices


def check():
    print("canlib version:", canlib.dllversion())

    num_channels = canlib.getNumberOfChannels()
    print(f"\n######## Found {num_channels} channels ########")
    for ch in range(num_channels):
        chd = canlib.ChannelData(ch)
        print(f"{ch}. {chd.channel_name} ({chd.card_upc_no} / {chd.card_serial_no})")

    print("\n######## Connected Devices ########")
    for dev in connected_devices():
        print(f"{dev.probe_info()}\n")


def main():
    parser = argparse.ArgumentParser(description="Check canlib version and connected devices.")
    parser.add_argument("--check", action="store_true", help="Check canlib version and connected devices.")
    args = parser.parse_args()

    if args.check:
        check()
