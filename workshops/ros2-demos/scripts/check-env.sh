#!/bin/sh
# Read-only checks; does not start nodes, install software, or change networking.
case "${1:-}" in pc|d3) role=$1 ;; *) echo 'Usage: sh scripts/check-env.sh pc|d3' >&2; exit 2 ;; esac
fail=0
check() {
    if "$@" >/dev/null 2>&1; then printf 'OK    %s\n' "$*"
    else printf 'FAIL  %s\n' "$*"; fail=1; fi
}
printf 'Target=%s host=%s arch=%s\n' "$role" "$(hostname)" "$(uname -m)"
check command -v ros2
printf 'ROS_DISTRO=%s DOMAIN=%s RMW=%s LOCALHOST_ONLY=%s\n' "${ROS_DISTRO:-unset}" "${ROS_DOMAIN_ID:-unset}" "${RMW_IMPLEMENTATION:-unset}" "${ROS_LOCALHOST_ONLY:-unset}"
check test "${ROS_DISTRO:-}" = humble
check test "${RMW_IMPLEMENTATION:-}" = rmw_fastrtps_cpp
check test "${ROS_LOCALHOST_ONLY:-}" = 0
case "${ROS_DOMAIN_ID:-}" in ''|*[!0-9]*) echo 'FAIL  ROS_DOMAIN_ID missing/invalid'; fail=1 ;; *) check test "$ROS_DOMAIN_ID" -le 101 ;; esac
if command -v ros2 >/dev/null 2>&1; then
    check ros2 pkg prefix demo_nodes_cpp
    check ros2 pkg prefix rmw_fastrtps_cpp
    if [ "$role" = pc ]; then
        for pkg in turtlesim rqt_graph rqt_image_view ros2bag rosbag2_transport rosbag2_storage_default_plugins ros2service ros2action; do
            check ros2 pkg prefix "$pkg"
        done
        if [ -z "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]; then echo 'FAIL  No desktop display; use a terminal in the Ubuntu desktop'; fail=1; fi
        check command -v ssh
    else
        check ros2 pkg prefix v4l2_camera
        check command -v v4l2-ctl
        check command -v lsusb
    fi
fi
printf 'This checks prerequisites only, not DDS delivery or camera capture.\n'
exit "$fail"
