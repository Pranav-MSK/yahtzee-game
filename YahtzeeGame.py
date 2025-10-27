import tkinter as tk
from tkinter import messagebox
import random

class Yahtzee:
    UPPER_CATEGORIES = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]
    LOWER_CATEGORIES = ["Three of a Kind", "Four of a Kind", "Full House", "Small Straight", "Large Straight", "Yahtzee", "Chance"]

    def __init__(self, root):
        self.root = root
        self.root.title("🎲 Yahtzee Mini Game")

        # Color theme
        self.bg_main = "#1e1e2f"
        self.bg_panel = "#292943"
        self.accent = "#ffcc66"
        self.text_light = "#ffffff"
        self.text_dim = "#cccccc"

        self.root.configure(bg=self.bg_main)
        
        # Game state
        self.dice = [0] * 5
        self.hold_flags = [False] * 5
        self.roll_count = 0
        self.round = 0
        self.scores = {cat: None for cat in self.UPPER_CATEGORIES + self.LOWER_CATEGORIES}

        # Create interface
        self.create_layout()
        self.update_dice_display()
        self.update_scorecard_display()
        self.show_rules_popup()

    # ---------------- GUI LAYOUT ----------------
    def create_layout(self):
        # Title
        title = tk.Label(self.root, text="YAHTZEE MINI GAME", font=("Arial Black", 22), bg=self.bg_main, fg=self.accent)
        title.pack(pady=10)

        # Top container (dice + roll area)
        top_frame = tk.Frame(self.root, bg=self.bg_main)
        top_frame.pack(pady=10)

        # Dice buttons
        self.dice_buttons = []
        dice_frame = tk.Frame(top_frame, bg=self.bg_main)
        dice_frame.pack()
        for i in range(5):
            btn = tk.Button(dice_frame, text="🎲", font=("Arial", 28, "bold"), width=3, height=1,
                            bg=self.bg_panel, fg=self.text_light,
                            activebackground=self.accent, relief="raised",
                            command=lambda i=i: self.toggle_hold(i))
            btn.grid(row=0, column=i, padx=8)
            self.dice_buttons.append(btn)

        # Roll & info area
        control_frame = tk.Frame(top_frame, bg=self.bg_main)
        control_frame.pack(pady=10)
        self.roll_button = tk.Button(control_frame, text="ROLL DICE 🎲", font=("Arial", 14, "bold"),
                                     bg=self.accent, fg="black", padx=20, pady=5,
                                     relief="flat", command=self.roll_dice)
        self.roll_button.pack()

        self.info_label = tk.Label(control_frame, text="Round 1 — Rolls: 0/3", 
                                   font=("Arial", 12), bg=self.bg_main, fg=self.text_dim)
        self.info_label.pack(pady=5)

        # Scorecard section
        scorecard_frame = tk.Frame(self.root, bg=self.bg_panel, bd=2, relief="ridge")
        scorecard_frame.pack(pady=15, fill="x", padx=20)

        header = tk.Label(scorecard_frame, text="SCORECARD", font=("Arial Black", 16),
                          bg=self.bg_panel, fg=self.accent)
        header.pack(pady=5)

        self.score_frame = tk.Frame(scorecard_frame, bg=self.bg_panel)
        self.score_frame.pack(pady=5)
        self.score_buttons = {}
        for i, cat in enumerate(self.UPPER_CATEGORIES + self.LOWER_CATEGORIES):
            btn = tk.Button(self.score_frame, text=f"{cat}: —", font=("Arial", 12),
                            bg=self.bg_panel, fg=self.text_light, width=25,
                            relief="flat", anchor="w",
                            activebackground="#403c64",
                            command=lambda c=cat: self.choose_category(c))
            btn.grid(row=i, column=0, sticky="w", pady=2)
            self.score_buttons[cat] = btn

        # Total
        self.total_label = tk.Label(scorecard_frame, text="Total Score: 0", font=("Arial Black", 14), bg=self.bg_panel, fg=self.accent)
        self.total_label.pack(pady=5)

        # Reset
        self.reset_button = tk.Button(self.root, text="NEW GAME", font=("Arial", 12, "bold"),
                                      bg="#66cc99", fg="black", padx=10, pady=5,
                                      command=self.reset_game)
        self.reset_button.pack(pady=5)

    # ---------------- DICE LOGIC ----------------
    def toggle_hold(self, index):
        if self.roll_count == 0:
            return
        self.hold_flags[index] = not self.hold_flags[index]
        self.update_dice_display()

    def roll_dice(self):
        if self.roll_count >= 3:
            messagebox.showinfo("No Rolls Left", "You’ve already rolled 3 times!")
            return
        for i in range(5):
            if not self.hold_flags[i]:
                self.dice[i] = random.randint(1, 6)
        self.roll_count += 1
        self.update_dice_display()
        self.info_label.config(text=f"Round {self.round+1} — Rolls: {self.roll_count}/3")

    def update_dice_display(self):
        for i, btn in enumerate(self.dice_buttons):
            value = self.dice[i]
            text = str(value) if value != 0 else "🎲"
            color = "#ffd966" if self.hold_flags[i] else self.bg_panel
            btn.config(text=text, bg=color, fg="black" if self.hold_flags[i] else self.text_light)

    # ---------------- SCORING ----------------
    def choose_category(self, category):
        if self.roll_count == 0:
            messagebox.showinfo("No Roll Yet", "Roll the dice before choosing a category.")
            return
        if self.scores[category] is not None:
            messagebox.showinfo("Used", f"You already used '{category}'.")
            return
        score = self.calculate_score(category)
        self.scores[category] = score
        self.update_scorecard_display()
        self.next_round()

    def calculate_score(self, category):
        counts = {i: self.dice.count(i) for i in range(1, 7)}
        total = sum(self.dice)

        # Upper section
        if category in self.UPPER_CATEGORIES:
            n = self.UPPER_CATEGORIES.index(category) + 1
            return counts[n] * n

        # Lower section
        if category == "Three of a Kind":
            return total if max(counts.values()) >= 3 else 0
        if category == "Four of a Kind":
            return total if max(counts.values()) >= 4 else 0
        if category == "Full House":
            return 25 if 3 in counts.values() and 2 in counts.values() else 0
        if category == "Small Straight":
            straights = [{1,2,3,4}, {2,3,4,5}, {3,4,5,6}]
            return 30 if any(s.issubset(set(self.dice)) for s in straights) else 0
        if category == "Large Straight":
            return 40 if set(self.dice) in [{1,2,3,4,5}, {2,3,4,5,6}] else 0
        if category == "Yahtzee":
            return 50 if max(counts.values()) == 5 else 0
        if category == "Chance":
            return total
        return 0

    # ---------------- SCORECARD ----------------
    def update_scorecard_display(self):
        for cat, btn in self.score_buttons.items():
            score = self.scores[cat]
            btn.config(text=f"{cat}: {'—' if score is None else score}",
                       state=tk.DISABLED if score is not None else tk.NORMAL)
        total = sum(s for s in self.scores.values() if s is not None)
        self.total_label.config(text=f"Total Score: {total}")

    def next_round(self):
        self.round += 1
        if self.round >= 13:
            total = sum(s for s in self.scores.values() if s is not None)
            messagebox.showinfo("Game Over", f"🎉 Game Over!\nYour final score: {total}")
            self.roll_button.config(state=tk.DISABLED)
        else:
            self.roll_count = 0
            self.hold_flags = [False]*5
            self.dice = [0]*5
            self.update_dice_display()
            self.info_label.config(text=f"Round {self.round+1} — Rolls: 0/3")
            self.roll_button.config(state=tk.NORMAL)

    # ---------------- RESET ----------------
    def reset_game(self):
        self.dice = [0]*5
        self.hold_flags = [False]*5
        self.roll_count = 0
        self.round = 0
        self.scores = {cat: None for cat in self.UPPER_CATEGORIES + self.LOWER_CATEGORIES}
        self.roll_button.config(state=tk.NORMAL)
        self.update_dice_display()
        self.update_scorecard_display()
        self.info_label.config(text="Round 1 — Rolls: 0/3")
        self.show_rules_popup()

    # ---------------- RULES POPUP ----------------
    def show_rules_popup(self):
        # Create a new top-level popup window
        popup = tk.Toplevel(self.root)
        popup.title("🎲 How to Play Yahtzee")
        popup.configure(bg=self.bg_panel)
        popup.geometry("520x500")
        popup.resizable(False, False)

        # Header
        header = tk.Label(
            popup,
            text="🎲 How to Play Yahtzee",
            font=("Arial Black", 18),
            bg=self.bg_panel,
            fg=self.accent
        )
        header.pack(pady=(15, 10))

        # Scrollable frame
        text_frame = tk.Frame(popup, bg=self.bg_panel)
        text_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        # Text widget
        text_widget = tk.Text(
            text_frame,
            wrap="word",
            font=("Arial", 12),
            bg=self.bg_main,
            fg=self.text_light,
            padx=15,
            pady=10,
            relief="flat",
            yscrollcommand=scrollbar.set
        )
        text_widget.pack(fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)

        # Rules text
        rules = (
            "🎲 HOW TO PLAY YAHTZEE\n\n"
            "• Objective: Score the highest total after 13 rounds.\n"
            "• Each round: Roll five dice up to three times.\n"
            "• You may hold (keep) any dice between rolls to aim for specific combos.\n"
            "• After rolling, select one empty category on the scorecard to record your score.\n"
            "• Each category can only be used once — even if the score is 0.\n\n"
            "🏆 SCORING HIGHLIGHTS:\n\n"
            "• Yahtzee (five of a kind): 50 points.\n"
            "• Large Straight (1–5 or 2–6): 40 points.\n"
            "• Small Straight (four in a row): 30 points.\n"
            "• Full House (3 of one + 2 of another): 25 points.\n"
            "• Three/Four of a Kind: Sum of all dice.\n"
            "• Upper Section (Ones–Sixes): Sum of dice showing that number.\n"
            "• Chance: Total of all dice, any combination.\n\n"
            "💡 TIP: Plan ahead! Use lower-value rolls strategically and save your best rolls for high-scoring categories."
        )

        text_widget.insert("1.0", rules)
        text_widget.config(state="disabled")  # make text read-only

        # Close button
        close_btn = tk.Button(
            popup,
            text="Close",
            font=("Arial", 12, "bold"),
            bg=self.accent,
            fg="black",
            padx=10,
            pady=5,
            command=popup.destroy
        )
        close_btn.pack(pady=10)

        # Center popup relative to main window
        popup.transient(self.root)
        popup.grab_set()
        self.root.wait_window(popup)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    game = Yahtzee(root)
    root.mainloop()
