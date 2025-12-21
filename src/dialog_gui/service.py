import tkinter as tk
import queue
from .dialog_gui import InputDialog

class DialogService:
    def __init__(self):
        """Queue the Input Dialog widget and handle startup and teardown in a thread safe way."""
        self.root = tk.Tk()
        # --- FIX 5: Ensure Root is strictly hidden ---
        self.root.withdraw()
        # ---------------------------------------------

        self.request_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.check_queue()

    def start(self):
        print("[UI Thread] Service Started.")
        self.root.mainloop()

    def check_queue(self):
        try:
            task = self.request_queue.get_nowait()
            if task['action'] == 'show_input':
                print(f"[UI Thread] Showing Dialog: {task['title']}")

                # Double check root is hidden before showing child
                self.root.withdraw()

                dialog = InputDialog(self.root, task['title'], task['fields'], task['validate_callback'])
                print('dialog', dialog)
                dialog.create_dialog_window()

                # Block only until dialog is destroyed
                self.root.wait_window(dialog)
                self.result_queue.put(dialog.result)

            elif task['action'] == 'quit':
                print("[UI Thread] Quitting...")
                self.root.destroy()
                return
        except queue.Empty:
            pass

        self.root.after(100, self.check_queue)