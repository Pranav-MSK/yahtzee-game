import tkinter as tk
from tkinter import messagebox
import random

class Yahtzee:
    UPPER_CATEGORIES = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]
    LOWER_CATEGORIES = ["Three of a Kind", "Four of a Kind", "Full House","Small Straight", "Large Straight", "Yahtzee", "Chance"]

    def __init__(self, root):
        self.root = root
        self.root.title("Yahtzee")
        
        # Game state
        self.dice = [0] * 5
        self.hold_flags = [False] * 5
        self.roll_count = 0
        self.round = 0
        self.scores = {cat: None for cat in self.UPPER_CATEGORIES + self.LOWER_CATEGORIES}

        # GUI
        self.create_widgets()
        self.update_dice_display()
        self.update_scorecard_display()

    # -------------------- GUI --------------------
    def create_widgets(self):
        # Dice buttons
        self.dice_buttons = []
        dice_frame = tk.Frame(self.root)
        dice_frame.pack(pady=10)
        for i in range(5):
            btn = tk.Button(dice_frame, text="🎲", font=("Arial", 24), width=3,
                            command=lambda i=i: self.toggle_hold(i))
            btn.grid(row=0, column=i, padx=5)
            self.dice_buttons.append(btn)

        # Roll button
        self.roll_button = tk.Button(self.root, text="Roll Dice", font=("Arial", 14),
                                     command=self.roll_dice)
        self.roll_button.pack(pady=10)

        # Info
        self.info_label = tk.Label(self.root, text="Round 1, Rolls: 0/3", font=("Arial", 12))
        self.info_label.pack()

        # Scorecard
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(pady=10)
        self.score_buttons = {}
        for i, cat in enumerate(self.UPPER_CATEGORIES + self.LOWER_CATEGORIES):
            btn = tk.Button(self.score_frame, text=f"{cat}: ", width=20,
                            command=lambda c=cat: self.choose_category(c))
            btn.grid(row=i, column=0, pady=2)
            self.score_buttons[cat] = btn

        # Total score
        self.total_label = tk.Label(self.root, text="Total Score: 0", font=("Arial", 14, "bold"))
        self.total_label.pack(pady=10)

        # New game button
        self.reset_button = tk.Button(self.root, text="New Game", font=("Arial", 12),
                                      command=self.reset_game)
        self.reset_button.pack(pady=5)

    # -------------------- Dice Logic --------------------
    def toggle_hold(self, index):
        if self.roll_count == 0:
            return
        self.hold_flags[index] = not self.hold_flags[index]
        self.update_dice_display()

    def roll_dice(self):
        if self.roll_count >= 3:
            messagebox.showinfo("No Rolls Left", "You have rolled 3 times!")
            return
        for i in range(5):
            if not self.hold_flags[i]:
                self.dice[i] = random.randint(1, 6)
        self.roll_count += 1
        self.update_dice_display()
        self.info_label.config(text=f"Round {self.round+1}, Rolls: {self.roll_count}/3")

    def update_dice_display(self):
        for i, btn in enumerate(self.dice_buttons):
            value = self.dice[i]
            text = str(value) if value != 0 else "🎲"
            btn.config(text=text, bg="#ffd966" if self.hold_flags[i] else "SystemButtonFace")

    # -------------------- Scoring Logic --------------------
    def choose_category(self, category):
        if self.scores[category] is not None:
            messagebox.showinfo("Category Used", f"{category} already used!")
            return
        score = self.calculate_score(category)
        self.scores[category] = score
        self.update_scorecard_display()
        self.next_round()

    def calculate_score(self, category):
        counts = {i: self.dice.count(i) for i in range(1, 7)}
        total = sum(self.dice)

        # Upper Section
        if category in self.UPPER_CATEGORIES:
            number = self.UPPER_CATEGORIES.index(category) + 1
            return counts[number] * number

        # Lower Section
        if category == "Three of a Kind":
            return total if max(counts.values()) >= 3 else 0
        if category == "Four of a Kind":
            return total if max(counts.values()) >= 4 else 0
        if category == "Full House":
            return 25 if sorted(counts.values())[-2:] == [2,3] or (3 in counts.values() and 2 in counts.values()) else 0
        if category == "Small Straight":
            straights = [{1,2,3,4},{2,3,4,5},{3,4,5,6}]
            dice_set = set(self.dice)
            return 30 if any(straight.issubset(dice_set) for straight in straights) else 0
        if category == "Large Straight":
            return 40 if set(self.dice) in [{1,2,3,4,5},{2,3,4,5,6}] else 0
        if category == "Yahtzee":
            return 50 if max(counts.values()) == 5 else 0
        if category == "Chance":
            return total
        return 0

    # -------------------- Scorecard & Rounds --------------------
    def update_scorecard_display(self):
        for cat, btn in self.score_buttons.items():
            score = self.scores[cat]
            btn.config(text=f"{cat}: {'-' if score is None else score}",
                       state=tk.DISABLED if score is not None else tk.NORMAL)
        total = sum(s for s in self.scores.values() if s is not None)
        self.total_label.config(text=f"Total Score: {total}")

    def next_round(self):
        self.round += 1
        if self.round >= 13:
            messagebox.showinfo("Game Over", f"Game Over! Final Score: {sum(s for s in self.scores.values() if s is not None)}")
            self.roll_button.config(state=tk.DISABLED)
        else:
            self.roll_count = 0
            self.hold_flags = [False]*5
            self.dice = [0]*5
            self.update_dice_display()
            self.info_label.config(text=f"Round {self.round+1}, Rolls: 0/3")
            self.roll_button.config(state=tk.NORMAL)

    # -------------------- Reset --------------------
    def reset_game(self):
        self.dice = [0]*5
        self.hold_flags = [False]*5
        self.roll_count = 0
        self.round = 0
        self.scores = {cat: None for cat in self.UPPER_CATEGORIES + self.LOWER_CATEGORIES}
        self.roll_button.config(state=tk.NORMAL)
        self.update_dice_display()
        self.update_scorecard_display()
        self.info_label.config(text="Round 1, Rolls: 0/3")

# -------------------- Run --------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = Yahtzee(root)
    root.mainloop()
