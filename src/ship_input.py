import csv
from src.utils import in_bounds, coord_to_index, neighbours

SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def read_player_ships():
    ships = {}
    occupied = set()
    ship_id = 1

    print("Enter ship coordinates separated by spaces (e.g., A1 A2 A3 A4)")

    for size in SHIP_SIZES:
        while True:
            line = input(f"Ship size {size}: ").upper()
            cells = line.strip().split()

            try:
                if len(cells) != size:
                    raise ValueError(f"You need exactly {size} cells.")

                indexes = []
                for c in cells:
                    r, col = coord_to_index(c)
                    if not in_bounds(r, col):
                        raise ValueError("Coordinate out of bounds.")
                    indexes.append((r, col))

                # проверка на касание других кораблей
                for r, col in indexes:
                    for nr, nc in neighbours(r, col):
                        if (nr, nc) in occupied:
                            raise ValueError("Ships cannot touch each other.")

                for cell in indexes:
                    occupied.add(cell)

                ships[ship_id] = cells  # сохраняем уже в формате "A1"
                ship_id += 1
                break

            except ValueError as e:
                print("Invalid ship placement:", e, "Try again.")

    return ships

def save_ships(ships, filename):
    """Сохраняем корабли в CSV в графическом виде (A1, B5 и т.д.)"""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ship_id", "cell"])
        for ship_id, cells in ships.items():
            for cell in cells:
                writer.writerow([ship_id, cell])
