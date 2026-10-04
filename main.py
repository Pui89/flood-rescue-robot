from flood_robot.config import DEFAULT_FLOOD_THRESHOLD
from flood_robot.image_generation import generate_flood_map
from flood_robot.navigation import plan_safe_route
from flood_robot.reporting import create_emergency_report
from flood_robot.sensors import SensorData, read_gps, read_water_level
from flood_robot.vision import detect_flood_zones, detect_human_presence


def run_demo() -> None:
    """Run a short flood-rescue simulation."""
    gps = read_gps()
    water_level = read_water_level()
    sensors = SensorData(
        water_level=water_level,
        gps=gps,
        battery=78,
    )

    flood_zones = detect_flood_zones(
        water_level=sensors.water_level,
        threshold=DEFAULT_FLOOD_THRESHOLD,
    )
    human_presence = detect_human_presence(
        flood_zones=flood_zones,
        water_level=sensors.water_level,
    )

    route = plan_safe_route(
        current_location=sensors.gps,
        flood_zones=flood_zones,
    )

    image_path = generate_flood_map(
        water_level=sensors.water_level,
        safe_route=route,
        flood_zones=flood_zones,
        output_path="outputs/flood_map.png",
    )

    summary = create_emergency_report(
        sensors=sensors,
        flood_zones=flood_zones,
        human_presence=human_presence,
        route=route,
        image_path=image_path,
    )

    print("\nFlood Rescue Robot Demo")
    print("=" * 40)
    print(summary)
    print(f"Generated image: {image_path}")


if __name__ == "__main__":
    run_demo()
