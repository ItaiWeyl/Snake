import tkinter as tk
from boggle_board_randomizer import randomize_board


class Board:
    def __init__(self, root, words_dict):
        self.root = root
        root.title("Boggle Game")
        root.resizable(False, False)
        self.table = randomize_board()
        self.height = 4
        self.width = 4
        self.buttons = []
        self.displayed_word = ""
        self.words_dict = words_dict
        self.score = 0
        self.time = 0
        self.available = set()
        self.words_found = []
        self.path = []

        self.left_frame = tk.Frame(root, bg="white")
        self.left_frame.grid(row=0, column=0)
        self.delete_button = tk.Button(self.left_frame, text="del", width=5, height=5)
        self.delete_button.grid(row=0, column=0, pady=5, padx=5)
        self.delete_button.config(command=lambda: self.delete_word())

        self.right_frame = tk.Frame(root, bg="white", pady=40, padx=40)
        self.right_frame.grid(row=0, column=1)
        self.right_frame.rowconfigure(0, weight=1)
        self.right_frame.columnconfigure(1, weight=1)
        red_label = tk.Label(self.right_frame, text='WORDS:', bg="gray", height=5, width=8)
        red_label.grid(row=0, column=1)

        self.upper_frame = tk.Frame(self.left_frame, bg="gray")
        self.upper_frame.grid(row=0, column=1, padx=40, pady=20)

        self.word_display = tk.Label(self.upper_frame, text=self.displayed_word, font=("courier", 20), fg="black",
                                     bg="gray", width=len(self.displayed_word))
        self.word_display.pack(fill=tk.BOTH, expand=False)

        self.lower_frame = tk.Frame(self.left_frame, bg="gray")
        self.lower_frame.grid(row=1, column=1, padx=30, pady=40)

        self.timer = tk.Label(self.upper_frame, text="3:00", font=("helveca", 20), fg="green", bg="pink", width=10)
        self.timer.pack(fill=tk.NONE)

    def is_legal_word(self):
        current_word = self.displayed_word
        if current_word in self.words_dict and current_word not in self.words_found:
            self.score += len(current_word) ** 2
            new_label = tk.Label(self.right_frame, text=current_word, height=5, width=10)
            new_label.pack()
            self.words_found.append(current_word)
            self.path = []
            self.available = []
            self.root.after(500, self.delete_word)

    def button_press(self, row, col):
        cor = (row, col)
        if cor in self.available or not self.available:
            button = self.buttons[row][col]
            letter = button.cget('text')
            self.displayed_word += letter
            self.word_display.configure(text=self.displayed_word)
            self.word_display.update()
            self.path.append(cor)
            self.available = helper.get_neighbors(cor, self.table) - set(self.path)
            self.is_legal_word()
            self.update_buttons_color()

    def delete_word(self):
        self.displayed_word = ""
        self.path = []
        self.available = set()
        self.word_display.configure(text=self.displayed_word)
        self.word_display.update()
        self.update_buttons_color()

    def set_buttons(self):
        for row in range(self.height):
            tmp_row = []
            for col in range(self.width):
                new_b = tk.Button(self.lower_frame, text=self.table[row][col], width=7, height=7)
                new_b.config(command=lambda r=row, c=col: self.button_press(r, c))
                new_b.grid(row=row, column=col, padx=10, pady=10)
                tmp_row.append(new_b)
            self.buttons.append(tmp_row)

    def start(self):
        self.set_buttons()
        self.root.mainloop()

    def restart(self):
        self.table = randomize_board()
        self.score = 0
        self.time = 0
        self.available = set()
        self.words_found = []
        self.path = []
        self.buttons = []
        self.set_buttons()
        self.update_time()




if __name__ == '__main__':
    root = tk.Tk()
    b = Board(root, {"BT": 0, "DE": 0, "SH": 0, "AE": 0, "TO": 0})
    b.start()

