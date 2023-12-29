from rise_aft_can.sensors import AFT200D80
from rise_aft_can.utils import print_pretty_raw_frame

channel = 0

# open과 close를 안전하게 처리하기 위해 with 문 사용
# with 문을 사용하면, setup_channel()과 teardown_channel()을 자동으로 호출함
with AFT200D80(channel) as aft:
    aft.set_continuous_transmitting()

    for _ in range(10):
        raw_frame = aft.ch.read(timeout_sec=1)

        # raw frame
        print_pretty_raw_frame(raw_frame)

        # raw byte array
        print(f"=> Raw Byte Array: {bytes(raw_frame.data)}")
