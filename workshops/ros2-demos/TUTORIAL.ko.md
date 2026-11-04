# ROS 2 데모 워크숍

**디스플레이 없는 D3를 SSH로 조작하고, 결과는 PC에서 관찰하기**

180분 / ROS 2 Humble / Ubuntu 22.04 데스크톱 PC / D3-G Yocto ROS 이미지

[자료 안내](README.md) · [강사용 진행표](INSTRUCTOR.md) · [제출 기록](RESULTS.md)

## 0. 오늘의 구성과 도착점

| 위치 | 실행할 것 | 화면 |
|---|---|---|
| Ubuntu PC | turtlesim, rqt_graph, rqt_image_view, rosbag, ROS CLI | PC 데스크톱 |
| D3 | talker/listener, USB 카메라 노드, ROS CLI | PC에서 접속한 SSH 터미널 |

D3에 모니터를 연결하지 않습니다. `ssh -X`도 사용하지 않습니다. **SSH는 원격 명령 입력 통로이고, ROS 토픽은 별도의 DDS 네트워크 통신**입니다. SSH가 된다고 영상 토픽까지 반드시 전달되는 것은 아닙니다.

성공 목표: 메시지 수신, 다른 컴퓨터 간 통신, 거북이 조작, 서비스/액션 실행, 실제 카메라 영상, 기록 데이터 재생을 각각 확인하고 증거를 남깁니다. 보드가 준비되지 않으면 PC의 demo_nodes_cpp로 ①을 실행하고 ③④⑥을 먼저 진행합니다. ②⑤는 미실시로 기록합니다.

## 1. 수업 전에 준비하기

강사는 D3 ROS 이미지 부팅, SSH 서버 동작, 로그인 가능한 계정과 인증 방법, IP 주소를 확인해 배부합니다. 기본 계정·기본 비밀번호를 추측하지 않습니다. 부팅 및 SSH 서버가 준비되지 않았다면 보드에 화면이 없으므로 강사가 USB 시리얼 콘솔과 해당 BSP 절차로 준비해야 합니다.

PC와 D3는 서로 통신 가능한 같은 실습망에 연결합니다. 가능하면 유선망을 사용합니다. 게스트 Wi-Fi의 단말 격리, VM NAT, 방화벽으로 DDS가 차단될 수 있습니다. VM이면 데스크톱 GUI와 브리지 네트워크를 사전 검증합니다.

**PC 터미널 — 이미 ROS 2 Humble 저장소가 설정된 Ubuntu 22.04에서만:**

```bash
sudo apt update
sudo apt install openssh-client ros-humble-demo-nodes-cpp \
  ros-humble-turtlesim ros-humble-rqt-graph ros-humble-rqt-image-view \
  ros-humble-ros2bag ros-humble-rosbag2-transport \
  ros-humble-rosbag2-storage-default-plugins ros-humble-rmw-fastrtps-cpp \
  ros-humble-ros2service ros-humble-ros2action
```

ROS 자체가 없는 PC는 강사가 먼저 Humble 환경을 설치합니다. 이 `apt` 명령을 Yocto D3에서 실행하지 않습니다. 이번 수업에서 이미지 빌드나 FWDN을 다시 수행하지 않습니다.

자료 ZIP을 풀고 `workshops/ros2-demos` 폴더에서 터미널을 엽니다. 저장소를 이미 받았다면 그 안의 같은 폴더로 이동합니다. 이하 PC의 시작 작업 폴더는 이 폴더입니다.

## 2. SSH 첫 접속 — PC에서 D3 터미널 열기

강사가 준 주소와 계정을 입력합니다. 아래 명령은 Ubuntu PC의 Bash 터미널 기준입니다.

```bash
read -r -p 'D3 IP 주소: ' D3_HOST
read -r -p 'D3 로그인 계정: ' D3_USER
ssh "${D3_USER}@${D3_HOST}"
```

첫 접속에서는 서버 공개키 지문이 표시됩니다. 강사가 확인한 지문과 맞는지 확인한 뒤 `yes`를 입력합니다. 비밀번호 입력 시 화면에 글자가 보이지 않는 것은 정상입니다. 키 인증 계정이면 배부받은 절차를 따릅니다. 비밀번호나 개인키를 제출 기록에 넣지 않습니다.

**접속 후부터 이 터미널은 D3입니다.** 다음으로 위치를 확인합니다.

```sh
hostname
whoami
uname -m
cat /etc/os-release
ip -br addr
```

D3 이미지라면 ARM64(`aarch64`)와 Yocto 계열 OS 정보가 기대됩니다. 실제 출력을 기록합니다. PC의 Ubuntu 정보와 혼동하지 않습니다.

- 원격 명령 종료: `Ctrl+C`. SSH 연결은 유지됩니다.
- D3 터미널 종료: `exit`. PC 프롬프트로 돌아옵니다.
- 새 D3 터미널: PC에서 새 탭을 열고 같은 `ssh 사용자@주소`로 다시 접속합니다.
- 새 탭에서는 `D3_HOST`, `D3_USER` 변수도 자동 복사되지 않습니다. 입력 명령을 반복하거나 실제 계정·주소를 직접 씁니다.
- 각 SSH 연결은 독립된 셸입니다. ROS 환경도 각 탭에서 설정해야 합니다.
- 수업 중 실행한 노드는 SSH 연결 종료 시 중단될 수 있습니다. 연결을 유지합니다.

### 접속이 안 될 때

| 증상 | 확인할 것 |
|---|---|
| timeout / No route to host | 보드 전원, 케이블, 현재 DHCP 주소, PC와 보드의 네트워크 |
| Connection refused | 해당 주소가 D3인지, SSH 서버가 준비되었는지 강사 확인 |
| Permission denied | 계정과 비밀번호/키 인증 방법 확인 |
| REMOTE HOST IDENTIFICATION HAS CHANGED | 강사에게 이미지 교체와 새 지문 확인. 확인 없이 known_hosts 항목 삭제 금지 |

IP를 모르면 강사가 공유기 DHCP 목록 또는 USB 시리얼에서 확인합니다. 디스플레이 없는 보드에 직접 터미널 명령을 입력하라고 가정하지 않습니다.

## 3. 모든 ROS 터미널의 공통 설정

강사가 팀별 Domain ID를 배정합니다. 아래 `10`은 예시이며 **같은 팀의 PC와 D3는 같은 값**, 다른 팀은 다른 값을 사용합니다.

**PC의 새 터미널마다:**

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=10
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_LOCALHOST_ONLY=0
```

**D3의 새 SSH 터미널마다:**

```sh
. /opt/ros/humble/local_setup.sh
export ROS_DOMAIN_ID=10
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_LOCALHOST_ONLY=0
```

환경을 바꿀 때는 해당 실습 노드를 `Ctrl+C`로 종료하고 `ros2 daemon stop`을 실행한 뒤 재시작합니다. 기존 실행 노드는 셸 환경 변경을 자동으로 반영하지 않습니다.

자료 폴더에서는 위 설정 대신 `export ROS_DOMAIN_ID=10` 후 `. ./scripts/env.sh`를 사용할 수도 있습니다. 자동으로 Humble 설정 파일을 찾으며 현재 셸에 적용해야 하므로 `sh scripts/env.sh`로 실행하지 않습니다.

**PC — 준비 검사:**

```bash
bash scripts/check-env.sh pc
```

**선택: PC에서 검사 도구를 D3로 복사** — 2절의 변수가 설정된 PC 탭에서 실행합니다.

```bash
ssh "${D3_USER}@${D3_HOST}" 'mkdir -p ~/ros2-workshop'
scp scripts/env.sh scripts/check-env.sh "${D3_USER}@${D3_HOST}:ros2-workshop/"
```

**D3 SSH 터미널:**

```sh
export ROS_DOMAIN_ID=10
. ~/ros2-workshop/env.sh
sh ~/ros2-workshop/check-env.sh d3
```

오래된 보드 SSH 서버가 SFTP를 지원하지 않아 `scp`가 실패하면 PC의 `scp -O` 옵션으로 기존 SCP 프로토콜을 사용할 수 있습니다. 이 검사는 패키지 존재를 확인하며, 통신 성공을 보증하지 않습니다.

## 4. 데모 ① — Talker / Listener

**D3 SSH-A:** 3절 환경 설정 후 실행합니다.

```sh
ros2 run demo_nodes_cpp talker
```

**D3 SSH-B:** 별도 SSH 접속 및 3절 설정 후 실행합니다.

```sh
ros2 run demo_nodes_cpp listener
```

**D3 SSH-C:** 별도 SSH 접속 및 3절 설정 후 관찰합니다.

```sh
ros2 node list
ros2 topic list -t
ros2 topic info /chatter --verbose
ros2 topic echo /chatter
```

관찰: talker의 번호가 증가하며 listener에 같은 문자열이 도착하는지 봅니다. `topic echo`도 하나의 구독자입니다. SSH-C에서 `Ctrl+C`로 echo를 멈추고 `ros2 topic hz /chatter`를 실행해 수신 주기를 봅니다. 이후 `Ctrl+C`로 종료합니다.

미션: talker만 종료하면 listener 출력이 멈추는지, talker를 다시 시작하면 다시 수신하는지 확인합니다. **완료 기준: 실제로 연속 수신한 로그.**

## 5. 데모 ② — PC ↔ D3 통신

D3 SSH-A의 talker는 유지하고 SSH-B의 listener는 종료합니다.

**PC-A:** 3절 PC 환경을 설정하고 실행합니다.

```bash
ros2 run demo_nodes_cpp listener
```

**PC-B:** 환경 설정 후 연결을 확인합니다.

```bash
ros2 topic info /chatter --verbose
ros2 run rqt_graph rqt_graph
```

그래프에서 talker와 listener의 연결을 봅니다. 필요하면 GUI의 새로고침을 누릅니다. 그래프에 보이는 것과 실제 문자열 수신을 따로 확인합니다.

미션: PC-A의 listener를 종료하고 해당 탭만 `ROS_DOMAIN_ID=11`로 바꾼 뒤 재실행합니다(강사가 충돌 없는 실험용 값을 배정). D3와 값이 다르면 메시지가 오지 않아야 합니다. 다시 종료하고 원래 팀 값으로 복구한 뒤 재실행합니다.

**완료 기준: 원격 수신 로그 + Domain ID 불일치/복구 결과.** 끝나면 talker, listener, rqt_graph를 각 터미널에서 `Ctrl+C`로 종료합니다.

## 6. 데모 ③ — 거북이 운전과 토픽

이 데모는 모두 **PC에서** 실행합니다. 각 새 터미널에서 3절 PC 환경을 설정합니다.

**PC-A:**

```bash
ros2 run turtlesim turtlesim_node
```

**PC-B:**

```bash
ros2 run turtlesim turtle_teleop_key
```

거북이 그림 창이 아니라 **PC-B 터미널에 키보드 포커스**를 놓고 방향키를 누릅니다.

**PC-C:**

```bash
ros2 topic echo /turtle1/cmd_vel
```

키를 누를 때 선속도 `linear.x`와 각속도 `angular.z`가 출력되는지 봅니다. `Ctrl+C`로 echo를 종료하고 다음을 실행합니다.

```bash
ros2 topic echo /turtle1/pose
```

이번에는 위치와 방향이 바뀌는 것을 확인합니다. 다시 `Ctrl+C`로 종료합니다.

PC-B의 키보드 노드를 `Ctrl+C`로 종료한 후 **PC-C**에서 직접 명령을 보냅니다.

```bash
ros2 topic pub --rate 10 /turtle1/cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 2.0}, angular: {z: 1.0}}'
```

원이 그려지는지 확인합니다. 10초 정도 뒤 `Ctrl+C`로 발행을 멈추고 0 속도 명령을 보냅니다.

```bash
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 0.0}, angular: {z: 0.0}}'
```

**완료 기준: 키보드·직접 토픽 발행의 두 방식으로 움직이고 명령/위치 데이터를 구분.** turtlesim 창은 다음 데모를 위해 유지합니다.

## 7. 데모 ④ — 서비스·파라미터·액션

**PC-C — 서비스: 거북이 한 마리 추가 요청**

```bash
ros2 service list -t
ros2 interface show turtlesim/srv/Spawn
ros2 service call /spawn turtlesim/srv/Spawn \
  '{x: 2.0, y: 2.0, theta: 0.0, name: "turtle2"}'
```

`turtle2`가 생기고 응답에 이름이 돌아오는지 확인합니다. 같은 이름으로 다시 만들면 실패할 수 있으므로 기존 것을 지우려면 다음을 실행합니다.

```bash
ros2 service call /kill turtlesim/srv/Kill '{name: "turtle2"}'
```

**PC-C — 파라미터: 실행 중 설정 변경**

```bash
ros2 param get /turtlesim background_r
ros2 param set /turtlesim background_r 150
```

배경색 변화를 확인합니다. 변경은 이 노드 실행 세션에 적용됩니다.

**PC-C — 액션: 목표 각도로 회전하고 진행 상황 확인**

```bash
ros2 action list -t
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute \
  '{theta: 1.57}' --feedback
```

목표 수락, 남은 회전량 피드백, 완료 결과를 구분합니다. 실행 전 다른 속도 발행기는 종료되어 있어야 합니다.

취소 실험은 **PC-B**에서 `ros2 run turtlesim turtle_teleop_key`를 다시 실행하고 터미널에 포커스를 둡니다. `G/B/V/C/D/E/R/T` 중 현재 방향과 다른 방향의 키를 누르고 회전이 끝나기 전에 `F`를 누릅니다. `F`는 회전 액션 취소입니다. CLI 명령에서 `Ctrl+C`를 누르는 것을 액션 취소 확인으로 대체하지 않습니다.

**완료 기준: 서비스 응답, 색 변경, 액션 완료와 취소 로그.** 취소 로그는 turtlesim을 실행한 PC-A에서 봅니다. 끝나면 키보드 노드를 종료합니다.

## 8. 데모 ⑤ — D3 USB 카메라를 PC에서 보기

카메라는 D3 USB 포트에 연결합니다. PC 내장 웹캠과 혼동하지 않습니다.

**D3 SSH-A — ROS 환경 설정 후 장치 확인:**

```sh
lsusb
v4l2-ctl --list-devices
v4l2-ctl -d /dev/video0 --list-formats-ext
```

`/dev/video0`은 예시입니다. 출력으로 실제 캡처 장치를 고릅니다. 이 이미지의 v4l2_camera는 YUYV/UYVY/GREY 입력을 사용합니다. 아래는 **YUYV 640×480 지원을 확인한 경우**입니다. MJPEG 전용 모드를 그대로 지정하지 않습니다.

```sh
v4l2-ctl -d /dev/video0 \
  --set-fmt-video=width=640,height=480,pixelformat=YUYV \
  --stream-mmap --stream-count=30 --stream-to=/tmp/workshop-camera.yuyv
```

캡처 종료 코드와 로그를 확인합니다. raw 파일이 만들어졌다는 사실만으로 화면 품질까지 검증된 것은 아닙니다. 캡처 도구가 종료된 뒤 노드를 시작합니다.

```sh
ros2 run v4l2_camera v4l2_camera_node --ros-args \
  -r __ns:=/camera \
  -p video_device:=/dev/video0 \
  -p pixel_format:=YUYV \
  -p 'image_size:=[640,480]'
```

**D3 SSH-B:**

```sh
ros2 topic info /camera/image_raw --verbose
ros2 topic hz /camera/image_raw
```

**PC-B — 3절 환경 설정 후:**

```bash
ros2 run rqt_image_view rqt_image_view
```

드롭다운에서 `/camera/image_raw`를 고릅니다. 렌즈 앞에서 손을 움직여 현재의 실제 영상인지 확인합니다. 뷰어에 QoS 선택 기능이 있으면 publisher와 호환되게 맞춥니다.

**PC-C:**

```bash
ros2 topic hz /camera/image_raw
```

D3와 PC의 수신 주기를 각각 기록하고 `Ctrl+C`로 관측을 종료합니다. `hz`는 해당 구독자의 수신 빈도이며 카메라의 설정 FPS와 동일하다고 단정하지 않습니다.

미션: 지원 목록에 다른 해상도가 있으면 카메라 노드를 종료하고 지원되는 값으로 재시작해 비교합니다. 보드/PC CPU, 대역폭, 지연의 변화를 관찰합니다. **완료 기준: PC에서 실제 움직이는 영상 + 포맷·해상도·수신 빈도 기록.**

## 9. 데모 ⑥ — rosbag 기록과 재생

기본 실습은 PC의 turtlesim으로 진행합니다. 카메라는 선택 확장입니다. 각 터미널에 3절 PC 환경을 적용합니다.

### A. 거북이 조작 기록

6절의 turtlesim이 실행 중인지 확인합니다. 직접 속도 발행기와 키보드 노드는 종료한 상태로 시작합니다.

**PC-C:**

```bash
ros2 service call /reset std_srvs/srv/Empty '{}'
mkdir -p ~/ros2-workshop-recordings
cd ~/ros2-workshop-recordings
ros2 bag record -o "turtle-$(date +%Y%m%d-%H%M%S)" /turtle1/cmd_vel
```

**PC-B:** 키보드 노드를 실행하고 약 10초 동안 거북이를 움직입니다. 끝나면 키에서 손을 떼고 잠시 기다린 다음 키보드 노드를 `Ctrl+C`로 종료합니다. PC-C의 녹화도 `Ctrl+C`로 정상 종료합니다.

```bash
ros2 run turtlesim turtle_teleop_key
```

### B. 입력 노드 없이 재생

**PC-C:** 생성된 디렉터리 목록을 확인하고 재생할 이름을 입력합니다.

```bash
ls -d ~/ros2-workshop-recordings/turtle-*
read -r -p '재생할 bag 디렉터리 전체 경로: ' BAG_DIR
ros2 bag info "$BAG_DIR"
ros2 service call /reset std_srvs/srv/Empty '{}'
ros2 bag play "$BAG_DIR"
```

키보드 노드가 꺼져 있어도 거북이가 움직이는지 봅니다. 같은 초기 위치에서 재생하지만 타이밍과 시뮬레이션 차이로 궤적이 완전히 같지는 않을 수 있습니다. 기록한 것은 영상이 아니라 **속도 명령 메시지**입니다. `/pose`만 재생하는 것은 거북이를 운전하는 것과 다릅니다.

### C. 선택: 카메라를 끄고 영상 재생

5절 카메라 노드를 켠 상태에서 **PC-C**에서 실행합니다.

```bash
cd ~/ros2-workshop-recordings
df -h .
ros2 bag record -o "camera-$(date +%Y%m%d-%H%M%S)" /camera/image_raw
```

raw 영상은 용량이 크므로 5~10초만 기록하고 `Ctrl+C`로 종료합니다. `ros2 bag info`로 메시지 수가 0이 아닌지 확인합니다. D3 SSH-A에서 **카메라 노드를 종료**하고, turtlesim 때와 같은 방법으로 새 bag 경로를 `BAG_DIR`에 입력한 뒤 `ros2 bag play "$BAG_DIR"`를 실행합니다. PC 영상 뷰어로 녹화된 움직임이 보이는지 확인합니다.

라이브와 재생 발행기를 동시에 켜 두면 같은 토픽에 영상이 섞일 수 있습니다. 녹화 메시지가 없으면 publisher의 QoS와 recorder 연결을 먼저 확인합니다.

**완료 기준: bag의 토픽·메시지 수 확인 + 원래 입력/카메라 노드가 꺼진 상태에서 재생 성공.**

## 10. 문제가 생기면 이 순서로 확인

| 증상 | 확인 순서 |
|---|---|
| ros2 명령 없음 | 현재 PC인지 D3인지 → 해당 환경 설정 파일 → 설치/이미지 |
| SSH는 되지만 토픽이 안 보임 | 양쪽 Domain ID·localhost·RMW → 기존 노드 재시작·daemon → LAN/방화벽/단말 격리 |
| 토픽은 보이나 메시지가 없음 | 실제 발행 로그 → `topic info --verbose`의 QoS → UDP 데이터 경로 |
| 카메라가 안 보임 | USB 인식 → V4L2 지원 포맷 → 직접 캡처 → ROS 노드 → PC 토픽 → 뷰어 |
| 거북이가 안 움직임 | 키보드 터미널 포커스 → cmd_vel → 중복 발행기 → 실행 중인 turtlesim |
| GUI가 열리지 않음 | D3 SSH에서 실행했는지 확인. GUI는 Ubuntu 데스크톱 PC 터미널에서 실행 |
| bag에 메시지가 없음 | record 실행 중 발행했는지 → 토픽 이름 → QoS → 저장 공간 |

방화벽을 무조건 끄거나 시스템 설정을 임의로 바꾸지 말고 강사에게 네트워크 진단을 요청합니다. 다른 사용자의 ROS 프로세스를 일괄 종료하지 않습니다.

## 11. 종료와 제출

각 데모의 실행 터미널에서 `Ctrl+C`로 노드를 종료합니다. SSH 터미널은 `exit`로 나갑니다. 보드 전원 종료는 강사의 안내에 따릅니다.

[RESULTS.md](RESULTS.md)를 복사해 실제 결과와 로그·스크린샷 경로를 기록합니다. 성공/실패/미실시를 구분합니다. 비밀번호·개인키는 제출하지 않습니다.

## 참고 자료

- [ROS 2 Humble 공식 입문 튜토리얼](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools.html)
- [공식 turtlesim 예제 원문](https://github.com/ros2/ros2_documentation/blob/humble/source/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.rst)
- [공식 서비스 예제](https://github.com/ros2/ros2_documentation/blob/humble/source/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.rst)
- [공식 파라미터 예제](https://github.com/ros2/ros2_documentation/blob/humble/source/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Parameters/Understanding-ROS2-Parameters.rst)
- [공식 액션 예제](https://github.com/ros2/ros2_documentation/blob/humble/source/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions/Understanding-ROS2-Actions.rst)
- [공식 rosbag 예제](https://github.com/ros2/ros2_documentation/blob/humble/source/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.rst)
- 기존 저장소의 `workshops/ros2-camera/TUTORIAL.ko.md`: 검증 이력과 D3 카메라 절차

작성일: 2026-11-04. 문서·스크립트 검사는 실제 Ubuntu/D3 데모 리허설과 별개입니다.
