from rise_aft_can.sensors import AFT200D80

channel = 0

# open과 close를 안전하게 처리하기 위해 with 문 사용
# with 문을 사용하면, setup_channel()과 teardown_channel()을 자동으로 호출함
with AFT200D80(channel) as aft:
    aft.set_continuous_transmitting()

    for _ in range(10):
        data: list = aft.read()
        print(f"Fxyz[N], Txyz[Nm]: {data}")
