from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

from flood_robot.config import OUTPUTS_DIR


def generate_flood_map(
    water_level: float,
    safe_route: List[Tuple[float, float]],
    flood_zones: List[dict],
    output_path: str = "outputs/flood_map.png",
) -> str:
    """Create a visual flood map using Pillow."""
    OUTPUTS_DIR.mkdir(exist_ok=True)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    width, height = 1200, 800
    image = Image.new("RGB", (width, height), color=(230, 239, 250))
    draw = ImageDraw.Draw(image)

    # Terrain background
    draw.rectangle((0, 560, width, height), fill=(118, 146, 173))

    # Flood area
    draw.ellipse((150, 150, 1050, 650), fill=(76, 140, 220), outline=(35, 90, 170), width=4)

    # Flood risk overlay
    risk_alpha = int(80 + water_level * 120)
    for zone in flood_zones:
        cx = int(zone["center_x"] * width)
        cy = int(zone["center_y"] * height)
        radius = 110 + int(zone["severity"] * 100)
        overlay = Image.new("RGBA", (width, height), (255, 120, 80, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(255, 120, 80, risk_alpha))
        image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")

    # Safe route overlay
    if safe_route:
        points = []
        for lat, lon in safe_route:
            x = 200 + int(lat * 600)
            y = 650 - int(lon * 350)
            points.append((x, y))
        if len(points) > 1:
            draw.line(points, fill=(40, 180, 100), width=10)

    # Labels
    title_font = ImageFont.load_default()
    draw.text((50, 40), "Flood Risk Map", fill=(20, 20, 20), font=title_font)
    draw.text((50, 680), f"Water level: {water_level * 100:.0f}%", fill=(20, 20, 20), font=title_font)

    image.save(path)
    return str(path)
