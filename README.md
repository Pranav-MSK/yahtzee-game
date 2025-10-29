# 🎲 Yahtzee Game (Python + Tkinter)

A modern, fully playable **Yahtzee** game built with Python and Tkinter.  
It features a polished GUI, interactive dice rolling, scorecard tracking for all 13 categories, and a clean, dark-themed interface — no external images required.

---

## 🕹️ Features

- ✅ **Full Yahtzee gameplay** — 13 rounds with all standard categories  
- 🎨 **Modern Tkinter UI** — clean dark theme with accent colors  
- 🎲 **Interactive Dice** — click to hold dice between rolls  
- 🧮 **Automatic Scoring** — detects and calculates valid combinations  
- 🧾 **Scorecard Panel** — track categories and total score  
- 💬 **In-Game Popup Rules** — scrollable, easy-to-read help window  
- 💡 **Simple & Lightweight** — no images or extra assets required  

---

## 🧠 How to Play

1. **Start the game** — read the short rules popup.  
2. **Each round**:
   - Roll five dice (up to three times per round).  
   - Click any dice to **hold** them between rolls.  
3. After rolling, **choose a scoring category** on the right-hand scorecard.  
4. Each category can be used only once (even if it scores zero).  
5. After 13 rounds, your **total score** is displayed — aim for the highest possible!

---

## 🏆 Scoring Highlights

| Category | Description | Points |
|-----------|--------------|---------|
| **Yahtzee** | Five of a kind | 50 |
| **Full House** | 3 of one + 2 of another | 25 |
| **Small Straight** | Four consecutive numbers | 30 |
| **Large Straight** | Five consecutive numbers | 40 |
| **Three / Four of a Kind** | Sum of all dice | — |
| **Upper Section (Ones–Sixes)** | Sum of chosen number | — |
| **Chance** | Any combination | Sum of dice |

---

## 🛠️ Installation

Make sure you have **Python 3.8+** installed.

```bash
# Clone the repository
git clone https://github.com/Pranav-MSK/yahtzee-game.git

# Navigate into the project folder
cd yahtzee-game

# Run the game
python yahtzee.py
```

No additional dependencies are required — Tkinter comes pre-installed with Python.

---

## 📁 Project Structure
```bash
yahtzee-game/
│
├── yahtzee.py    # Main game script
├── README.md     # Project documentation
└── LICENSE       # License file
```

--- 

## 🎨 Theme & Design
The interface uses a dark-themed color palette:
- Background panels in soft gray/black
- Accent colors for highlights and buttons
- Rounded dice buttons with hover feedback
- Scrollable rules popup window

All components are built with pure Tkinter widgets — no external graphics or dependencies.

---

## 🚀 Future Enhancements
- Add sound effects for dice rolls 🎵
- Save / load high scores 📊
- Add animations for rolling dice 🌀
- Implement multiplayer mode 👥

---

## 👨‍💻 Author
Pranav M S Krishnan
🔗 [GitHub Profile](https://github.com/Pranav-MSK)

---

## 📝 License
This project is released under the MIT License.
You are free to use, modify, and distribute it with attribution.