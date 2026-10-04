from __future__ import annotations

from typing import List, Tuple


def plan_safe_route(
    current_location: Tuple[float, float],
    flood_zones: List[dict],
) -> List[Tuple[float, float]]:
    """Return a simple safe route around flooded areas."""
    if not flood_zones:
        return [current_location, (current_location[0] + 0.002, current_location[1] + 0.002)]

    route = [current_location]
    for zone in flood_zones:
        route.append((zone["center_x"], zone["center_y"]))
    route.append((current_location[0] + 0.003, current_location[1] + 0.003))
    return route
