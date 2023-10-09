from rise_aft_can.sensors import AFT200D80

channel = 0

# ---------------------------------------------------
# open과 close를 안전하게 처리하기 위해 with 문 사용.
# with 문을 사용하지 않는 경우, 명시적으로 setup_channel()과 teardown_channel()을 호출해야 함.
with AFT200D80(channel) as aft:
    aft.set_continuous_transmitting()
    data: list = aft.read()
    print(f"Fxyz[N], Txyz[Nm]: {data}")

# ---------------------------------------------------
# with 문을 사용하지 않는 경우
aft = AFT200D80(channel)
aft.setup_channel()

# aft.set_continuous_transmitting()  # 방금 위에서 이미 설정했으므로 스킵
data: list = aft.read()
print(f"Fxyz[N], Txyz[Nm]: {data}")

aft.teardown_channel()
