# Source in each terminal: . ./scripts/env.sh
# Set ROS_DOMAIN_ID to the instructor-assigned value before sourcing.
workshop_ros_env() {
    case "${ROS_DOMAIN_ID:-}" in
        ''|*[!0-9]*) echo 'Set ROS_DOMAIN_ID to your assigned integer (0..101) first.' >&2; return 1 ;;
    esac
    if [ "$ROS_DOMAIN_ID" -gt 101 ]; then
        echo 'This workshop uses domain IDs 0..101.' >&2; return 1
    fi
    if [ -r /opt/ros/humble/setup.sh ]; then
        . /opt/ros/humble/setup.sh || return 1
    elif [ -r /opt/ros/humble/local_setup.sh ]; then
        . /opt/ros/humble/local_setup.sh || return 1
    else
        echo 'ROS 2 Humble setup file missing. Ask the instructor to check the image.' >&2; return 1
    fi
    export ROS_DOMAIN_ID
    export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
    export ROS_LOCALHOST_ONLY=0
    printf 'ROS domain=%s middleware=%s localhost_only=%s\n' "$ROS_DOMAIN_ID" "$RMW_IMPLEMENTATION" "$ROS_LOCALHOST_ONLY"
}
workshop_ros_env
