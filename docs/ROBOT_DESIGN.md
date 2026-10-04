# Flood Rescue Robot - Design & Concept

## Robot Overview

The Flood Rescue Robot is a specialized emergency-response platform designed to operate in dangerous flooded environments. This document describes the physical design, sensors, and capabilities.

## Robot Physical Design

### Main chassis
- **Type**: 4-wheel all-terrain rover
- **Wheelbase**: 600mm
- **Width**: 480mm
- **Height**: 580mm (with antenna)
- **Weight**: 45kg (dry)
- **Material**: Waterproof composite shell + reinforced steel frame
- **Waterproof rating**: IP67 (can be submerged up to 1m for 30 minutes)
- **Tires**: 14-inch all-terrain tires with deep treads for mud and water

### Motor & Drive System
- **Propulsion**: 4 independent brushless motors (150W each)
- **Max speed**: 2.5 m/s on flat terrain
- **Max climb**: 45° inclines
- **Power**: LiPo battery 48V 20Ah (960Wh)
- **Runtime**: 3-4 hours at 50% load
- **Backup battery**: Onboard 12V emergency power for communications

### Color Scheme
- **Primary**: Bright Yellow (#F7C948) - high visibility in water and debris
- **Secondary**: Black (#1F2D3D) - contrast for sensor mounts
- **Accents**: Emergency Red (#FF4D4D) - warning lights and status indicators
- **Antenna**: Silver (#3F3F3F) - communication

## Sensor Package

### Primary Sensors
1. **Front Camera** (center mount)
   - 4K resolution at 30fps
   - 120° wide-angle lens
   - Night vision IR LEDs
   - Waterproof enclosure

2. **Water Depth Sensor** (bottom front)
   - Ultrasonic water level measurement
   - Range: 0-5 meters
   - Accuracy: ±5cm
   - Real-time flood depth analysis

3. **LiDAR System** (top mounted)
   - 360° scanning
   - Range: 0-40 meters
   - Resolution: 0.25°
   - Obstacle detection and mapping

4. **GPS + IMU** (roof antenna)
   - Real-time position tracking
   - Accuracy: ±2 meters
   - 9-axis IMU for tilt and orientation
   - Compass for heading

5. **Thermal Camera** (optional, right side)
   - 160×120 thermal resolution
   - Long-wave IR (8-14 μm)
   - Detects body heat of trapped survivors
   - Temperature range: -20°C to +120°C

### Secondary Sensors
- Temperature & humidity monitor
- Battery voltage and current monitor
- Motor encoder feedback (wheel rotation)
- Microphone for audio alerts

## Emergency Systems

### Lighting
- **Front LED bars**: Two high-intensity white LEDs (1000 lm each)
- **Warning lights**: Four red strobes on corners
- **Status indicator**: RGB LED on roof for quick status

### Audio
- Onboard siren (120dB)
- Speaker system for voice commands
- Backup horn for alerts

### Communication
- Primary: LTE/4G modem (if available)
- Secondary: LoRa radio (long-range backup)
- Tertiary: WiFi hotspot for local connectivity
- Failsafe: Automatic return-home on signal loss

## Operational Features

### Autonomous Capabilities
- Auto-mapping of flooded terrain
- Obstacle detection and avoidance
- Human detection in water/debris
- Safe route planning
- Automatic return-home on low battery
- Emergency stop override

### Manual Control
- Remote control operation via WiFi or radio
- Live video feed to operator
- Real-time sensor data streaming
- Emergency manual override

### Rescue-Specific Features
- Tow hook for pulling small objects (100kg capacity)
- Strobe lights for visibility in poor conditions
- Waterproof speaker for communication with trapped people
- Flotation rings for emergency buoyancy
- First-aid kit storage compartment

## Performance Specifications

| Spec | Value |
|------|-------|
| Max Speed | 2.5 m/s |
| Max Climb | 45° |
| Water Ford Depth | 1.2 m |
| Operating Temperature | -10°C to +50°C |
| Sensor Visibility | 120° forward + 360° LiDAR |
| Communication Range | 5km (WiFi), 15km (LoRa) |
| Battery Runtime | 3-4 hours |
| Max Payload | 15kg (external) |

## Deployment Scenarios

### Urban Flooding
- Navigate through submerged streets
- Identify trapped individuals in buildings
- Map water depth and flow patterns
- Generate evacuation routes

### Rural/Agricultural Flooding
- Cross flooded fields and dams
- Search for missing livestock and people
- Monitor water breach points
- Track flood spread

### Disaster Assessment
- Survey structural damage
- Locate hazards (broken power lines, gas leaks)
- Generate before/after comparison maps
- Support insurance and emergency planning

## Integration with Rescue Operations

The robot is designed to **support, not replace** human rescue teams:

1. **Scout Phase**: Robot surveys area ahead of rescue teams
2. **Mapping Phase**: Generates detailed flood maps and hazard zones
3. **Communication Phase**: Provides real-time data to command center
4. **Rescue Phase**: Guides human teams to safest routes and survivors

## Future Enhancements

- Autonomous 3D scanning for detailed maps
- Drone integration for aerial view
- Robotic arm for small object manipulation
- Modular payload system for specialized sensors
- AI-powered decision making
- Swarm capability (multiple robots coordinating)

## Concept Art

See `assets/flood_robot.svg` for visual concept of the robot in a flooded urban environment.

---

**Status**: Design prototype - Ready for ROS2 integration and real hardware testing
