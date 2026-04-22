

import tkinter as tk
from tkinter import messagebox
import random




class TicTacToeGame:
    def __init__(self):
        self.reset()
        self.algorithm = "Minimax"  

    def reset(self):
        self.board = [' ' for _ in range(9)]
        self.winner = None
        self.game_over = False

    def check_winner(self, player):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for w in wins:
            if self.board[w[0]] == self.board[w[1]] == self.board[w[2]] == player:
                return True
        return False

    def is_full(self):
        return ' ' not in self.board

    def get_empty(self):
        return [i for i, v in enumerate(self.board) if v == ' ']

    
    def random_move(self):
        empty = self.get_empty()
        if empty:
            return random.choice(empty)
        return None

    
    def greedy_move(self):
        empty = self.get_empty()

        
        for i in empty:
            self.board[i] = 'O'
            if self.check_winner('O'):
                self.board[i] = ' '
                return i
            self.board[i] = ' '

        
        for i in empty:
            self.board[i] = 'X'
            if self.check_winner('X'):
                self.board[i] = ' '
                return i
            self.board[i] = ' '

        
        if self.board[4] == ' ':
            return 4

       
        corners = [0, 2, 6, 8]
        random.shuffle(corners)
        for c in corners:
            if self.board[c] == ' ':
                return c

        
        return empty[0] if empty else None

    
    def minimax(self, is_max):
        if self.check_winner('O'):
            return 1
        if self.check_winner('X'):
            return -1
        if self.is_full():
            return 0

        if is_max:
            best = -1000
            for i in self.get_empty():
                self.board[i] = 'O'
                score = self.minimax(False)
                self.board[i] = ' '
                best = max(best, score)
            return best
        else:  
            best = 1000
            for i in self.get_empty():
                self.board[i] = 'X'
                score = self.minimax(True)
                self.board[i] = ' '
                best = min(best, score)
            return best

    def minimax_move(self):
        best_score = -1000
        best_move = None
        for i in self.get_empty():
            self.board[i] = 'O'
            score = self.minimax(False)
            self.board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
        return best_move

    
    def computer_move(self):
        if self.algorithm == "Random":
            return self.random_move()
        elif self.algorithm == "Greedy":
            return self.greedy_move()
        else:
            return self.minimax_move()

    def player_move(self, pos):
        if self.board[pos] == ' ' and not self.game_over:
            self.board[pos] = 'X'
            if self.check_winner('X'):
                self.winner = "player"
                self.game_over = True
            elif self.is_full():
                self.winner = "tie"
                self.game_over = True
            return True
        return False




class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.window.geometry("450x600")
        self.window.configure(bg='#1a1a2e')

        self.game = TicTacToeGame()
        self.buttons = []

        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        
        title = tk.Label(self.window, text="Tic-Tac-Toe",
                         font=("Arial", 28, "bold"), bg='#1a1a2e', fg='white')
        title.pack(pady=20)

        
        algo_frame = tk.Frame(self.window, bg='#1a1a2e')
        algo_frame.pack(pady=10)

        tk.Label(algo_frame, text="خوارزمية الكمبيوتر:",
                 font=("Arial", 12), bg='#1a1a2e', fg='white').pack(side='left', padx=5)

        self.algo_var = tk.StringVar(value="Minimax")
        algo_menu = tk.OptionMenu(algo_frame, self.algo_var, "Random", "Greedy", "Minimax",
                                  command=self.change_algorithm)
        algo_menu.config(bg='#16213e', fg='white', font=("Arial", 11))
        algo_menu.pack(side='left', padx=10)

       
        self.info_label = tk.Label(self.window, text="🧠 Minimax: أذكى خوارزمية",
                                   font=("Arial", 10), bg='#1a1a2e', fg='#f1c40f')
        self.info_label.pack(pady=5)

        
        board_frame = tk.Frame(self.window, bg='#1a1a2e')
        board_frame.pack(pady=30)

        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(board_frame, text="", font=("Arial", 40, "bold"),
                                width=4, height=2, bg='#0f3460', fg='white',
                                activebackground='#16213e',
                                command=lambda r=i, c=j: self.player_click(r, c))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

        
        self.status_label = tk.Label(self.window, text="🎮 دورك انت!",
                                     font=("Arial", 14, "bold"), bg='#1a1a2e', fg='#4ecdc4')
        self.status_label.pack(pady=10)

        
        control_frame = tk.Frame(self.window, bg='#1a1a2e')
        control_frame.pack(pady=20)

        reset_btn = tk.Button(control_frame, text="🔄 إعادة اللعب", font=("Arial", 12),
                              bg='#e94560', fg='white', padx=20, pady=5,
                              command=self.reset_game)
        reset_btn.pack(side='left', padx=10)

        exit_btn = tk.Button(control_frame, text="🚪 خروج", font=("Arial", 12),
                             bg='#533483', fg='white', padx=20, pady=5,
                             command=self.window.quit)
        exit_btn.pack(side='left', padx=10)

    def change_algorithm(self, algo):
        self.game.algorithm = algo
        info = {
            "Random": "🎲 Random: حركات عشوائية - سهل الفوز عليه",
            "Greedy": "⚡ Greedy: ذكي - يفكر في الفوز والمنع",
            "Minimax": "🧠 Minimax: أذكى خوارزمية - صعب الفوز عليه"
        }
        self.info_label.config(text=info[algo])
        self.reset_game()

    def player_click(self, row, col):
        pos = row * 3 + col

        
        if self.game.game_over:
            messagebox.showinfo("تنبيه", "اللعبة انتهت! اضغط إعادة اللعب")
            return

        
        if self.game.winner is not None:
            return

        
        if self.game.player_move(pos):
            self.update_button(pos, 'X')

            
            if self.game.winner == "player":
                self.show_winner("🎉 انت فزت! 🎉")
                return

            
            if self.game.winner == "tie":
                self.show_winner("🤝 تعادل! 🤝")
                return

            
            self.status_label.config(text="💻 دور الكمبيوتر...", fg='#f9a826')
            self.window.update()
            self.window.after(300, self.computer_play)

    def computer_play(self):
       
        if self.game.game_over:
            return

        
        move = self.game.computer_move()

        if move is not None:
            self.game.board[move] = 'O'
            self.update_button(move, 'O')

            
            if self.game.check_winner('O'):
                self.game.game_over = True
                self.show_winner("💻 الكمبيوتر فاز! 💻")
                return

           
            if self.game.is_full():
                self.game.game_over = True
                self.show_winner("🤝 تعادل! 🤝")
                return

      
        self.status_label.config(text="🎮 دورك انت!", fg='#4ecdc4')

    def update_button(self, pos, symbol):
        row = pos // 3
        col = pos % 3
        self.buttons[row][col].config(text=symbol, state='disabled')

    def show_winner(self, message):
        self.status_label.config(text=message)
        for row in self.buttons:
            for btn in row:
                btn.config(state='disabled')

        answer = messagebox.askyesno("اللعبة انتهت", f"{message}\n\nهل تريد اللعب مرة أخرى؟")
        if answer:
            self.reset_game()
        else:
            self.window.quit()

    def reset_game(self):
        self.game.reset()
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", state='normal', bg='#0f3460')
        self.status_label.config(text="🎮 دورك انت!", fg='#4ecdc4')



if __name__ == "__main__":
    TicTacToeGUI()