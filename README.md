# AFT80 Python with Kvaser CAN

## Installation

1. 크바저 USB-to-CAN 드라이버 설치

   1. [크바저 Support 페이지](https://www.kvaser.com/download/#?categories=driver)에서 "Kvaser Linux Drivers and SDK"를 받아 설치한다.
   2. 드라이버를 설치할 때에는 실제 Kvaser 장치가 ***연결되지 않은 상태에서 설치해야 한다.*** 장비가 연결되어 있으면 경고문구와 함께 제대로 설치되지 않는다.
   3. 설치 방법은 압축 파일 안에 있는 README에 설명되어 있다. 그 내용은 보통 다음과 같음.

      ```sh
      # 압축 폴더 안에서
      sudo apt install build-essential pkg-config dkms
      make dkms
      sudo make dkms_install
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

2. 파이썬에서 크바저 드라이버에 접근할 수 있도록 [canlib 패키지](https://pycanlib.readthedocs.io/)를 설치한다.

   1. 다음과 같이 쉽게 설치할 수 있다.

      ```sh
      pip install canlib
      ```

   2. 설치가 잘 되었는지 본 저장소에 들어있는 `healthcheck.py`를 실행해 보자. (`listChannels`와 동일하고, 아래에 `Kvaser U100`이 새로 생긴 것은 실제 Kvaser 장치를 연결했기 때문이므로 무시해도 된다.)

      ```sh
      $ python3 healthcheck.py
      ######## Found 3 channels ########
      0. Kvaser U100 (channel 0) (73-30130-01173-1 / 1007015)
      1. Kvaser Virtual CAN (channel 0) (00-00000-00000-0 / 1)
      2. Kvaser Virtual CAN (channel 1) (00-00000-00000-0 / 1)

      ######## Connected Devices ########
      CANlib Channel: 0
      Card Number   : 0
      Device        : Kvaser U100 (channel 0)
      Driver Name   : mhydra
      EAN           : 73-30130-01173-1
      Firmware      : 3.24.0.744
      Serial Number : 1007015

      CANlib Channel: 1
      Card Number   : 0
      Device        : Kvaser Virtual CAN (channel 0)
      Driver Name   : kvvirtualcan
      EAN           : 00-00000-00000-0
      Firmware      : 0.0.0.0
      Serial Number : 1
      ```

## Getting Started

1. 배선 연결 및 5V 전원 인가 (잘못된 전원은 센서를 망가뜨릴 수 있으므로 각별히 주의할 것)
2. `python3 aft200-d80.py`를 실행한다.
