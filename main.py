from src.gameplay import gameplay_loop

if __name__ == "__main__":
    try:
        gameplay_loop()
    except KeyboardInterrupt:
        print("\nGame stopped. Bye!")
