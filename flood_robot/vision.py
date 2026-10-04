from __future__ import annotations

from typing import List


def detect_flood_zones(water_level: float, threshold: float = 0.65) -> List[dict]:
    """Return flood regions based on water level."""
    if water_level < threshold:
        return []

    return [
        {"name": "Zone A", "center_x": 0.65, "center_y": 0.55, "severity": 0.9},
        {"name": "Zone B", "center_x": 0.8, "center_y": 0.7, "severity": 0.75},
    ]


def detect_human_presence(flood_zones: List[dict], water_level: float) -> List[dict]:
    """Simulate human detection in flood areas."""
    if not flood_zones or water_level < 0.5:
        return []

    return [
        {"location": "near Zone A", "risk": "high"},
        {"location": "near Zone B", "risk": "medium"},
    ]
