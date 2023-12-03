from rise_aft_can.sensors import AFT200D80

channel = 0

# with 문을 사용하지 않는 경우
# with 문을 사용하지 않는 경우, 명시적으로 setup_channel()과 teardown_channel()을 호출해야 함
aft = AFT200D80(channel)
aft.setup_channel()

aft.set_continuous_transmitting()

for _ in range(10):
    data: list = aft.read()
    print(f"Fxyz[N], Txyz[Nm]: {data}")

aft.teardown_channel()
