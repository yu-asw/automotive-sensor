# ROS 2 on D3-G — 학생 배포 자료

영어 슬라이드와 한국어 실습 튜토리얼입니다. 이전 D3-G Yocto 수업을 마친 학생을 대상으로 합니다.

- [영어 슬라이드 PDF](automotive-sensor-workshop-ros2-camera-en.pdf) — 71장
- [영어 웹 슬라이드](slides.en.html) — 방향키로 이동, 애니메이션 포함
- [튜토리얼 PDF](tutorial.ko.pdf) — 빌드, FWDN, ROS 통신, USB 카메라, 제출 기록
- [튜토리얼 웹 문서](tutorial.ko.html) / [Markdown](TUTORIAL.ko.md)
- [실습 스크립트](../../labs/ros2-yocto/README.md)
- [그림·내용 출처](SOURCES.md) / [그림 라이선스](assets/reference/ATTRIBUTION.md)
- [전체 묶음 ZIP](../../downloads/ros2-d3g-student-kit.zip)

## 이용 순서

1. 슬라이드로 ROS 2와 자동차 센서 구성을 살펴봅니다.
2. 튜토리얼 1–10절에서 호스트 설정, 빌드, 이미지 검사와 패키징을 진행합니다. 전체 빌드는 수업 전에 준비합니다.
3. 보드가 준비되면 11–13절의 FWDN·부팅·ROS 통신을 확인합니다.
4. 16절의 USB 카메라 실습 후 제출 기록을 채웁니다.

2026-10-28 기준: 이미지 빌드·정적 검사·FWDN ZIP 검사는 통과했습니다. 보드·카메라 실측은 아직 하지 않았고 QEMU listener 수신도 확인되지 않았습니다. 하드웨어 성공을 전제로 한 자료가 아닙니다. FWDN low-format은 기존 eMMC 데이터를 지웁니다.

ZIP을 풀어 `workshops/ros2-camera/index.html`을 열면 오프라인에서도 문서와 그림을 볼 수 있습니다. 웹 폰트를 못 불러오면 시스템 폰트로 표시되며 PDF는 배포 당시 레이아웃을 유지합니다. SDK, 펌웨어, 빌드 이미지와 개인 네트워크 설정은 배포 묶음에 포함되지 않습니다.
