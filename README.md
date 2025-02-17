# Hand-Controlled Flappy Bird with OpenCV

A unique twist on the classic Flappy Bird game where players control the bird using hand gestures captured through their webcam. The game features real-time hand tracking, player statistics, and a high score system.

## 🎮 Features

- **Hand Gesture Control**: Control the bird's movement naturally with your hand movements
- **Real-time Skeleton Tracking**: Watch your hand movements represented by a skeleton overlay
- **Progressive Difficulty**: Game speed increases over time for an added challenge
- **High Score System**: Top 5 players' scores are saved and displayed
- **Player Recognition**: Enter your name before playing to track your achievements
- **Reaction Capture**: Automatically captures your reaction when the game ends

## 🛠️ Prerequisites

- Python 3.x
- OpenCV
- NumPy
- MediaPipe (for hand tracking)

## 📥 Installation

1. Clone the repository:
```bash
git clone https://github.com/Creative-banda/Flappy_Bird.git
cd Flappy_Bird
```


## 🎯 How to Play

1. Run the game:
```bash
python main.py
```

2. Enter your name when prompted at the intro screen
3. Position yourself in front of the webcam
4. Control the bird by moving your hand:
   - Move your hand up to make the bird fly higher
   - Move your hand down to make the bird descend
5. Try to avoid the pipes and survive as long as possible
6. Your reaction will be captured when the game ends

## 🎛️ Controls

- **Hand Up**: Bird flies upward
- **Hand Down**: Bird descends
- **ESC**: Exit game
- **R**: Restart game after death

## 🏆 High Score System

- The game maintains a leaderboard of the top 5 players
- Scores are automatically saved when you beat a previous high score
- High scores are displayed on the intro screen


## 🔧 Technical Implementation

- Hand tracking implemented using OpenCV and MediaPipe
- Real-time skeleton visualization for hand movement feedback
- Dynamic difficulty scaling based on gameplay duration
- Local storage system for maintaining high scores
- Webcam integration for player interaction and reaction capture

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Original Flappy Bird game by Dong Nguyen
- OpenCV community for computer vision tools
- MediaPipe team for hand tracking implementation
