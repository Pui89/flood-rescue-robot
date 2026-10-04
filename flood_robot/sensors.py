from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass
class SensorData:
    water_level: float
    gps: Tuple[float, float]
    battery: int


def read_water_level() -> float:
    """Simulate a water-level reading from a flood sensor."""
    return 0.82


def read_gps() -> Tuple[float, float]:
    """Simulate GPS coordinates for the rescue robot."""
    return (12.9716, 77.5946)
