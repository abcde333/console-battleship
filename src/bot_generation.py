import random
import csv
from src.utils import BOARD_SIZE, in_bounds, neighbours, index_to_coord

SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def generate_bot_ships():
    occupied = set()
    ships = {}
    ship_id = 1

    for size in SHIP_SIZES:
        while True:
            horizontal = random.choice([True, False])
            r = random.randint(0, BOARD_SIZE - 1)
            c = random.randint(0, BOARD_SIZE - 1)

            cells = []
            for i in range(size):
                nr = r + (0 if horizontal else i)
                nc = c + (i if horizontal else 0)
                if not in_bounds(nr, nc):
                    break
                cells.append((nr, nc))

            if len(cells) != size:
                continue

            bad = False
            for r_cell, c_cell in cells:
                if (r_cell, c_cell) in occupied:
                    bad = True
                    break
                for nr, nc in neighbours(r_cell, c_cell):
                    if (nr, nc) in occupied:
                        bad = True
                        break
                if bad:
                    break

            if bad:
                continue

            for cell in cells:
                occupied.add(cell)

            ships[ship_id] = [index_to_coord(r, c) for r, c in cells]
            ship_id += 1
            break

    return ships

def save_bot_ships(ships, filename="data/bot_ships.csv"):
    """Сохраняем корабли бота в графическом виде"""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ship_id", "cell"])
        for ship_id, cells in ships.items():
            for cell in cells:
                writer.writerow([ship_id, cell])
