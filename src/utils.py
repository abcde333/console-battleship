import string

BOARD_SIZE = 10
LETTERS = string.ascii_uppercase[:BOARD_SIZE]


def coord_to_index(coord):
    row = LETTERS.index(coord[0])
    col = int(coord[1:]) - 1
    return row, col


def index_to_coord(row, col):
    return f"{LETTERS[row]}{col + 1}"


def is_inside(coord):
    try:
        r, c = coord_to_index(coord)
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE
    except:
        return False


def neighbors(row, col):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr != 0 or dc != 0:
                nr, nc = row + dr, col + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    yield nr, nc


def print_board(board, title):
    print(f"\n{title}")
    print("  " + " ".join(str(i+1) for i in range(BOARD_SIZE)))
    for i, row in enumerate(board):
        print(f"{LETTERS[i]} " + " ".join(row))
