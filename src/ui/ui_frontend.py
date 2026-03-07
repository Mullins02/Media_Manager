import tkinter as tk
from tkinter import ttk
import logging

from .ui_backend import UIBackend

logger = logging.getLogger(__name__)


class MediaManagerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Manager")
        self.root.geometry("500x600")

        self.backend = UIBackend()
        self.grouped_media = self.backend.grouped_media()

        self.checkbox_vars = {}

        self.build_ui()

    def build_ui(self):
        title_label = ttk.Label(self.root, text="Media Library", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        for media_type, items in self.grouped_media.items():
            section_label = ttk.Label(container, text=media_type, font=("Arial", 12, "bold"))
            section_label.pack(anchor="w", pady=(10, 5))

            section_frame = ttk.Frame(container)
            section_frame.pack(fill="x", padx=15)

            for library_item, data in sorted(items.items(), key=lambda x: x[0].lower()):
                key = f"{media_type}|{library_item}"
                var = tk.BooleanVar(value=False)
                self.checkbox_vars[key] = var

                checkbox_text = f"{library_item} ({len(data['files'])} files)"
                checkbox = ttk.Checkbutton(
                    section_frame,
                    text=checkbox_text,
                    variable=var
                )
                checkbox.pack(anchor="w")

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)

        show_selected_button = ttk.Button(
            button_frame,
            text="Show Selected",
            command=self.show_selected
        )
        show_selected_button.pack(side="left")

    def show_selected(self):
        selected = [key for key, var in self.checkbox_vars.items() if var.get()]
        logger.info(f"Selected items: {selected}")
        print("Selected items:")
        for item in selected:
            print(item)
            
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    app = MediaManagerUI(root)
    app.run()