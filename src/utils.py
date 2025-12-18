BOARD_SIZE = 10

def in_bounds(r, c):
    """Проверка, что индексы внутри доски"""
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

def neighbours(r, c):
    """Возвращает все соседние клетки (включая диагонали)"""
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc):
            yield nr, nc

def coord_to_index(coord):
    """Преобразует координату вида 'A1' в индексы (row, col)"""
    row = ord(coord[0].upper()) - ord('A')
    col = int(coord[1:]) - 1
    return row, col

def index_to_coord(row, col):
    """Преобразует индексы (row, col) обратно в координату 'A1'"""
    return f"{chr(row + ord('A'))}{col + 1}"
