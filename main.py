import tkinter as tk
from tkinter import messagebox
import random


class flip_game:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory game")

        # game setting
        self.rows, self.cols = 4, 4  # number of all row and cols int the game
        self.card = list("AABBCCDDEEFFGGHH")  # 8 PAIRS
        random.shuffle(self.card)

        # color variable
        self.color_blue = "#4584b6"
        self.color_yellow = "#ffde57"
        self.color_gray = "#343434"
        self.color_light_gray = "#646464"

        # game state
        self.button = {}
        self.flipped = []  # store (row,col) of flipped cards
        self.revealed = set()
        self.current_player = 1
        self.score = {1: 0, 2: 0}
        self.game_over = False

        # UI
        self.score_label = tk.Label(
            root, text=self.get_score_text(), font=("Arial", 14)
        )
        self.score_label.grid(row=0, column=0, columnspan=self.cols, pady=10)

        self.create_board()

    def get_score_text(self):
        return f"Player 1: {self.score[1]}   Player 2: {self.score[2]}   |   Turn: Player {self.current_player}"

    def create_board(self):
        global board_btn
        for row in range(self.rows):
            for column in range(self.cols):
                board_btn = tk.Button(
                    self.root,
                    text="?",
                    background=self.color_gray,
                    foreground="white",
                    width=6,
                    height=3,
                    font=("Arial", 18, "bold"),
                    command=lambda row=row, column=column: self.flip_card(row, column),
                )

                board_btn.grid(
                    row=row + 1,
                    column=column,
                )
                self.button[(row, column)] = board_btn

        restart = tk.Button(
            self.root,
            text="RESART",
            background="white",
            foreground=self.color_gray,
            font=("Consolas", 20),
            command=self.new_game,
        )
        restart.grid(row=self.rows + 2, column=0, columnspan=self.cols, sticky="we")

    def flip_card(self, row, col):
        if (row, col) in self.revealed:
            return
        if len(self.flipped) == 2:  # wating for the prosess
            return

        idx = row * self.cols + col  # inddex for back card that realetec to card order
        btn = self.button[(row, col)]
        btn.config(
            text=self.card[idx],
            background=self.color_yellow,
            foreground=self.color_blue,
        )

        self.flipped.append((row, col))

        if len(self.flipped) == 2:
            self.root.after(1000, self.check_match)

    def check_match(self):
        (r1, c1), (r2, c2) = self.flipped
        i1, i2 = r1 * self.cols + c1, r2 * self.cols + c2

        if self.card[i1] == self.card[i2]:
            # match found
            self.revealed.add((r1, c1))
            self.revealed.add((r2, c2))
            self.score[
                self.current_player
            ] += 1  # give score to the user who flipped the true card
        else:
            self.button[(r1, c1)].config(
                text="?", background=self.color_gray, foreground="white"
            )
            self.button[(r2, c2)].config(
                text="?", background=self.color_gray, foreground="white"
            )

            # change player
            self.current_player = 2 if self.current_player == 1 else 1

        self.flipped = []
        self.score_label.config(text=self.get_score_text())

        # check if game over
        if len(self.revealed) == self.rows * self.cols:
            self.end_game()

    def end_game(self):
        if self.score[1] > self.score[2]:
            winner = "Player 1 WIN"
        elif self.score[1] < self.score[2]:
            winner = "Player 2 WIN"
        else:
            winner = "Its a tie!"

        self.game_over = True
        self.score_label.config(text=f"{winner}", foreground=self.color_blue)
        return

    def new_game(self):
        for (
            widget
        ) in (
            root.winfo_children()
        ):  # will destroy all of the window and start  from the beginning
            widget.destroy()
        flip_game(root)


if __name__ == "__main__":
    root = tk.Tk()  # make an window or base user interface
    game = flip_game(root)
    root.mainloop()
