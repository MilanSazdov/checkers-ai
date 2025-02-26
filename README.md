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
