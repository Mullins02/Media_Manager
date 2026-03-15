import logging
import tkinter as tk

from ui import MediaManagerUI
from utils.logger import setup_logger

setup_logger(debug=False)

logger = logging.getLogger(__name__)

logger.info("Starting Media Manager")


def main():
    root = tk.Tk()
    app = MediaManagerUI(root)
    app.run()


if __name__ == "__main__":
    main()
