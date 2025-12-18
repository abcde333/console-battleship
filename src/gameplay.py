import csv
import random
from src.utils import BOARD_SIZE, in_bounds, neighbours, coord_to_index, index_to_coord
from src.ship_input import read_player_ships, save_ships
from src.bot_generation import generate_bot_ships, save_bot_ships

GAME_STATE_FILE = "data/game_state.csv"

# ---------- CSV ----------

def init_game_state_csv():
    with open(GAME_STATE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "turn",
            "player_move", "player_result",
            "bot_move", "bot_result",
            "player_board",
            "bot_board"
        ])

# ---------- BOARD ----------

def board_to_string(board):
    # превращаем доску в строку, каждая строка доски на новой линии
    return "\n".join(" ".join(cell for cell in row) for row in board)


# ---------- CSV ----------

def save_game_state(turn, p_move, p_res, b_move, b_res, p_board, b_board):
    with open(GAME_STATE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        row = [turn, p_move, p_res, b_move, b_res]
        row.extend([" ".join(r) for r in p_board])  # player_board rows as separate columns
        row.extend([" ".join(r) for r in b_board])  # bot_board rows as separate columns
        writer.writerow(row)



# ---------- BOARD ----------

def init_board():
    return [["~"] * BOARD_SIZE for _ in range(BOARD_SIZE)]

def print_board(board, hide_ships=False):
    print("   " + " ".join(str(i) for i in range(1, BOARD_SIZE + 1)))
    for i, row in enumerate(board):
        out = []
        for cell in row:
            if hide_ships and cell == "S":
                out.append("~")
            else:
                out.append(cell)
        print(f"{chr(i + ord('A'))}  " + " ".join(out))

def place_ships(board, ships):
    for ship in ships.values():
        for coord in ship:
            r, c = coord_to_index(coord)
            board[r][c] = "S"

def mark_misses(board, ship):
    for coord in ship:
        r, c = coord_to_index(coord)
        for nr, nc in neighbours(r, c):
            if board[nr][nc] == "~":
                board[nr][nc] = "M"

def read_ships_from_csv(path):
    ships = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            ship_id = int(row["ship_id"])
            cell = row["cell"]
            ships.setdefault(ship_id, []).append(cell)
    return ships

# ---------- GAMEPLAY ----------

def gameplay_loop():
    player_board = init_board()
    bot_board = init_board()

    player_hits = set()
    bot_hits = set()

    destroyed_player = set()
    destroyed_bot = set()

    # --- ship input ---
    player_ships = read_player_ships()
    save_ships(player_ships, "data/player_ships.csv")

    bot_ships = generate_bot_ships()
    save_bot_ships(bot_ships, "data/bot_ships.csv")

    player_ships = read_ships_from_csv("data/player_ships.csv")
    bot_ships = read_ships_from_csv("data/bot_ships.csv")

    place_ships(player_board, player_ships)

    init_game_state_csv()

    turn = 1

    while True:
        print(f"\n--- TURN {turn} ---")
        print("\nYour board:")
        print_board(player_board)

        print("\nBot board:")
        print_board(bot_board, hide_ships=True)

        # ---------- PLAYER ----------
        while True:
            try:
                move = input("Your move (e.g., A1, B5): ").upper()
                if move in player_hits:
                    print("Already shot there. Try again.")
                    continue
                r, c = coord_to_index(move)
                if not in_bounds(r, c):
                    print("Out of bounds, try again.")
                    continue
                break
            except KeyboardInterrupt:
                print("\nGame interrupted by user. Exiting...")
                exit()
            except Exception:
                print("Invalid input, try again.")

        player_hits.add(move)
        p_result = "Miss"

        for sid, ship in bot_ships.items():
            if move in ship:
                bot_board[r][c] = "X"
                p_result = "Hit"

                if all(cell in player_hits for cell in ship) and sid not in destroyed_bot:
                    destroyed_bot.add(sid)
                    mark_misses(bot_board, ship)
                    p_result = "Ship destroyed"
                break
        else:
            bot_board[r][c] = "M"

        # ---------- BOT ----------
        while True:
            rb = random.randint(0, BOARD_SIZE - 1)
            cb = random.randint(0, BOARD_SIZE - 1)
            bot_move = index_to_coord(rb, cb)
            if bot_move not in bot_hits:
                break

        bot_hits.add(bot_move)
        b_result = "Miss"

        for sid, ship in player_ships.items():
            if bot_move in ship:
                player_board[rb][cb] = "X"
                b_result = "Hit"

                if all(cell in bot_hits for cell in ship) and sid not in destroyed_player:
                    destroyed_player.add(sid)
                    mark_misses(player_board, ship)
                    b_result = "Ship destroyed"
                break
        else:
            player_board[rb][cb] = "M"

        save_game_state(
            turn,
            move, p_result,
            bot_move, b_result,
            player_board, bot_board
        )

        if len(destroyed_bot) == len(bot_ships):
            print("YOU WIN!")
            break

        if len(destroyed_player) == len(player_ships):
            print("BOT WINS!")
            break

        turn += 1

# --- запуск через main ---
if __name__ == "__main__":
    try:
        gameplay_loop()
    except KeyboardInterrupt:
        print("\nGame stopped. Bye!")
