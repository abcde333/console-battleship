import csv
from src.utils import is_inside, coord_to_index, neighbors

SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

def read_player_ships():
    ships = []
    occupied = set()

    print("Enter ships in format: size: A1 A2 A3")
    for size in SHIP_SIZES:
        while True:
            line = input(f"Ship size {size}: ").upper()
            try:
                s, coords = line.split(":")
                s = int(s.strip())
                cells = coords.strip().split()

                if s != size or len(cells) != size:
                    raise ValueError

                for c in cells:
                    if not is_inside(c):
                        raise ValueError

                indexes = [coord_to_index(c) for c in cells]

                for r, c in indexes:
                    for nr, nc in neighbors(r, c):
                        if (nr, nc) in occupied:
                            raise ValueError

                for r, c in indexes:
                    occupied.add((r, c))

                ships.append(cells)
                break
            except:
                print("Invalid ship placement. Try again.")

    return ships


def save_player_ships(ships, filename="data/player_ships.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ship_id", "size", "cells"])
        for i, ship in enumerate(ships):
            writer.writerow([i+1, len(ship), " ".join(ship)])
