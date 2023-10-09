# AFT Python with Kvaser CAN

본 저장소는 [Aidin Robotics 사의 FT 센서](https://www.aidinrobotics.co.kr/smart-6-axis-ft-sensor)를 USB-to-CAN 장치를 통해 파이썬에서 사용하기 위한 패키지이다.
현재는 Kvaser 장치만 지원한다.

1. [Compatibility](#compatibility)
2. [Installation](#installation)
3. [Minimal Python Example](#minimal-python-example)

## Compatibility

현재 테스트된 센서는 다음과 같다.

- AFT200-D80-C

## Installation

1. 크바저 USB-to-CAN 드라이버를 설치한다.

   1. [크바저 Support 페이지](https://www.kvaser.com/download/#?categories=driver)에서 "Kvaser Linux Drivers and SDK"를 받아 설치한다.
   2. 드라이버를 설치할 때에는 실제 Kvaser 장치가 ***연결되지 않은 상태에서 설치해야 한다.*** 장비가 연결되어 있으면 경고문구와 함께 제대로 설치되지 않는다.
   3. 설치 방법은 압축 파일 안에 있는 README에 설명되어 있다. 그 내용은 보통 다음과 같다.

      ```sh
      # 압축 폴더 안에서
      $ sudo apt install build-essential pkg-config dkms
      $ make dkms
      $ sudo make dkms_install
      ```

   4. 제대로 설치가 되었다면, `/usr/doc/canlib/examples`에 있는 예제가 다음과 같이 실행되는지 확인해보자. 실제 장치를 연결할 필요는 없다.

      ```sh
      $ cd /usr/doc/canlib/examples
      $ ./listChannels
      CANlib version 5.43
      Found 2 channel(s).
      ch  0: Kvaser Virtual CAN      0-00000-00000-0, s/n 1, v0.0.0  (kvvirtualcan v8.43.472)
      ch  1: Kvaser Virtual CAN      0-00000-00000-0, s/n 1, v0.0.0  (kvvirtualcan v8.43.472)
      ```

2. 파이썬에 `rise_aft_can` 패키지를 설치한다. 본 저장소를 따로 clone할 필요는 없으며, 필요한 [canlib 패키지](https://pycanlib.readthedocs.io/)는 자동으로 설치된다.

   Pip 로 설치할 경우:

   ```sh
   $ pip install git+https://github.com/rise-lab-skku/rise-aft-can.git
   ```

   Poetry 환경에 설치할 경우:

   ```sh
   $ poetry add git+https://github.com/rise-lab-skku/rise-aft-can.git
   ```

3. 설치가 잘 되었는지 확인하기 위해, 새 터미널을 열고 다음과 같이 실행해보자.

   ```sh
   $ rise-aft-can --check
   ```

   아래와 같은 결과가 나오면 정상적으로 설치가 된 것이다. (아래에 `Kvaser U100`이 새로 생긴 것은 실제 Kvaser 장치를 연결했기 때문이므로 무시해도 된다.)

   ```sh
   canlib version: 8.43

   ######## Found 3 channels ########
   1. Kvaser U100 (channel 0) (**-*****-*****-* / *******)
   2. Kvaser Virtual CAN (channel 0) (00-00000-00000-0 / 1)
   3. Kvaser Virtual CAN (channel 1) (00-00000-00000-0 / 1)

   ######## Connected Devices ########
   CANlib Channel: 0
   Card Number   : 0
   Device        : Kvaser U100 (channel 0)
   Driver Name   : mhydra
   EAN           : **-*****-*****-*
   Firmware      : 3.24.0.744
   Serial Number : *******)

   CANlib Channel: 1
   Card Number   : 0
   Device        : Kvaser Virtual CAN (channel 0)
   Driver Name   : kvvirtualcan
   EAN           : 00-00000-00000-0
   Firmware      :
   ```

## Minimal Python Example

> 실제 센서를 연결할 때에는 반드시 적절한 전원을 인가하라. 잘못된 전원은 센서를 망가뜨릴 수 있다. AFT200-D80-C의 경우 5V DC이다.

With 문을 사용하는 경우 (권장):

```python
from rise_aft_can.sensors import AFT200D80

channel = 0

with AFT200D80(channel) as aft:
    aft.set_continuous_transmitting()
    data: list = aft.read()
    print(f"Fxyz[N], Txyz[Nm]: {data}")
```

With 문을 사용하지 않는 경우:

```python
from rise_aft_can.sensors import AFT200D80

channel = 0

aft = AFT200D80(channel)
aft.setup_channel()

aft.set_continuous_transmitting()
data: list = aft.read()
print(f"Fxyz[N], Txyz[Nm]: {data}")

aft.teardown_channel()
```

Output:

```sh
$ python3 example.py
Using channel: Kvaser U100 (channel 0), EAN: 73-30130-01173-1, Serial: 1007015
Fxyz[N], Txyz[Nm]: [-12.990000000000009, 3.579999999999984, -16.04000000000002, -0.07200000000000273, 0.4759999999999991, -0.6820000000000022]
Closing channel: Kvaser U100 (channel 0)
Channel closed.
```

보다 자세한 사용법은 [example 폴더](./example)와 [소스코드](./rise_aft_can)를 참고하라.

```sh
$ python ./example/aft200_d80_advanced.py
Using channel: Kvaser U100 (channel 0), EAN: 73-30130-01173-1, Serial: 1007015

Listening...
[1696841302.346] Fx[N]:   -12.750  | Fy[N]:     2.570  | Fz[N]:   -16.990  | Tx[Nm]:     0.044  | Ty[Nm]:     0.400  | Tz[Nm]:    -0.676
[1696841302.356] Fx[N]:   -12.140  | Fy[N]:     2.540  | Fz[N]:   -16.490  | Tx[Nm]:     0.076  | Ty[Nm]:     0.422  | Tz[Nm]:    -0.708
[1696841302.366] Fx[N]:   -12.450  | Fy[N]:     3.380  | Fz[N]:   -17.020  | Tx[Nm]:     0.004  | Ty[Nm]:     0.396  | Tz[Nm]:    -0.700
[1696841302.376] Fx[N]:   -12.210  | Fy[N]:     3.230  | Fz[N]:   -16.420  | Tx[Nm]:    -0.016  | Ty[Nm]:     0.450  | Tz[Nm]:    -0.698
```
