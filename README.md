# 🏆 Checkers AI - Intelligent Game Player  

🔍 **Checkers AI** is a Python-based program that plays the game of **Checkers (Draughts)** as one of the players. The game is played on an **8×8 board** with **12 pieces per player**, following the standard checkers rules. The goal is to eliminate all opponent's pieces or block their possible moves.  

🤖 This project implements **AI-based decision-making**, using:  
- **Heuristic Evaluation** – Determines the best move based on piece positioning and game state.  
- **Variable Depth Search Engine** – Adjusts search depth dynamically for better performance.  
- **Minimax Algorithm** – Computes the best possible move considering all future possibilities.  
- **Alpha-Beta Pruning** – Optimizes Minimax by eliminating unnecessary calculations.  
- **Hash Map Optimization** – Reduces redundant computations and speeds up move selection.  

🎮 **Game Modes:**  
- **Standard Checkers Rules:** Pieces move diagonally and can jump over opponent pieces.  
- **Two Play Modes:** Choose whether capturing opponent pieces is **mandatory** or **optional**.  
- **King Promotion:** When a piece reaches the opponent's back row, it becomes a "king" and can move **both forward and backward**.  
- **Multi-Jump Sequences:** If a capture is possible, a piece can continue jumping over multiple opponent pieces in one turn.  
- **Console-Based Gameplay:** The game is played through the terminal, with a **graphical board representation** and move selection.  

⏳ **Performance:**  
- The AI must decide its move **within 5 seconds**.  
- For higher scores, the move must be computed in **less than 3 seconds**.  

---

📖 **This project was developed as part of the "Algorithms and Data Structures" course (2023/2024).**  

---

## 📚 Table of Contents  
- [🛠 Technologies & Specifications](#-technologies--specifications)  
- [🔧 Installing and Running the Project](#-installing-and-running-the-project)  
- [📖 How It Works](#-how-it-works)  
- [⚠️ Potential Issues & Troubleshooting](#-potential-issues--troubleshooting)  
- [📜 License](#-license)  
- [📬 Contact](#-contact)

---

## 🛠 Technologies & Specifications  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-orange?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20MacOS-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen)

### 📦 **Dependencies**  
The project relies on the following libraries and technologies:  

| Library      | Purpose |
|-------------|---------|
| `pygame`    | Used for rendering the game board and handling user interactions |
| `queue`     | Utilized for internal AI processing and state management |
| `time`      | Used for AI move timing and performance measurement |
| `json`      | Handles game configuration and move storage |
| `os`        | File system operations and handling saved games |

### 📥 **Install Dependencies**  
Before running the project, install the required dependencies using:  

```sh
pip install pygame
```

---

## 🔧 Installing and Running the Project  

### 📥 **1️⃣ Clone the Repository**  
First, download the project by cloning the repository:  

```sh
git clone https://github.com/MilanSazdov/checkers-ai.git
cd checkers-ai
```
### 📦 **2️⃣ Install Dependencies**  
Ensure you have all required dependencies installed:  

```sh
pip install pygame
```

### ▶️ **3️⃣ Run the Game**  
To start the checkers game, simply run the **board.py** script located inside the **checkers** folder:  

```sh
python checkers/board.py
```

---


