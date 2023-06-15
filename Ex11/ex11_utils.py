from typing import List, Tuple, Iterable, Optional, Dict

Board = List[List[str]]
Path = List[Tuple[int, int]]


def get_words_dict(address) -> Iterable[str]:
    words_dict = {}
    with open(address, "r") as file:
        for word in file:
            words_dict[word] = "_"
    return words_dict


def sort_by_letters(board: Board, words: Iterable[str]) -> Dict[str]:
    sorted_dict = {}
    current_letters = []
    # adding all the letters in the board to a string
    for line in board:
        for letter in line:
            if letter not in current_letters:
                current_letters.append(letter)
    for word in words:
        break_checker = False
        for letter in word:
            if letter not in current_letters:
                break_checker = True
                break
        if not break_checker:
            sorted_dict[word] = "_"
    return sorted_dict


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:



def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    pass


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    pass


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    pass
