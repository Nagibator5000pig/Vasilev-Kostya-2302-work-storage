from src.log_config import setup_logging
from src.gui.app import App


def main():
    setup_logging()
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
