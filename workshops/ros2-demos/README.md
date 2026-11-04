# ROS 2 데모 워크숍 — SSH로 D3를 연결하고 실행하기

180분 · ROS 2 Humble · Ubuntu 22.04 PC + 디스플레이 없는 D3-G

[웹 실습서](index.html) · [실습서 원본](TUTORIAL.ko.md) · [강사용 진행표](INSTRUCTOR.md) · [학생 결과 기록](RESULTS.md) · [오프라인 ZIP](../../downloads/ros2-demos-workshop.zip)

PC에서는 turtlesim, rqt_graph, 영상 뷰어, rosbag을 실행합니다. D3에서는 SSH로 talker/listener와 USB 카메라 노드를 실행합니다. SSH X11 전달이나 D3 디스플레이는 필요하지 않습니다.

실행 순서: SSH 접속 → 메시지 송수신 → PC–D3 통신 → 거북이 운전 → 서비스·파라미터·액션 → 카메라 → 기록·재생.

현재 상태: 문서 및 보조 도구 작성. 실제 Ubuntu/D3에서의 리허설 결과는 아직 없습니다. 이전 이미지 빌드 성공은 이번 데모의 동작 확인을 의미하지 않습니다.

`bash scripts/check-env.sh pc` 또는 D3에서 `sh scripts/check-env.sh d3`로 준비 상태를 확인합니다. `scripts/env.sh`는 각 ROS 터미널에서 읽는 환경 설정 파일입니다. 주소·계정·비밀번호는 포함하지 않습니다.
