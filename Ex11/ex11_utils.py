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
    board_length = len(board)
    board_width = len(board[0])
    path_set = set(path)
    if len(path) != len(path_set):  # in case one of the coordinates is outside the board
        return None
    for i in range(len(path) - 1):
        cor = path[i]
        next_cor = path[i+1]
        delta_cor = cor[0] + cor[1] - next_cor[0] - next_cor[1]
        if delta_cor < -2 or delta_cor > 2:
            return None
        # in case one of the coordinates is outside the board
        if cor[0] >= board_length or cor[0] < 0 or cor[1] >= board_width or cor[1] < 0:
            return None
    if path[-1][0] >= board_length or path[-1][0] < 0 or path[-1][1] >= board_width or\
            path[-1][1] < 0:  # for the last coordinate
        return None
    # check if the word is in the dictionary
    word = path_to_word(board, path)
    if word in words:
        return word
    else:
        return None


def path_to_word(board, path):
    """ gets a path and a board, creates the word from that path on the board"""
    word = ""
    for cor in path[::-1]:
        word += board[cor[0]][cor[1]]
    return word


def get_neighbors(cor, board):
    """ gets a coordinate, returns a list with all its neighbors"""
    neighbors = set()
    cor_row = cor[0]
    cor_col = cor[1]
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= cor_row + i < len(board) and 0 <= cor_col < len(board[0]):
                new_cor = (cor_row, cor_col)
                if new_cor != cor:
                    neighbors.add(new_cor)
    return neighbors


def is_path_in_words(words_dict, path_word, illegal_dict):
    for word in words_dict:
        if path_word in word:
            return True
    illegal_dict[path_word] = ""
    return False


def find_len_path_helper(n, board, words_dict, final_list, path, illegal_words):
    if len(path) == n:
        checker = is_valid_path(board, path, words_dict)
        if checker:
            final_list.append(path)
            return None
        else:
            return None
    path_word = path_to_word(board, path)
    if path_word in illegal_words:
        return None
    if is_path_in_words(words_dict, path_word, illegal_words):
        path_set = set(path)
        neighbors = get_neighbors(path[0], board)
        neighbors = neighbors - path_set
        for cor in neighbors:
            find_len_path_helper(n, board, words_dict, final_list, [cor] + path)
    return None


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    final_list = []
    words_dict = get_words_dict(words)
    sorted_dict = sort_by_letters(board, words_dict)
    for key in sorted_dict.keys():
        if len(key) != n:
            sorted_dict.pop(key)
    illegal_words = {}
    for line in board:
        for cor in line:
            find_len_path_helper(n, board, sorted_dict, final_list, [cor], illegal_words)
    return final_list




def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    pass


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    pass
