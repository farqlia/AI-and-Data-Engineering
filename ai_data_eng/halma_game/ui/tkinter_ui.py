import logging
import threading
import tkinter as tk
from tkinter import messagebox

from ai_data_eng.halma_game.globals import STATE
from ai_data_eng.halma_game.adapters.game_live_adapter import GameLiveUiAdapter


def as_str(board, y, x):
    return str(board[y][x].value) if board[y][x] != STATE.EMPTY else ""


def color_formula(weight, color):
    return color[0], int((1 - weight) * color[1]), color[2]


def from_rgb(rgb):
    """Translates an RGB tuple of integers to a Tkinter-friendly color code."""
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'


class HalmaGUI:
    def __init__(self, game_adapter: GameLiveUiAdapter):
        self.master = tk.Tk()
        self.game_adapter = game_adapter
        self.master.title("Halma Game")
        self.field_from = None

        # Define colors for players
        self.bg_colors = {STATE.WHITE: "#5485A5", STATE.BLACK: "#E3A24D"}
        self.cell_colors = {STATE.WHITE: "#C2D6E3", STATE.BLACK: "#DED0BD", STATE.EMPTY: "#DBD4E2"}
        self.ui_board = None
        self.winner = None

        # Create the game board
        self.create_board()

    def run(self):
        self.update_ui()
        self.master.mainloop()

    # This functions should be implemented to show next game state
    def navigate_back(self):
        pass

    def navigate_forward(self):
        self.play_round()
        self.forward_gui()

    def forward_gui(self):
        self.update_ui()
        if self.winner:
            logging.info("Match is finished")
            messagebox.showinfo("Information", f"The winner is {self.winner}")

    def play_round(self):
        self.game_adapter.next()
        self.winner = self.game_adapter.is_finished()

    def play_automatically(self):
        while self.winner is None:
            t = threading.Thread(target=self.play_round)
            t.start()
            t.join()
            self.forward_gui()

    # Also print all necessary information
    def update_ui(self):
        self.draw_player_positions()
        self.update_displayed_info()
        weights = self.game_adapter.to_be_moved().get_weights()
        if weights:
            colors = self.weights_to_colors(weights)
            self.color_cells(colors)

    def update_displayed_info(self):
        self.player_label.configure(text=f"Player: {self.game_adapter.moving_player()}")
        self.round_label.configure(text=f"Move: {self.game_adapter.round_number()}")
        self.tree_size_label.configure(
            text=f"TS: {self.game_adapter.player1.search_tree_size()}|{self.game_adapter.player2.search_tree_size()}")

    def weights_to_colors(self, weights):
        base_color = (255, 127, 255)
        colors = [[None for _ in range(16)] for _ in range(16)]
        for i in range(16):
            for j in range(16):
                colors[i][j] = from_rgb(color_formula(weights[i][j], base_color))
        return colors

    def color_cells(self, colors):
        for i in range(16):
            for j in range(16):
                self.ui_board[i][j].configure(bg=colors[i][j])

    def create_board(self):
        self.ui_board = []

        for i in range(16):
            cell = tk.Canvas(self.master, width=30, height=30, bg="white", border=1.0)
            cell.grid(row=i + 1, column=0)
            cell.create_text(15, 15, text=i, font=("Arial", 10), fill="black")

        for i in range(16):
            cell = tk.Canvas(self.master, width=30, height=30, bg="white", border=1.0)
            cell.grid(row=0, column=i + 1)
            cell.create_text(15, 15, text=i, font=("Arial", 10), fill="black")

        for i in range(16):
            cell = tk.Canvas(self.master, width=30, height=30, bg="white", border=1.0)
            cell.grid(row=17, column=i + 1)
            cell.create_text(15, 15, text=i, font=("Arial", 10), fill="black")

        for i in range(16):
            cell = tk.Canvas(self.master, width=30, height=30, bg="white", border=1.0)
            cell.grid(row=i + 1, column=17)
            cell.create_text(15, 15, text=i, font=("Arial", 10), fill="black")

        for i in range(1, 17):
            row = []
            for j in range(1, 17):
                cell = tk.Canvas(self.master, width=30, height=30, bg=self.cell_colors[STATE.EMPTY], border=1.0)
                cell.grid(row=i, column=j)
                row.append(cell)
            self.ui_board.append(row)

        l_r = 18
        self.draw_camps()
        self.back_button = tk.Button(self.master, text="Back", command=self.navigate_back)
        self.back_button.grid(row=l_r, column=1, columnspan=1)
        # self.back_button.pack(side=tk.LEFT, padx=5)
        self.forward_button = tk.Button(self.master, text="Next", command=self.navigate_forward)
        self.forward_button.grid(row=l_r, column=2, columnspan=1)
        self.forward_button = tk.Button(self.master, text="Play", command=self.play_automatically)
        self.forward_button.grid(row=l_r, column=3, columnspan=1)
        # self.forward_button.pack(side=tk.LEFT, padx=5)
        self.player_label = tk.Label(self.master, text=f"Player: {self.game_adapter.moving_player()}")
        self.player_label.grid(row=l_r, column=6, columnspan=4)
        self.round_label = tk.Label(self.master, text=f"Round: {self.game_adapter.round_number()}")
        self.round_label.grid(row=l_r, column=10, columnspan=3)
        self.tree_size_label = tk.Label(self.master, text=f"TS: 0")
        self.tree_size_label.grid(row=l_r, column=13, columnspan=4)

    def draw_player_positions(self):
        state_board = self.game_adapter.get_board()
        for i in range(16):
            for j in range(16):
                self.ui_board[i][j].delete("all")
                self.ui_board[i][j].configure(bg=self.cell_colors[state_board[i][j]])
                self.ui_board[i][j].create_text(15, 15, text=as_str(state_board, i, j), font=("Arial", 10),
                                                fill="black")

    def draw_camps(self):
        '''This should be called at the beginning'''
        for i in range(0, 5):
            for j in range(0, [5, 5, 4, 3, 2][i]):
                color = self.bg_colors.get(STATE.BLACK, 'white')
                self.ui_board[i][j].configure(highlightthickness=2, highlightbackground=color)

        # Ustawiamy obóz Białego.
        for i in range(0, 5):
            for j in range(0, [5, 5, 4, 3, 2][i]):
                color = self.bg_colors.get(STATE.WHITE, 'white')
                self.ui_board[15 - i][15 - j].configure(highlightthickness=2, highlightbackground=color)
