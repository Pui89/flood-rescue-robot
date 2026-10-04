# Human-Robot Interaction (HRI) System

Comprehensive system for the Flood Rescue Robot to interact intelligently with humans through vision, multimodal communication, predictive warnings, and autonomous actions.

## Overview

The HRI system enables the flood rescue robot to:
- **Perceive**: See and understand human presence, emotions, and intent
- **Communicate**: Speak, display, gesture, and alert in multiple modalities
- **Act**: Take autonomous actions to protect or assist humans
- **Warn**: Predict dangers and issue advance alerts
- **Adapt**: Learn human preferences and adjust behavior

---

## 1. Vision System (Human Perception)

### 1.1 Real-time Human Detection

**Technology**: YOLOv8 + skeleton pose estimation

```python
from ultralytics import YOLO
import cv2

class HumanDetector:
    def __init__(self):
        self.yolo = YOLO('yolov8n.pt')  # Nano model for speed
        self.pose_model = YOLO('yolov8n-pose.pt')
    
    def detect_humans(self, frame):
        """
        Returns: list of human detections with:
        - bounding box
        - confidence score
        - pose skeleton (keypoints)
        - estimated position (x, y, z in 3D)
        """
        results = self.yolo(frame, conf=0.4)
        poses = self.pose_model(frame)
        
        humans = []
        for result in results:
            if result.cls == 0:  # Person class
                human = {
                    'box': result.xyxy[0],
                    'confidence': result.conf[0],
                    'distance': self.estimate_distance(result),
                    'in_water': self.check_water_contact(result, frame),
                }
                humans.append(human)
        
        return humans
    
    def estimate_distance(self, detection):
        """Estimate distance to human using depth camera or size heuristics"""
        # Simplified: bounding box area correlates with distance
        box_area = detection.xyxy[0][2] * detection.xyxy[0][3]
        distance_m = 1000 / (box_area ** 0.5 + 1)  # Rough estimate
        return distance_m
    
    def check_water_contact(self, detection, frame):
        """Check if person is in water (color analysis)"""
        x1, y1, x2, y2 = detection.xyxy[0]
        roi = frame[int(y1):int(y2), int(x1):int(x2)]
        # Blue/water color dominance = in water
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        blue_mask = cv2.inRange(hsv, (100, 50, 50), (130, 255, 255))
        water_ratio = cv2.countNonZero(blue_mask) / blue_mask.size
        return water_ratio > 0.3
```

### 1.2 Emotion & Distress Detection

**Technology**: Facial expression analysis + body language

```python
import mediapipe as mp

class EmotionDetector:
    def __init__(self):
        self.face_detection = mp.solutions.face_detection.FaceDetection()
    
    def analyze_distress(self, frame, human_detection):
        """
        Returns distress level: 'calm', 'anxious', 'panicked', 'unknown'
        """
        x1, y1, x2, y2 = human_detection['box']
        face_roi = frame[int(y1):int(y2), int(x1):int(x2)]
        
        results = self.face_detection.process(face_roi)
        
        if not results.detections:
            return 'unknown', 0.0
        
        # Analyze face orientation and eye contact
        distress_score = 0.0
        
        # If looking down/away = lower confidence/anxiety
        # If mouth open = possibly calling for help
        # If rapid head movement = panic
        
        distress_level = 'calm' if distress_score < 0.3 else \
                        'anxious' if distress_score < 0.6 else \
                        'panicked'
        
        return distress_level, distress_score
    
    def analyze_body_language(self, poses):
        """
        Analyze pose keypoints for body language:
        - arms up = help needed
        - falling = emergency
        - still = disabled/injured
        """
        # Analyze skeleton keypoints
        signals = {
            'arms_raised': False,
            'falling': False,
            'immobile': False,
            'drowning': False,
        }
        
        # Logic here based on keypoint positions
        return signals
```

### 1.3 Situational Awareness

```python
class SituationAnalyzer:
    def analyze_scene(self, frame, humans, water_level):
        """
        Overall scene understanding:
        - safe zones
        - danger zones
        - priority humans
        - environmental hazards
        """
        situation = {
            'humans_in_danger': [],
            'humans_safe': [],
            'hazards': [],
            'safe_paths': [],
            'priority_score': {},
        }
        
        for human in humans:
            priority = self.calculate_priority(
                human['distress'],
                human['in_water'],
                human['distance'],
                water_level
            )
            
            if priority > 0.6:
                situation['humans_in_danger'].append(human)
            else:
                situation['humans_safe'].append(human)
            
            situation['priority_score'][human['id']] = priority
        
        return situation
    
    def calculate_priority(self, distress, in_water, distance, water_level):
        """Priority scoring: 0 (low) to 1 (critical)"""
        priority = 0.0
        priority += distress * 0.4  # Emotional state
        priority += (1.0 if in_water else 0.0) * 0.3  # In water?
        priority += (1.0 - min(distance / 50, 1.0)) * 0.2  # Proximity
        priority += (water_level * 0.1)  # Water level severity
        return min(priority, 1.0)
```

---

## 2. Multimodal Communication System

### 2.1 Audio Communication

```python
import pyttsx3
import speech_recognition as sr

class AudioCommunication:
    def __init__(self):
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 150)  # Speaking rate
        self.recognizer = sr.Recognizer()
    
    def speak(self, message, priority='normal'):
        """
        Speak to humans with different urgency levels
        priority: 'normal', 'urgent', 'critical'
        """
        if priority == 'critical':
            # Louder, faster, repeated
            self.tts.setProperty('volume', 1.0)
            self.tts.setProperty('rate', 200)
        else:
            self.tts.setProperty('volume', 0.8)
            self.tts.setProperty('rate', 150)
        
        self.tts.say(message)
        self.tts.runAndWait()
    
    def listen(self, timeout=5):
        """Listen for human voice commands"""
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=timeout)
                text = self.recognizer.recognize_google(audio)
                return text
        except Exception as e:
            return None
    
    def respond_to_human(self, detected_phrase):
        """Parse human speech and respond appropriately"""
        responses = {
            'help': 'Help is on the way. Stay calm.',
            'water': 'Measuring water level now.',
            'safe': 'Moving to safer location.',
            'direction': 'Which direction do you need help?',
        }
        
        for keyword, response in responses.items():
            if keyword in detected_phrase.lower():
                self.speak(response)
                return True
        
        return False
```

### 2.2 Visual Communication (Display & Gestures)

```python
import numpy as np
import time

class VisualCommunication:
    def __init__(self):
        self.led_colors = {
            'safe': (0, 255, 0),      # Green
            'warning': (255, 165, 0), # Orange
            'danger': (255, 0, 0),    # Red
            'searching': (0, 0, 255), # Blue
        }
    
    def signal_status(self, status):
        """
        Visual feedback via LED strips on robot
        """
        color = self.led_colors.get(status, (255, 255, 255))
        # Send color command to LED controller
        self.set_led_color(color)
    
    def strobe_emergency(self):
        """Rapid red flashing for emergency"""
        for _ in range(10):
            self.set_led_color((255, 0, 0))
            time.sleep(0.2)
            self.set_led_color((0, 0, 0))
            time.sleep(0.2)
    
    def point_to_location(self, target_x, target_y):
        """Move robot body/camera to point at location"""
        # Adjust robot heading toward target
        # Front camera lights up and points direction
        pass
    
    def display_message(self, message):
        """Show text/images on front LCD screen (if equipped)"""
        # Display on small screen mounted on robot
        pass
```

### 2.3 Gestural Communication

```python
class GesturalCommunication:
    def gesture_follow_me(self):
        """Blink lights and move forward to invite follow"""
        self.signal_status('searching')
        self.move_forward(0.5)  # Move 50cm
        self.rotate(45)  # Turn to show direction
    
    def gesture_stay_still(self):
        """Signal to stay in place (red steady light)"""
        self.signal_status('danger')
        self.sound_alert('steady')  # Steady beep
    
    def gesture_come_here(self):
        """Reverse direction and flash green"""
        self.signal_status('safe')
        self.move_backward(1.0)  # Back up to safety
    
    def gesture_emergency(self):
        """Full alert: lights, sound, and siren"""
        self.strobe_emergency()
        self.sound_siren()
```

---

## 3. Predictive Warning System

### 3.1 Hazard Prediction Engine

```python
import numpy as np
from datetime import datetime, timedelta

class HazardPredictor:
    def __init__(self):
        self.water_level_history = []
        self.human_position_history = {}
    
    def predict_water_rise(self, current_level, rate_of_change):
        """
        Predict water level in next 5-30 minutes
        Returns: list of (time, predicted_level) tuples
        """
        predictions = []
        current_time = datetime.now()
        
        # Simple linear extrapolation
        for minutes_ahead in [5, 10, 15, 30]:
            future_time = current_time + timedelta(minutes=minutes_ahead)
            predicted_level = current_level + (rate_of_change * minutes_ahead)
            predictions.append((future_time, predicted_level))
        
        return predictions
    
    def predict_danger_zone(self, water_predictions, terrain_map):
        """
        Predict which areas will be dangerous based on water rise
        """
        danger_zones = []
        for time, level in water_predictions:
            # Map water level to affected terrain areas
            affected = self.get_affected_areas(terrain_map, level)
            danger_zones.append({
                'time': time,
                'level': level,
                'areas': affected,
            })
        return danger_zones
    
    def predict_human_safety(self, human, water_predictions):
        """
        Warn if human will be in danger based on water rise prediction
        """
        human_elevation = human['current_position']['z']
        warnings = []
        
        for pred in water_predictions:
            if pred['level'] >= human_elevation - 0.2:  # 20cm safety margin
                warnings.append({
                    'time': pred['time'],
                    'severity': 'CRITICAL',
                    'message': f'Water will reach your area in {pred["time"]}',
                })
        
        return warnings
```

### 3.2 Early Warning System

```python
class EarlyWarningSystem:
    def __init__(self):
        self.warning_threshold = 0.7  # 0-1 scale
        self.issued_warnings = {}  # Avoid duplicate warnings
    
    def issue_warning(self, human, hazard_type, severity, time_to_impact):
        """
        Issue advance warning to human before danger strikes
        severity: 'low', 'medium', 'high', 'critical'
        time_to_impact: minutes until danger
        """
        warning_id = f"{human['id']}_{hazard_type}_{int(time.time())}"
        
        if warning_id in self.issued_warnings:
            return  # Don't repeat same warning
        
        self.issued_warnings[warning_id] = True
        
        # Multimodal alert
        if severity in ['high', 'critical']:
            # Visual alert
            self.strobe_emergency()
            
            # Audio alert
            message = f"WARNING: {hazard_type} approaching in {time_to_impact} minutes"
            self.speak(message, priority='critical')
            
            # Log for operators
            self.log_warning(human['id'], hazard_type, severity, time_to_impact)
    
    def issue_collective_warning(self, area_id, hazard_type):
        """Warn all humans in a specific area"""
        self.speak(
            f"ATTENTION: {hazard_type} detected in your area. "
            f"Move to higher ground immediately.",
            priority='critical'
        )
        self.strobe_emergency()
```

---

## 4. Autonomous Action System

### 4.1 Decision-Making (Behavioral Trees)

```python
class RobotBehavior:
    def __init__(self):
        self.state = 'idle'
    
    def run_behavior_tree(self, situation):
        """
        Main decision loop using behavior tree logic
        """
        if situation['humans_in_danger']:
            return self.rescue_behavior(situation)
        elif situation['hazards']:
            return self.warning_behavior(situation)
        else:
            return self.patrol_behavior()
    
    def rescue_behavior(self, situation):
        """
        Priority-based rescue approach
        1. Identify highest priority human
        2. Move toward them
        3. Establish communication
        4. Guide to safety
        """
        # Sort humans by priority
        priority_humans = sorted(
            situation['humans_in_danger'],
            key=lambda h: h['priority_score'],
            reverse=True
        )
        
        target = priority_humans[0]
        
        # Approach target
        self.navigate_to(target['position'])
        
        # Establish communication
        self.speak("Help is here. Follow me to safety.")
        
        # Guide along safe route
        safe_path = situation['safe_paths'][0]
        self.lead_along_path(target['id'], safe_path)
    
    def warning_behavior(self, situation):
        """
        Detect and warn about hazards
        """
        for hazard in situation['hazards']:
            if hazard['type'] == 'rising_water':
                self.issue_flood_warning(hazard)
            elif hazard['type'] == 'structural':
                self.issue_structural_warning(hazard)
            elif hazard['type'] == 'electrical':
                self.issue_electrical_warning(hazard)
    
    def patrol_behavior(self):
        """Scan area for dangers when idle"""
        self.rotate_camera_360()
        self.move_forward_slowly()
```

### 4.2 Safety Protocols

```python
class SafetyProtocol:
    def assess_interaction_safety(self, human, robot_action):
        """
        Before taking action, verify safety for human
        """
        safety_score = 1.0
        
        # Check if human is in stable position
        if not human['stable']:
            safety_score *= 0.5
        
        # Check if action might scare human
        if robot_action == 'approach' and human['distress'] == 'panicked':
            # Approach more slowly
            safety_score *= 0.7
        
        # Check for obstacles
        if self.path_has_hazards(robot_action['path']):
            safety_score *= 0.6
        
        return safety_score > 0.6  # Safe if > 60% confidence
    
    def emergency_stop(self, reason):
        """Immediate halt for safety"""
        self.stop_motors()
        self.set_led_color((255, 0, 0))  # Red
        self.speak(f"Emergency stop: {reason}", priority='critical')
        self.log_emergency(reason)
```

---

## 5. Alert Types and Responses

| Alert Type | Trigger | Visual | Audio | Action |
|---|---|---|---|---|
| **Immediate Danger** | Human in water, structural failure | Red strobe | Siren + voice warning | Move to human, guide away |
| **Water Rising** | Level increase > 10cm/min | Orange flash | Repeating beep + "evacuate area" | Point toward safe zone |
| **Human Distress** | Panicked face/body | Red steady | "Help coming" message | Approach slowly with reassurance |
| **Safe Route Found** | Path to safety identified | Green arrow | Chime + "this way" | Lead along path with lights |
| **Structural Hazard** | Debris detected overhead | Yellow flash | Warning tone | Back away, warn of hazard |
| **Low Battery** | Battery < 15% | Blue blink | Alert tone | Return to charging station |
| **Lost Connection** | Comms timeout | Purple flash | Beep sequence | Auto-return home |

---

## 6. Complete HRI Integration Example

```python
class HumanRobotInteractionSystem:
    def __init__(self):
        self.human_detector = HumanDetector()
        self.emotion_detector = EmotionDetector()
        self.situation_analyzer = SituationAnalyzer()
        self.audio_comm = AudioCommunication()
        self.visual_comm = VisualCommunication()
        self.hazard_predictor = HazardPredictor()
        self.warning_system = EarlyWarningSystem()
        self.robot_behavior = RobotBehavior()
        self.safety_protocol = SafetyProtocol()
    
    def hri_cycle(self, frame, sensor_data):
        """
        Main HRI loop: Perceive → Analyze → Warn → Act
        """
        # 1. PERCEIVE: Detect humans
        humans = self.human_detector.detect_humans(frame)
        
        for human in humans:
            # Detect emotion/distress
            distress, score = self.emotion_detector.analyze_distress(
                frame, human
            )
            human['distress'] = distress
            human['distress_score'] = score
        
        # 2. ANALYZE: Understand situation
        situation = self.situation_analyzer.analyze_scene(
            frame, humans, sensor_data['water_level']
        )
        
        # 3. WARN: Predict hazards and issue warnings
        water_predictions = self.hazard_predictor.predict_water_rise(
            sensor_data['water_level'],
            sensor_data['water_rise_rate']
        )
        
        for human in situation['humans_in_danger']:
            warnings = self.hazard_predictor.predict_human_safety(
                human, water_predictions
            )
            for warning in warnings:
                self.warning_system.issue_warning(
                    human,
                    'flood',
                    warning['severity'],
                    warning['time']
                )
        
        # 4. ACT: Take autonomous actions
        action = self.robot_behavior.run_behavior_tree(situation)
        
        # 5. SAFETY CHECK: Verify action is safe
        if self.safety_protocol.assess_interaction_safety(humans[0], action):
            self.execute_action(action)
        else:
            self.safety_protocol.emergency_stop("Action unsafe for human")
        
        # 6. COMMUNICATE: Provide feedback
        self.provide_feedback(situation, action)
    
    def provide_feedback(self, situation, action):
        """Communicate status to humans"""
        if situation['humans_in_danger']:
            self.visual_comm.signal_status('danger')
            self.audio_comm.speak(
                "Rescue team alerted. Stay calm.",
                priority='urgent'
            )
        else:
            self.visual_comm.signal_status('safe')


# Run the HRI system
if __name__ == "__main__":
    hri = HumanRobotInteractionSystem()
    
    while True:
        frame = camera.read()  # Get camera frame
        sensor_data = sensors.read()  # Get sensor readings
        
        hri.hri_cycle(frame, sensor_data)
```

---

## 7. Advanced Capabilities

### Swarm Communication
```python
# Multiple robots coordinating
def swarm_alert_humans(area_id, hazard_type):
    """
    All robots in area issue same warning for redundancy
    """
    robots = get_robots_in_area(area_id)
    for robot in robots:
        robot.speak(f"ALERT: {hazard_type}. Evacuate immediately.")
```

### Adaptive Learning
```python
# Robot learns individual human preferences
def adapt_to_human(human_id, interaction_history):
    """
    Adjust communication style based on past interactions
    """
    if human_prefers_calm_voice:
        tts_rate = 120  # Slower
    elif human_prefers_direct_commands:
        use_imperative = True
```

---

**Status**: Complete HRI specification ready for implementation in robot firmware.
