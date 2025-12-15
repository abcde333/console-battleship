from src.ship_input import read_player_ships, save_player_ships

def main():
    player_ships = read_player_ships()
    save_player_ships(player_ships)
    print("Player ships saved to data/player_ships.csv")

if __name__ == "__main__":
    main()
