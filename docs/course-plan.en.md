# Automotive Sensor — Course Plan (student handout)

- Offered by: Department of Automotive Software, Yeungnam University · **Fall 2026** · third-year fall major elective, 3 credits (3 hours/week)
- Enrollment: **two students** — run as a project-based course
- Issued: September 2026 (Lecture 1)

---

## 0. First, why two students is an advantage

This course was originally designed for a class of twenty. Under that plan four of you would have shared a single board, and you would have spent most of the lab **watching someone else do the work**. With two students, this becomes possible instead.

| | Class of 20 | **Two students (this plan)** |
|---|---|---|
| Equipment | one kit shared by four | **one kit each, plus a project vehicle dedicated to the two of you** |
| Radar lab | HB100 Doppler module and no further; automotive FMCW radar as an instructor demo only | **hands-on with a TI IWR6843 mmWave radar** (out of reach on a 20-student budget) |
| Deliverable | four individual written assignments | **one self-driving vehicle that actually drives, plus the subsystem you built** |
| Feedback | a few times a semester | **a face-to-face lab meeting every week, every lab notebook marked up** |
| Level | pitched down so that everyone can keep up | **pitched up, on the assumption that we dig you out on the spot** |

One condition comes attached. **With two of you there is nowhere to hide.** Every week you have to record what you did and explain it, and if one of you stops, the whole project stops. This plan is written on that assumption.

---

## 1. What this course covers

Self-driving and ADAS both start at the **sensors** that stand in for the human eye. This course covers the six environment-perception sensors on a vehicle — **camera, ultrasonic, radar, lidar, GNSS, IMU** — how they work, how to read their specifications, and how to interface with them and get their data out.

The boundary is deliberate. This course goes as far as **"what physical principle a sensor uses to measure the world, and in what form that data arrives in software."** The algorithms that process that data belong to the courses that follow.

| Topic | Course |
|---|---|
| Sensor principles · specifications · interfaces · data acquisition | **Automotive Sensor (this course, year 3 fall)** |
| Learning algorithms — CNN, RNN and the rest | Deep Learning (year 3 fall, recommended alongside) |
| 2D image and 3D point-cloud signal processing, object recognition | Automotive Vision (year 4 spring) |
| Advanced sensor fusion, navigation, perception, control | Autonomous Driving (year 4 fall) |

### What you will be able to do afterwards

1. Explain how each of the six sensors works down to the physics, and read the numbers that matter on a datasheet (resolution, FOV, range resolution, detection range).
2. **Wire a sensor up yourself and get data out of it** on an embedded board (TOPST D3-G), over GPIO, I2C, UART, MIPI-CSI/V4L2 and GStreamer.
3. Calibrate a camera, and explain the intrinsic and extrinsic parameters and the distortion model.
4. Read camera, lidar and radar data from public real-vehicle datasets (KITTI, nuScenes), visualize it and do a first analysis.
5. Compare what each sensor is good and bad at (light, weather, range, resolution) and explain why sensor fusion is necessary.
6. **Integrate several sensors into a single real-time system, and make that system work on a moving vehicle.** ← added because there are only two of you

---

## 2. The semester project: a sensor-integrated self-driving mini car

### 2-1. Platform

The two of you build **one** 1/10-scale self-driving vehicle **together**, on a **TOPST D3-G** (Telechips TCC8050, a Korean automotive SoC) with a **PiRacer chassis**.
The software is Ubuntu 22.04 + **ROS2 Humble**. Every sensor gets its own ROS2 node and the nodes hand data to each other over topics — the same structure a real autonomous-driving software stack uses.

> Note: this platform (D-Racer) is the official platform of the 2026 SEA:ME hackathon (sponsored by Volkswagen Group Korea, hosted by Kookmin University). What you build this semester can go straight into the competition, or into capstone design.

**The order is "get the car driving first, then put the sensors on one at a time."** Two weeks of groundwork → drive the car with the camera (weeks 3–6) → add the lidar (weeks 7–9) → add the radar (weeks 10–12) → integrate (weeks 13–15). Every time a sensor goes on, the same four steps repeat: **principle → wiring and acquisition → turn it into a vehicle capability → demo and record**.

### 2-2. Final demo scenario (week 15)

On an indoor track, the vehicle does the following.

1. **Lane-following autonomous driving with the camera** — one full lap of the track
2. **Detect an obstacle ahead, then stop or steer around it** — ultrasonic + 2D lidar (AEB in miniature)
3. **Measure the speed of an approaching object** — HB100 Doppler radar
4. **Log the driven trajectory** — GNSS + IMU, visualized afterwards
5. **Show all six sensor streams live in one place** — ROS2 topics + dashboard

### 2-3. Who owns what

You share one platform, and on it each of you has an **assigned subsystem**. The assignment is what you are responsible for delivering — it is **not the scope of what you learn.** The lectures and the midterm cover all six sensors, and both of you study all six.

| | **Student A — Perception / Vision** | **Student B — Ranging / Localization** |
|---|---|---|
| Sensors | MIPI-CSI camera, USB webcam | ultrasonic, Doppler radar, 2D lidar, GNSS, IMU |
| Main work | V4L2/GStreamer video pipeline, camera calibration, lane detection (Canny + Hough), steering-angle computation | GPIO ToF ranging, Doppler speed computation, lidar scans and obstacle clustering, NMEA parsing, I2C IMU, 1D Kalman filter |
| ROS2 topics published | `/camera/image_raw`, `/lane/steering_angle` | `/ultrasonic/range`, `/scan`, `/radar/speed`, `/gps/fix`, `/imu/data` |
| Shared by both | system architecture, vehicle control (motor and servo) node, integration, dashboard, final demo | same |

**Peer teaching is a graded item.** At every lab meeting you brief the other person on your own progress, and just before week 8 and again in week 14 you sit an **oral check on the other person's sensors**. There are only two of you, so each of you is the other's only audience and only reviewer.

### 2-4. Milestones (four)

| | When | Pass criteria |
|---|---|---|
| **M1 — Platform alive** | end of week 4 | D3-G boots, ROS2 nodes talk to each other, motor and servo under remote control drive 3 m in a straight line, CSI camera streams video |
| **M2 — Camera autonomy** | end of week 6 | one lap of the track (straights and gentle curves) driving on detected lane lines; stops when the ultrasonic sees something within 30 cm ahead |
| **M3 — Lidar integrated** | end of week 9 | 2D lidar gives range and bearing to an obstacle ahead, and the car **slows down or steers around it rather than stopping**; no conflict with the camera-based driving |
| **M4 — Radar integrated** | end of week 12 | Doppler speed measurements logged, approach warning working, camera, lidar and radar topics published simultaneously |

The final demo (week 15) is judged on all of that plus the ultrasonic and IMU: **all six sensors publishing at once, a driving log (rosbag), and the dashboard**.

> **Milestones are not scored pass/fail.** They are scored on the attempt and on the record of it. A failed attempt can still earn full marks if the lab notebook holds an analysis of the cause and the next hypothesis. Half of any hardware project fails — that is the normal state. Do not hide it, write it down.

---

## 3. How the course runs

### The three-hour session

| Time | What happens |
|---|---|
| 0:00–1:30 | **90-minute lecture** — 10-minute lab meeting (each of you briefs last week's progress, where you are stuck, this week's plan), then the principle, specifications and interface of the week's sensor (both of you together) |
| 1:30–3:00 | **90-minute lab** — connect the week's sensor → acquire data → fold it into the vehicle. I am in the room; when you get stuck, we dig it out on the spot |

### Weekly lab notebook (due every week, 20% of the grade)

**Commit it as Markdown to your GitHub repository every week.** It is graded on care and specificity, not length.

1. **Theory summary** — three to five lines on what you learned this week, and state outright what you did not understand
2. **Progress log** — what you did / where you got stuck / what you tried / next week's plan
3. **Evidence** — measurements, plots, screenshots, oscilloscope captures, failure logs
4. **Source code** — committed to the same repository

By the end of the semester that repository is your **portfolio**. In a job interview, a graduate application or a hackathon, what proves what you built is this record, not a transcript.

### Dataset labs (done in class)

The project vehicle uses low-cost sensors. For real data from vehicle-grade sensors (3D lidar, 77 GHz radar) you work with **public real-vehicle datasets instead**: KITTI lidar point clouds in week 8, the nuScenes radar lab in week 11. Run these on your own laptop (Colab is fine).

---

## 4. Weekly plan

| Week | Theory — 90-minute lecture | Project — 90-minute lab | Due / checkpoint |
|---|---|---|---|
| 1 | Orientation · autonomous driving concepts (sense-plan-act, SAE levels, ADAS and its sensors) · embedded systems and vehicle computing · the development environment | Dev-PC setup (Ubuntu 22.04), GitHub lab-notebook repository, SSH keys, talk through roles | Lab Notebook #1 |
| 2 | Embedded Linux anatomy (bootloader · kernel · rootfs · device tree) · ROS2 architecture (nodes, topics) · sensor interfaces at a glance (GPIO/I2C/UART/CSI) | **Flash the D3-G image → boot → SSH → ROS2 hello** · settle roles, draft the system architecture | Design document |
| 3 | Camera principles — image sensor (CMOS · Bayer · ISP), lens and field of view, pinhole model · MIPI-CSI and V4L2 | Connect the CSI camera, GStreamer pipeline, publish the image topic · assemble the PiRacer chassis | |
| 4 | Camera calibration (intrinsics and distortion) · vehicle actuators (PWM, servo and DC motor drivers) | Checkerboard calibration · motor and servo ROS2 nodes · remote driving | **M1** |
| 5 | Image processing basics — color spaces, Canny edges, Hough lines, ROI · designing the lane-detection pipeline | Lane-detection node → steering angle → wire it to the control node | |
| 6 | Feel for a control loop (proportional control, lag, oscillation) · ultrasonic ToF and GPIO timing | Tune the lane following · HC-SR04 stop-for-obstacle | **M2** |
| 7 | Lidar principles — laser and ToF, scanning methods, point-cloud structure, laser safety classes · reading a 2D lidar datasheet | Connect the YDLIDAR, ROS2 driver, visualize `/scan` | |
| 8 | **Midterm concept check (30 min, weeks 1–7)** · point-cloud processing — polar conversion, clustering, ground separation · 3D lidar and KITTI | Obstacle-detection node (range and bearing) · KITTI lab | Midterm check |
| 9 | Sensor coordinate frames and extrinsic calibration (camera-to-lidar alignment) · designing the avoidance behavior (stop → slow down → steer) | Integrate lidar-driven slowing and steering around, reconcile with camera driving | **M3** |
| 10 | Radar principles — radio waves and frequency bands, the Doppler effect, CW vs FMCW, chirp and beat frequency | Speed measurement with the HB100 Doppler module, look at the IF signal | |
| 11 | Range-Doppler map (2D FFT), CFAR, angle estimation · automotive radar (SRR/LRR, ACC and AEB), 4D imaging radar | **TI IWR6843 mmWave lab** · nuScenes radar lab | |
| 12 | Designing approach-warning and AEB logic · IMU and GNSS at a glance (drift, positioning error) | Integrate the radar approach warning · IMU logging (optional) | **M4** |
| 13 | Sensor fusion at a glance — what each sensor is good and bad at, intuition for the Kalman filter (1D) | All six topics publishing at once, rosbag recording, dashboard | |
| 14 | Simulators (CARLA) at a glance · how to structure a presentation | Integration rehearsal · oral check on the other person's sensors | Rehearsal |
| 15 | — | **Final demo · presentation (20 min each) · report** | **Final** |

---

## 5. Grading

| Item | Weight | What it covers |
|---|---|---|
| **Project** | **50%** | four milestones 20% (5% each) + final demo 20% + final report 10% |
| **Weekly lab notebook** | **20%** | submitted every week (14 of them). Each missed submission costs marks |
| **Midterm concept check** | **20%** | 30-minute written paper at the start of the week 8 lecture, covering the theory from weeks 1–7 |
| **Participation and peer teaching** | **10%** | how seriously you brief at lab meetings, oral checks on the other person's sensors (weeks 8 and 14) |

There is no final exam; **the final demo, presentation and report take its place**.

**The final report** is submitted individually and contains: (1) the architecture of the whole system, (2) the sensor principles, specifications, implementation and measurements for **your own subsystem**, (3) what failed and why, (4) your own conclusion on the limits of each sensor and why sensor fusion is needed, (5) what you would improve.

---

## 6. Equipment (issued to each student / shared)

| Category | Items |
|---|---|
| **Shared — the project vehicle** | one TOPST D3-G, PiRacer chassis, ArduCam OV5647 CSI camera, YDLIDAR X4 2D lidar, battery and charger |
| **Issued to each student (one kit each)** | HC-SR04 ultrasonic, MPU-6050 IMU, NEO-6M GPS, HB100 Doppler radar module, breadboard, jumpers and resistor kit, USB webcam, microSD |
| **Shared lab equipment** | TI IWR6843ISK mmWave radar evaluation board, checkerboard, oscilloscope, GPU PC for running CARLA |

The parts issued to you are yours to take away and work on during the semester. **Burning parts out and breaking them is inside the scope of learning** — damage does not cost you marks, and there are spares. Just record how you broke it in the lab notebook.

---

## 7. Textbooks

| Category | Reference |
|---|---|
| Required textbook | Jeong Seung-hwan, *Autonomous Vehicle Engineering* (자율주행 자동차공학), 2nd ed., Golden Bell, 2024 (Part 2, "Perception") |
| Supplementary textbook | Hanky Sjafrie, *Introduction to Self-Driving Vehicle Technology* (자율주행차량 기술 입문, Korean ed. tr. Kim Eun-do et al., Acorn, 2021) (Chapter 2, hardware and sensors) |
| Free resources | Yeong et al., *Sensors* 21(6), 2021 (open-access review) · TI mmWave Training Series · TOPST official documentation (github.com/topst-development) · rlabbe, *Kalman and Bayesian Filters in Python* · the KITTI and nuScenes datasets |

---

## 8. What to have ready in the first two weeks

You set your development PC up in the Lecture 1 lab and power the D3-G on in Lecture 2. **The list below has to be in place before that, or the camera cannot go on in week 3.**

### 8-1. Concurrent courses

| | Course | Why |
|---|---|---|
| Helpful if already taken | MCU Programming (year 2 fall), Signals and Linear Systems (year 2 fall) | Prior GPIO/I2C/UART experience and a feel for frequency puts you about three weeks ahead at the start |
| **Strongly recommended alongside** | **Embedded Systems (year 3 fall)** | It works with Raspberry Pi and Linux, which connects directly to the D3-G work here |
| Recommended alongside | Deep Learning (year 3 fall) | Meshes with the week 5 image processing and the week 8 and 11 dataset labs |

### 8-2. Self-study (starts in the Lecture 1 lab, done before Lecture 2)

In priority order. **Items 1 to 3 must be done before Lecture 2.**

1. **Python** — handling numpy arrays, plotting with matplotlib. Rather than memorizing syntax, get as far as "read some data and draw a picture of it" and that is enough.
2. **The Linux command line** — `cd` `ls` `apt` `ssh` `vim` (or nano), file permissions. You will be working over SSH on the board all semester.
3. **Git / GitHub** — `clone` `add` `commit` `push`, and what a branch is. This is where your lab notebook and code go.
4. **A taste of OpenCV** — read an image, convert to grayscale, run Canny. The first part of the official tutorial is enough.
5. **The ROS2 Humble tutorial** — only the nodes and topics part. If you have time.

### 8-3. Something to think about beforehand

In the Lecture 1 lab you **discuss roles (A: vision / B: ranging and localization) and settle them in Lecture 2**. It helps to have thought about which side pulls you, and why. If you want both, that is also a good answer — in the back half of the semester you will end up in each other's code anyway.

---

## 9. Where this leads after the course ends

- **Automotive Vision (year 4 spring) → Autonomous Driving (year 4 fall)**: the follow-on courses that process and fuse the sensor data you acquired here
- **The SEA:ME hackathon**: same D-Racer platform. Your semester result can be entered as it stands
- **Capstone design / graduation project**: extending this vehicle is the most natural next step
- **Portfolio**: one GitHub repository holding 15 weeks of lab notebooks and videos of the thing working

---

*Related documents: `01-교과목-방향-리서치.md` (design rationale, Korean) · `02-교보재-구매계획.md` (original equipment plan, Korean) · `03-강의계획서.md` (department syllabus, 20-student version, Korean) · `05-project-schedule.en.md` (session-by-session detail, Lecture 1 plan) · `04-프로젝트-운영계획.md` (Korean edition of this handout)*
