# Hand Gesture Controlled Space Shooter

A real-time hand gesture controlled space shooter game that combines computer vision with gaming. Control your spaceship using hand movements and shoot enemies by pinching your fingers together!

## 🎮 How It Works

This project consists of two main components:

1. **Hand Gesture Detection** (`hand_gesture.py`) - Uses your webcam to detect hand gestures and sends control data via UDP
2. **Space Shooter Game** (`space-theme/`) - A Godot-based space shooter that receives gesture data and responds in real-time

## 🚀 Features

### Hand Gesture Controls
- **Vertical Movement**: Move your hand up/down to control spaceship position
- **Shooting**: Pinch thumb and index finger together to shoot bullets
- **Real-time Feedback**: Visual indicators show hand position and shooting status
- **UDP Communication**: Low-latency data transmission to the game

### Game Features
- **Smooth Movement**: Interpolated spaceship movement for natural feel
- **Dynamic Enemies**: Randomly spawned enemies with varying sizes
- **Obstacles**: Avoid incoming obstacles while shooting enemies
- **Power-ups**: Collect items to restore health and ammunition
- **Progressive Difficulty**: Game speed increases over time
- **Audio Effects**: Sound effects and background music

## 📋 Requirements

### Python Dependencies
```
opencv-python
mediapipe
```

### Game Engine
- Godot 4.4 or later

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hand-gesture-space-shooter
   ```

2. **Install Python dependencies**
   ```bash
   pip install opencv-python mediapipe
   ```

3. **Open the game in Godot**
   - Launch Godot Engine
   - Import the `space-theme` project
   - Open `project.godot`

## 🎯 How to Play

1. **Start the hand gesture detection**
   ```bash
   python hand_gesture.py
   ```

2. **Launch the game**
   - Run the project in Godot
   - The game will automatically listen for UDP data on port 5005

3. **Control your spaceship**
   - Position your **right hand** in front of the camera
   - Move your hand **up/down** to control spaceship vertical position
   - **Pinch** thumb and index finger together to shoot
   - The gesture detection window shows your hand position and shooting status

## 🔧 Configuration

### Network Settings
Both components use UDP communication on:
- **IP**: 127.0.0.1 (localhost)
- **Port**: 5005

### Gesture Sensitivity
In `hand_gesture.py`, you can adjust:
- `PINCH_THRESHOLD`: Distance threshold for pinch detection (default: 20 pixels)
- `min_detection_confidence`: Hand detection confidence (default: 0.7)

### Game Settings
In the Godot project:
- `LERP_SPEED`: How smoothly the player moves (default: 10.0)
- Spawn rates for enemies, obstacles, and items can be adjusted in `main.gd`

## 🎮 Game Controls

| Gesture | Action |
|---------|--------|
| Hand Up/Down | Move spaceship vertically |
| Pinch Fingers | Shoot bullets |
| No Hand Detected | Spaceship stays in center |

## 📁 Project Structure

```
├── hand_gesture.py          # Hand gesture detection script
├── react/                   # Additional assets
├── space-theme/            # Godot game project
│   ├── scenes/            # Game scenes and scripts
│   │   ├── player.gd     # Player controller with UDP input
│   │   ├── main.gd       # Main game logic
│   │   ├── enemy.gd      # Enemy behavior
│   │   └── ...           # Other game components
│   ├── assets/           # Game assets (sprites, sounds)
│   └── project.godot     # Godot project configuration
└── README.md             # This file
```

## 🔍 Troubleshooting

### Common Issues

**Camera not working**
- Ensure your webcam is connected and not used by other applications
- Try changing the camera index in `cv2.VideoCapture(0)` to `1` or `2`

**Game not responding to gestures**
- Check that both applications are running
- Verify UDP port 5005 is not blocked by firewall
- Ensure hand gesture detection shows "SUCCESS: Listening for UDP packets"

**Hand detection issues**
- Ensure good lighting conditions
- Keep your hand clearly visible in the camera frame
- Use your right hand (appears as 'Left' in the mirrored view)

**Performance issues**
- Close other applications using the camera
- Reduce game window size in Godot
- Lower the hand detection confidence threshold

## 🎨 Customization

### Adding New Gestures
1. Modify `hand_gesture.py` to detect additional hand landmarks
2. Update the UDP data structure
3. Modify `player.gd` to handle new gesture data

### Game Modifications
- Edit scenes in Godot to change game mechanics
- Modify spawn rates and difficulty scaling in `main.gd`
- Add new enemy types or power-ups

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the project!

## 📄 License

This project is open source. Please check individual components for specific licensing terms.

---

**Enjoy controlling your spaceship with hand gestures! 🚀👋**