"""Project entrypoint for launching the chess GUI."""


def main():
    try:
        from gui.display import main as run_game
    except ModuleNotFoundError as exc:
        if exc.name == "pygame":
            raise SystemExit(
                "pygame is not installed. Install it with `pip install pygame` and run the game again."
            ) from exc
        raise

    run_game()


if __name__ == "__main__":
    main()
