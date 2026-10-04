# Flood Rescue Robot

A practical emergency-response robot project for flood monitoring, rescue assistance, and image-based reporting.

This repository is designed as a starter project for:
- flood detection and risk assessment
- human detection in flooded areas
- safe route planning for rescue teams
- image generation for flood maps and alerts
- emergency reporting dashboards

## What the robot can do

- Detect rising water levels and flood hotspots
- Identify people or obstacles in unsafe terrain
- Estimate safe vs unsafe routes
- Generate visual flood-risk maps
- Log emergency events and produce visual reports
- Send alerts to rescue operators

## Project structure

```text
flood-rescue-robot/
├── README.md
├── requirements.txt
├── main.py
├── flood_robot/
│   ├── __init__.py
│   ├── config.py
│   ├── sensors.py
│   ├── navigation.py
│   ├── vision.py
│   ├── image_generation.py
│   └── reporting.py
├── assets/
│   └── flood_robot.svg
└── docs/
    └── architecture.md
```

## Tech stack

- Python
- OpenCV
- Pillow
- Matplotlib
- Simple sensor abstraction for robotics and flood systems
- SVG concept art for the robot

## Quick start

1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the demo

```bash
python main.py
```

This will generate a sample flood-risk image and print an emergency report summary.

## Example output

The project generates a visual flood map like this:

- `outputs/flood_map.png`

It also creates a text-based emergency summary for operators.

## Architecture overview

The system is split into a few clear modules:

- sensors: reads flood, battery, and location data
- vision: identifies danger zones and human presence
- navigation: plans safe rescue routes
- image_generation: produces risk maps and reports
- reporting: packages output for human operators

## Robot concept

An example concept image is included in the repository:

- `assets/flood_robot.svg`

## Future improvements

- integrate with ROS2 for hardware control
- connect to real LiDAR, camera, GPS, and water sensors
- add YOLO-based object detection
- link to a web dashboard
- support drone-assisted flood surveys
- add real emergency SMS or radio alerting

## License

MIT

## Repository status

This repo is a working starter project for a flood-response robot to help humans during critical flood situations.
