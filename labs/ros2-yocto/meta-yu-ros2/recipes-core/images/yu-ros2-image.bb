require recipes-telechips-topst/images/telechips-topst-image.bb
SUMMARY = "YU D3-G ROS 2 Humble sensor classroom image"
inherit ros_distro_humble ros2_image
IMAGE_INSTALL:append = " ros-workspace ros-environment demo-nodes-cpp ros2cli ros2run ros2node ros2topic ros2param ros2interface ros2launch rmw-fastrtps-cpp v4l2-camera v4l-utils usbutils"
