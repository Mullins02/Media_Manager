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
        title_label = ttk.Label(
            self.root, text="Media Library", font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            container, orient="vertical", command=self.canvas.yview
        )

        self.scroll_frame = ttk.Frame(self.canvas)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create the scrollable window inside canvas
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scroll_frame, anchor="nw"
        )

        # Update scroll region whenever content changes
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        # Make inner frame match canvas width
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width),
        )

        for media_type, items in self.grouped_media.items():
            section_frame = ttk.LabelFrame(self.scroll_frame, text=media_type)
            section_frame.pack(fill="x", expand=True, pady=(5, 10), padx=5)

            for library_item, data in sorted(items.items(), key=lambda x: x[0].lower()):
                key = f"{media_type}|{library_item}"
                var = tk.BooleanVar(value=False)

                self.checkbox_vars[key] = {
                    "var": var,
                    "data": data,
                    "media_type": media_type,
                    "library_item": library_item,
                }

                checkbox_text = f"{library_item} ({len(data['files'])} files)"
                checkbox = ttk.Checkbutton(
                    section_frame, text=checkbox_text, variable=var
                )
                checkbox.pack(anchor="w", padx=10, pady=2)

        # Mouse wheel scrolling
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda event: self.canvas.yview_scroll(
                int(-1 * (event.delta / 120)), "units"
            ),
        )

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)

        show_selected_button = ttk.Button(
            button_frame, text="Show Selected", command=self.show_selected
        )
        show_selected_button.pack(side="left")

        rename_button = ttk.Button(
            button_frame, text="Rename Selected", command=self.rename_selected
        )
        rename_button.pack(side="left")

    def show_selected(self):
        selected_data = [
            info for info in self.checkbox_vars.values() if info["var"].get()
        ]
        for item in selected_data:
            logger.info(f'{item["library_item"]} | {item["media_type"]}')
            for file in item["data"]["files"]:
                logger.info(f'   ↪{file["filename"]}')

    def rename_selected(self):
        selected_data = [
            info for info in self.checkbox_vars.values() if info["var"].get()
        ]
        self.backend.rename_files(selected_data)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    app = MediaManagerUI(root)
    app.run()
