import tkinter as tk

from ai_data_eng.halma_game.globals import PLAYER, STATE
from ai_data_eng.halma_game.logic.engine import Engine
from ai_data_eng.halma_game.logic.gamestate import GameState
from ai_data_eng.halma_game.ui.game_adapter import GameUiAdapter


def as_str(board, y, x):
    return str(board[y][x].value) if board[y][x] != STATE.EMPTY else ""


class HalmaGUI:
    def __init__(self, master, game_adapter: GameUiAdapter):
        self.master = master
        self.game_adapter = game_adapter
        self.master.title("Halma Game")
        self.field_from = None

        # Define colors for players
        self.bg_colors = {STATE.WHITE: "#5485A5", STATE.BLACK: "#E3A24D"}
        self.cell_colors = {STATE.WHITE: "#C2D6E3", STATE.BLACK: "#DED0BD", STATE.EMPTY: "#DBD4E2"}
        self.ui_board = None

        # Create the game board
        self.create_board()

    # This functions should be implemented to show next game state
    def navigate_back(self):
        pass

    def navigate_forward(self):
        self.game_adapter.next()
        self.update_ui()

    # Also print all necessary information
    def update_ui(self):
        self.draw_player_positions()
        self.update_displayed_info()

    def update_displayed_info(self):
        self.player_label.configure(text=f"Player: {self.game_adapter.moving_player()}")
        self.round_label.configure(text=f"Round: {self.game_adapter.round_number()}")

    # color this according to the
    def color_cells(self, colors):
        for i in range(16):
            for j in range(16):
                self.ui_board[i][j].configure(bg=colors[i][j])

    def create_welcome_window(self):
        pass

    def create_game_board(self):
        pass

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
        self.back_button.grid(row=l_r, column=1, columnspan=2)
        # self.back_button.pack(side=tk.LEFT, padx=5)
        self.forward_button = tk.Button(self.master, text="Forward", command=self.navigate_forward)
        self.forward_button.grid(row=l_r, column=3, columnspan=3)
        # self.forward_button.pack(side=tk.LEFT, padx=5)
        self.player_label = tk.Label(self.master, text=f"Player: {self.game_adapter.moving_player()}")
        self.player_label.grid(row=l_r, column=6, columnspan=4)
        self.round_label = tk.Label(self.master, text=f"Round: {self.game_adapter.round_number()}")
        self.round_label.grid(row=l_r, column=10, columnspan=4)

    def draw_player_positions(self):
        state_board = self.game_adapter.get_board()
        for i in range(16):
            for j in range(16):
                self.ui_board[i][j].delete("all")
                self.ui_board[i][j].configure(bg=self.cell_colors[state_board[i][j]])
                self.ui_board[i][j].create_text(15, 15, text=as_str(state_board, i, j), font=("Arial", 10), fill="black")

    def draw_camps(self):
        '''This should be called at the beginning'''
        for i in range(16):
            for j in range(16):
                color = self.bg_colors.get(self.game_adapter.get_board()[i][j], 'white')
                self.ui_board[i][j].configure(highlightthickness=2, highlightbackground=color, highlightcolor=color)

