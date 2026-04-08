"""
Tic Tac Toe — Python + Tkinter
Features: 2-player & vs Computer (unbeatable AI), score tracking, animated feedback
Run: python3 tictactoe.py
"""

import tkinter as tk
from tkinter import font as tkfont
import math

# ── Constants ──────────────────────────────────────────────────────────────────
BG         = "#1e1e2e"   # dark background
SURFACE    = "#2a2a3d"   # cell background
SURFACE_HV = "#32324a"   # cell hover
X_COLOR    = "#f38ba8"   # rose for X
O_COLOR    = "#89b4fa"   # blue for O
WIN_COLOR  = "#a6e3a1"   # green highlight for winning cells
DRAW_COLOR = "#fab387"   # orange for draw
TEXT_DIM   = "#6c7086"   # muted text
TEXT_MAIN  = "#cdd6f4"   # main text
ACCENT     = "#cba6f7"   # purple accent

WINS = [
    (0,1,2),(3,4,5),(6,7,8),   # rows
    (0,3,6),(1,4,7),(2,5,8),   # cols
    (0,4,8),(2,4,6)            # diagonals
]


# ── AI: Minimax ────────────────────────────────────────────────────────────────
def minimax(board, is_max, depth=0):
    winner = check_winner(board)
    if winner == "O": return  10 - depth
    if winner == "X": return -10 + depth
    if all(c != "" for c in board): return 0

    scores = []
    for i in range(9):
        if board[i] == "":
            board[i] = "O" if is_max else "X"
            scores.append(minimax(board, not is_max, depth + 1))
            board[i] = ""
    return max(scores) if is_max else min(scores)


def best_move(board):
    best_score, best_idx = -math.inf, 0
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""
            if score > best_score:
                best_score, best_idx = score, i
    return best_idx


def check_winner(board):
    for a, b, c in WINS:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    return None


# ── Main Application ───────────────────────────────────────────────────────────
class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.configure(bg=BG)
        self.resizable(False, False)

        # Fonts
        self.font_title  = tkfont.Font(family="Helvetica", size=22, weight="bold")
        self.font_cell   = tkfont.Font(family="Helvetica", size=44, weight="bold")
        self.font_status = tkfont.Font(family="Helvetica", size=14)
        self.font_score  = tkfont.Font(family="Helvetica", size=20, weight="bold")
        self.font_label  = tkfont.Font(family="Helvetica", size=11)
        self.font_btn    = tkfont.Font(family="Helvetica", size=12)

        # State
        self.board     = [""] * 9
        self.current   = "X"
        self.game_over = False
        self.vs_ai     = tk.BooleanVar(value=False)
        self.scores    = {"X": 0, "O": 0, "D": 0}
        self.cell_btns = []

        self._build_ui()
        self._update_status()

    # ── UI Construction ────────────────────────────────────────────────────────
    def _build_ui(self):
        # Title
        tk.Label(self, text="Tic Tac Toe", font=self.font_title,
                 bg=BG, fg=ACCENT).pack(pady=(28, 6))

        # Mode toggle
        mode_frame = tk.Frame(self, bg=BG)
        mode_frame.pack(pady=(0, 16))
        tk.Label(mode_frame, text="2 Player", font=self.font_label,
                 bg=BG, fg=TEXT_DIM).pack(side="left", padx=6)
        tk.Checkbutton(mode_frame, variable=self.vs_ai, command=self._on_mode_change,
                       bg=BG, fg=ACCENT, activebackground=BG,
                       selectcolor=SURFACE, relief="flat",
                       cursor="hand2").pack(side="left")
        tk.Label(mode_frame, text="vs Computer", font=self.font_label,
                 bg=BG, fg=TEXT_DIM).pack(side="left", padx=6)

        # Score board
        score_frame = tk.Frame(self, bg=BG)
        score_frame.pack(padx=24, pady=(0, 18))
        self._make_score_card(score_frame, "X", X_COLOR, "score_x").pack(side="left", padx=8)
        self._make_score_card(score_frame, "Draw", TEXT_DIM, "score_d").pack(side="left", padx=8)
        self._make_score_card(score_frame, "O", O_COLOR, "score_o").pack(side="left", padx=8)

        # Status label
        self.status_var = tk.StringVar()
        tk.Label(self, textvariable=self.status_var, font=self.font_status,
                 bg=BG, fg=TEXT_MAIN, width=22, anchor="center").pack(pady=(0, 14))

        # Grid board
        board_frame = tk.Frame(self, bg=BG)
        board_frame.pack(padx=24)
        for i in range(9):
            row, col = divmod(i, 3)
            btn = tk.Button(
                board_frame,
                text="", font=self.font_cell,
                width=3, height=1,
                bg=SURFACE, activebackground=SURFACE_HV,
                fg=TEXT_MAIN, relief="flat",
                cursor="hand2",
                command=lambda idx=i: self._on_click(idx)
            )
            btn.grid(row=row, column=col, padx=5, pady=5, ipadx=10, ipady=10)
            btn.bind("<Enter>", lambda e, b=btn: self._hover(b, True))
            btn.bind("<Leave>", lambda e, b=btn: self._hover(b, False))
            self.cell_btns.append(btn)

        # Buttons
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=20)
        self._action_btn(btn_frame, "New Game", self._reset_game).pack(side="left", padx=8)
        self._action_btn(btn_frame, "Reset Score", self._reset_score).pack(side="left", padx=8)

    def _make_score_card(self, parent, label, color, attr_name):
        frame = tk.Frame(parent, bg=SURFACE, padx=16, pady=10)
        tk.Label(frame, text=label, font=self.font_label,
                 bg=SURFACE, fg=color).pack()
        val = tk.Label(frame, text="0", font=self.font_score,
                       bg=SURFACE, fg=color)
        val.pack()
        setattr(self, attr_name, val)
        return frame

    def _action_btn(self, parent, text, cmd):
        return tk.Button(parent, text=text, font=self.font_btn,
                         bg=SURFACE, fg=TEXT_MAIN,
                         activebackground=SURFACE_HV, activeforeground=TEXT_MAIN,
                         relief="flat", padx=16, pady=8, cursor="hand2",
                         command=cmd)

    # ── Gameplay ───────────────────────────────────────────────────────────────
    def _on_click(self, idx):
        if self.game_over or self.board[idx]:
            return
        self._place(idx, self.current)
        if not self.game_over and self.vs_ai.get() and self.current == "O":
            self.after(300, self._ai_turn)

    def _ai_turn(self):
        if self.game_over:
            return
        idx = best_move(self.board)
        self._place(idx, "O")

    def _place(self, idx, player):
        self.board[idx] = player
        color = X_COLOR if player == "X" else O_COLOR
        self.cell_btns[idx].config(text=player, fg=color, state="disabled",
                                   disabledforeground=color)

        winner = check_winner(self.board)
        if winner:
            self._end_game(winner)
        elif all(c != "" for c in self.board):
            self._end_game(None)
        else:
            self.current = "O" if player == "X" else "X"
            self._update_status()

    def _end_game(self, winner):
        self.game_over = True
        if winner:
            self.scores[winner] += 1
            self._update_scores()
            # Highlight winning cells
            for a, b, c in WINS:
                if self.board[a] == self.board[b] == self.board[c] == winner:
                    for i in (a, b, c):
                        self.cell_btns[i].config(bg=WIN_COLOR,
                                                  disabledforeground=BG)
                    break
            label = f"{'You win' if (self.vs_ai.get() and winner == 'X') else ('Computer wins' if (self.vs_ai.get() and winner == 'O') else f'{winner} wins')}! 🎉"
            self.status_var.set(label)
        else:
            self.scores["D"] += 1
            self._update_scores()
            for btn in self.cell_btns:
                if btn["state"] == "normal":
                    btn.config(bg=DRAW_COLOR)
            self.status_var.set("It's a draw! 🤝")

    def _hover(self, btn, entering):
        if btn["state"] == "normal":
            btn.config(bg=SURFACE_HV if entering else SURFACE)

    def _update_status(self):
        if self.vs_ai.get():
            msg = "Your turn (X)" if self.current == "X" else "Computer thinking…"
        else:
            msg = f"{self.current}'s turn"
        self.status_var.set(msg)

    def _update_scores(self):
        self.score_x.config(text=str(self.scores["X"]))
        self.score_o.config(text=str(self.scores["O"]))
        self.score_d.config(text=str(self.scores["D"]))

    # ── Reset ──────────────────────────────────────────────────────────────────
    def _reset_game(self):
        self.board     = [""] * 9
        self.current   = "X"
        self.game_over = False
        for btn in self.cell_btns:
            btn.config(text="", bg=SURFACE, state="normal",
                       fg=TEXT_MAIN, disabledforeground=TEXT_MAIN)
        self._update_status()

    def _reset_score(self):
        self.scores = {"X": 0, "O": 0, "D": 0}
        self._update_scores()
        self._reset_game()

    def _on_mode_change(self):
        self._reset_game()


# ── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()
