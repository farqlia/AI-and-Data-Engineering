import tkinter as tk

from ai_data_eng.halma_game.engine import Engine
from ai_data_eng.halma_game.gameui import GameUI
from ai_data_eng.halma_game.globals import PLAYER, STATE


def as_str(board, y, x):
    return str(board[y][x].value) if board[y][x] != STATE.EMPTY else ""


class HalmaGUI:
    def __init__(self, master, game_ui):
        self.master = master
        self.game_ui = game_ui
        self.master.title("Halma Game")
        self.field_from = None

        # Define colors for players
        self.colors = {PLAYER.WHITE: "blue", PLAYER.BLACK: "black"}
        self.ui_board = None

        self.back_button = tk.Button(self.master, text="Back", command=self.navigate_back)
        # self.back_button.pack(side=tk.LEFT, padx=5)

        self.forward_button = tk.Button(self.master, text="Forward", command=self.navigate_forward)

        # self.forward_button.pack(side=tk.LEFT, padx=5)

        self.label = tk.Label(self.master, text=f"Player: {self.game_ui.moving_player()}")

        # Create the game board
        self.create_board()

    def navigate_back(self):
        pass

    def navigate_forward(self):
        pass

    def create_board(self):
        self.ui_board = []
        game_board = self.game_ui.get_board()
        for i in range(16):
            row = []
            for j in range(16):
                cell = tk.Canvas(self.master, width=30, height=30, bg='grey', border=1.0)
                cell.create_text(15,15, text=as_str(game_board, i, j), font=("Arial", 10), fill="black")
                cell.grid(row=i, column=j)
                row.append(cell)
            self.ui_board.append(row)

    def update_board(self):
        for i in range(16):
            for j in range(16):
                color = self.colors.get(self.game_ui.get_board()[i][j], 'white')
                self.ui_board[i][j].configure(bg=color)




def main():
    root = tk.Tk()
    engine = Engine()
    game_ui = GameUI(engine)
    halma_gui = HalmaGUI(root, game_ui)
    halma_gui.update_board()
    root.mainloop()

if __name__ == "__main__":
    main()
