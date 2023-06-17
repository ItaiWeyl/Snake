import tkinter as tk
from boggle_board_randomizer import randomize_board


class Board:
    def __init__(self, root):
        self.root = root
        root.title("Boggle Game")
        root.resizable(False, False)
        self.table = randomize_board()
        self.height = 4
        self.width = 4
        self.buttons = []
        self.displayed_word = ""

        self.upper_frame = tk.Frame(root, bg="gray")
        self.upper_frame.grid(row=0, column=0, padx=40, pady=20)

        self.word_display = tk.Label(self.upper_frame, text=self.displayed_word, font=("courier", 20), fg="black", bg="gray", width=10)
        self.word_display.pack(fill=tk.BOTH)

        self.lower_frame = tk.Frame(root, bg="gray")
        self.lower_frame.grid(row=1, column=0, padx=30, pady=40)

    def button_press(self, row, col):
        button = self.buttons[row][col]
        letter = button.cget('text')
        self.displayed_word += letter
        self.word_display.configure(text=self.displayed_word)
        self.word_display.update()
        print("Clicked at row:", row, "column:", col)
        print("Letter on the button:", letter)

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


if __name__ == '__main__':
    root = tk.Tk()
    b = Board(root)
    b.start()
