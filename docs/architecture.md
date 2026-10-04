# Flood Rescue Robot architecture

## System overview

The flood rescue robot is designed to support critical rescue operations in flood-prone areas. It combines mobility, sensing, AI-based detection, and visual reporting to assist human rescue teams.

## Main modules

### 1. Sensing layer

Responsible for collecting environmental and robot health data:
- water level sensor
- GPS position
- battery status
- camera feed
- optional LiDAR and thermal camera

### 2. Vision analysis

Used to detect flood zones and identify possible trapped people:
- flood segmentation
- object detection
- route hazard analysis

### 3. Navigation

Plans safe movement in unstable environments:
- obstacle avoidance
- path generation around dangerous areas
- prioritization of safe access routes

### 4. Reporting

Generates useful output for operators:
- flood risk map images
- rescue summary text
- emergency alert reports

### 5. Human operators

The robot does not replace rescuers. Instead, it supports them by:
- identifying safe points of access
- reducing uncertainty in dangerous areas
- generating visual communication material for command centers

## Example deployment

A robot may operate as follows:
- move into a flooded district
- scan camera feed and sensor values
- detect elevated water level and people in danger
- generate a flood map image with zones and safe route
- transmit summary to a rescue team

## Future enhancements

- ROS2 integration for real robot control
- real-time web dashboard
- YOLO-based person detection
- drone coordination
- GIS-based flood mapping

## Conclusion

The goal is to build a useful flood-ready robot that helps humans make faster, safer, and more informed rescue decisions during critical emergencies.
