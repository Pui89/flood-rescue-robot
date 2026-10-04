from __future__ import annotations

from typing import List, Tuple

from flood_robot.sensors import SensorData


def create_emergency_report(
    sensors: SensorData,
    flood_zones: List[dict],
    human_presence: List[dict],
    route: List[Tuple[float, float]],
    image_path: str,
) -> str:
    """Create a readable report for emergency operators."""
    lines = [
        "Emergency Flood Response Summary",
        "==============================",
        f"Water level: {sensors.water_level * 100:.0f}%",
        f"GPS: {sensors.gps}",
        f"Battery: {sensors.battery}%",
        f"Flood zones detected: {len(flood_zones)}",
        f"People detected: {len(human_presence)}",
        f"Suggested route points: {len(route)}",
        f"Report image: {image_path}",
    ]

    if human_presence:
        lines.append("Human presence status: High priority rescue area")
    else:
        lines.append("Human presence status: No confirmed person detected")

    return "\n".join(lines)
