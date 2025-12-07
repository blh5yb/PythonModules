import tkinter as tk
from tkinter import ttk
from typing import List, Optional, Dict, Any
import tkinter.font as tkFont

OptionConfig = Dict[Any, Any]

class InputDialog(tk.Toplevel):
    """
    A dynamic dialog box that generates input widgets.
    """

    def __init__(self, parent, title: str, fields: List[Any]):
        super().__init__(parent)
        # --- FIX 1: Remove 'transient' so dialog is independent of hidden root ---
        # self.transient(parent)  <-- REMOVED
        # -------------------------------------------------------------------------
        self.root = parent
        self.title(title)

        # Hide initially so we can build it before showing
        self.withdraw()

        self.define_custom_font()

        # Storage
        self.widget_map: Dict[str, Any] = {}
        self.data_maps: Dict[str, Dict[str, Any]] = {}
        self.result: Optional[List[str]] = None
        self.fields = fields
        self.inputs = []
        self.options = []
        self.curr_row = 0
        self.curr_label = 0

        # --- FIX 2: Layout Configuration (Prevents "Empty" Window) ---
        # This tells the window to expand the frame to fill the space
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame = ttk.Frame(self, padding="20")
        self.frame.grid(row=0, column=0, sticky="nsew")
        # -------------------------------------------------------------

    def create_dialog_window(self):
        input_idx = 0
        for item in self.fields:
            form_field = item.get('form_field', None)
            item['widget_id'] = self.curr_label
            if form_field == 'input':
                self.create_inputs(item, input_idx)
                self.inputs.append(item)
                input_idx += 1
            elif form_field == 'combobox':
                self.create_combobox(item)
                self.options.append(item)
            elif form_field == 'listbox':
                self.create_listbox(item)
                self.options.append(item)
            else:
                print(f"Warning: Field {form_field} ignored.")

        self.create_buttons()

        # --- FIX 3: Force Window to Center and Appear ---
        self.center_and_show()
        # ------------------------------------------------

    def center_and_show(self):
        """Calculates size and centers on screen."""
        self.update_idletasks()  # Calculate required size

        width = self.frame.winfo_reqwidth() + 40  # Add padding buffer
        height = self.frame.winfo_reqheight() + 40

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

        self.deiconify()  # Show the window now
        self.lift()  # Bring to front
        self.attributes('-topmost', True)  # Keep on top
        self.focus_force()  # Force focus

        # Handle the 'X' button
        self.protocol('WM_DELETE_WINDOW', self.cancel)

    def create_inputs(self, input, index) -> None:
        disabled = input.get('disabled', False)
        label = input.get('label', f'Input {index}')
        type = input.get('type', 'password')
        default_value = input.get('default', '')

        ttk.Label(self.frame, text=label + ":").grid(row=self.curr_row, column=0, sticky="w", pady=5)

        widget_id = input['widget_id']
        entry_name = f'entry_{widget_id}'

        if type == 'password':
            entry = ttk.Entry(self.frame, width=40, show="*")
        else:
            entry = ttk.Entry(self.frame, width=40)

        if default_value:
            entry.insert(0, str(default_value))

        if disabled:
            entry.state(['disabled'])

        self.widget_map[entry_name] = entry
        entry.grid(row=self.curr_row, column=1, sticky="ew", padx=5, pady=5)
        self.curr_label = widget_id + 1
        self.curr_row += 1

    def create_combobox(self, option_config) -> None:
        widget_id = option_config['widget_id']
        info = option_config.get('info')
        display_to_data = {}
        display_values = []

        for item in info:
            display = item.get('value')
            data = item.get('data', display)
            display_values.append(display)
            display_to_data[display] = data

        map_key = f'map_{widget_id}'
        self.data_maps[map_key] = display_to_data
        default_value = display_values[0] if display_values else ''

        ttk.Label(self.frame, text=option_config['label'] + ":").grid(row=self.curr_row, column=0, sticky="w", pady=5)

        combobox_name = f'combobox_{widget_id}'
        combobox = ttk.Combobox(self.frame, values=display_values, state="readonly", width=38)
        combobox.set(default_value)
        self.widget_map[combobox_name] = combobox

        combobox.grid(row=self.curr_row, column=1, sticky="ew", padx=5, pady=5)
        self.curr_row += 1
        self.curr_label = widget_id + 1

    def create_listbox(self, option_config) -> None:
        selectmode = tk.MULTIPLE if option_config.get('multiple', False) else tk.SINGLE
        label = option_config.get('label', 'Select Option')
        info = option_config.get('info')
        widget_id = option_config['widget_id']
        disabled = option_config.get('disabled', False)

        display_to_data = {}
        display_values = []

        for item in info:
            display = item.get('value')
            data = item.get('data', display)
            display_values.append(display)
            display_to_data[display] = data

        map_key = f'map_{widget_id}'
        self.data_maps[map_key] = display_to_data

        ttk.Label(self.frame, text=label + ":").grid(row=self.curr_row, column=0, sticky="nw", pady=5)

        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)
        initial_state = tk.DISABLED if disabled else tk.NORMAL

        listbox = tk.Listbox(
            self.frame,
            selectmode=selectmode,
            height=min(len(info), 5),
            yscrollcommand=scrollbar.set,
            width=38,
            font=self.dialog_font,
            exportselection=False,
            state=initial_state
        )

        for idx, display in enumerate(display_values):
            listbox.insert(tk.END, display)
            if info[idx].get('selected', False):
                listbox.selection_set(idx)

        scrollbar.config(command=listbox.yview)
        listbox_name = f'listbox_{widget_id}'
        self.widget_map[listbox_name] = listbox

        listbox.grid(row=self.curr_row, column=1, sticky="ew", padx=5, pady=5)
        scrollbar.grid(row=self.curr_row, column=2, sticky='ns')

        self.curr_row += 1
        self.curr_label = widget_id + 1

    def create_buttons(self):
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=self.curr_row, column=0, columnspan=3, pady=10)

        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side="right", padx=5)
        ttk.Button(button_frame, text="OK", command=self.ok).pack(side="right", padx=5)

        # Bind keys
        self.bind("<Return>", lambda event: self.ok())
        self.bind("<Escape>", lambda event: self.cancel())
        self.curr_row += 1

    def define_custom_font(self):
        style = ttk.Style(self)
        default_font = tkFont.nametofont("TkDefaultFont")
        self.dialog_font = tkFont.Font(family=default_font.actual("family"), size=10)
        style.configure(".", font=self.dialog_font)

    def ok(self):
        self.result = []

        # 1. Collect Entry Inputs
        for input_config in self.inputs:
            widget_id = input_config['widget_id']
            entry = self.widget_map.get(f'entry_{widget_id}')
            if entry:
                self.result.append(entry.get())

        # 2. Collect Option Inputs
        for option_config in self.options:
            widget_id = option_config['widget_id']
            map_key = f'map_{widget_id}'
            display_to_data = self.data_maps.get(map_key, {})

            combobox_name = f'combobox_{widget_id}'
            listbox_name = f'listbox_{widget_id}'

            if combobox_name in self.widget_map:
                combobox = self.widget_map[combobox_name]
                display_text = combobox.get()
                self.result.append(display_to_data.get(display_text, display_text))

            elif listbox_name in self.widget_map:
                listbox = self.widget_map.get(listbox_name)
                selected_indices = listbox.curselection()
                display_items = [listbox.get(idx) for idx in selected_indices]
                final_list = [display_to_data.get(display, display) for display in display_items]
                self.result.append(final_list)

        # --- FIX 4: Only destroy self, do NOT quit root ---
        self.destroy()
        # --------------------------------------------------

    def cancel(self):
        self.result = None
        self.destroy()
