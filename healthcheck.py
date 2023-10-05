from canlib import canlib, connected_devices

num_channels = canlib.getNumberOfChannels()
print(f"######## Found {num_channels} channels ########")
for ch in range(num_channels):
    chd = canlib.ChannelData(ch)
    print(f"{ch}. {chd.channel_name} ({chd.card_upc_no} / {chd.card_serial_no})")

print("\n######## Connected Devices ########")
for dev in connected_devices():
    print(f"{dev.probe_info()}\n")
