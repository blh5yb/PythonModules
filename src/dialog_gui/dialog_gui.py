import tkinter as tk
from tkinter import ttk
from typing import List, Any, Optional, Dict
import tkinter.font as tkFont

OptionConfig = Dict[Any, Any]


class InputDialog(tk.Toplevel):
    """
    A dynamic dialog box that generates input widgets.
    """

    def __init__(self, parent, title: str, fields: List[Any], validate_callback=None):
        super().__init__(parent)

        # --- FIX 1: Remove 'transient' so dialog is independent of hidden root ---
        # self.transient(parent)  <-- REMOVED
        # -------------------------------------------------------------------------

        self.root = parent
        self.title(title)
        self.validate_callback = validate_callback

        # Hide initially so we can build it before showing
        self.withdraw()

        self.define_custom_font()

        # Storage
        self.widget_map: Dict[str, Any] = {}
        self.label_map: Dict[str, Any] = {} # to access outside
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

        self.error_label = tk.Label( # showing if a validation error exists
            self.frame,
            text="",
            fg="red",
            font=("Arial", 10, "bold"),
            wraplength=300,  # Wrap text if it's too long
            justify="left"
        )
        # -------------------------------------------------------------

    def get_widget(self, label: str):
        """Helper for the custom callback to find widgets by name."""
        return self.label_map.get(label)

    def get_labels(self):
        return self.label_map

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

        # NEW: Run initial logic triggers (e.g., disable fields based on default value)
        # We do this HERE, after all widgets are created, so 'get_widget' works.
        if hasattr(self, '_initial_triggers'):
            for trigger in self._initial_triggers:
                trigger()

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

        lbl = ttk.Label(self.frame, text=label + ":")# .grid(row=self.curr_row, column=0, sticky="w", pady=5)
        lbl.grid(row=self.curr_row, column=0, sticky="w", pady=5)
        self.widget_map[f'label_{label}'] = lbl

        widget_id = input['widget_id']
        entry_name = f'entry_{widget_id}'

        if type == 'password':
            entry = ttk.Entry(self.frame, width=40, show="*")
            show_pass_var = tk.BooleanVar(value=False)
            self.widget_map[f'show_var_{widget_id}'] = show_pass_var

            def toggle_password():
                if show_pass_var.get():
                    entry.config(show="")  # Empty string = visible
                else:
                    entry.config(show="*")  # Asterisk = hidden

            # Create the checkbox in Column 2 (Right of the entry)
            cb = ttk.Checkbutton(self.frame, text="Show", variable=show_pass_var, command=toggle_password)
            cb.grid(row=self.curr_row, column=2, sticky="w", padx=5)
            self.widget_map[f"check_box_{label}"] = cb
        else:
            entry = ttk.Entry(self.frame, width=40)

        if default_value:
            entry.insert(0, str(default_value))

        if disabled:
            entry.state(['disabled'])

        entry.hide = input.get('hide', [])
        entry.disable = input.get('disable', [])

        self.widget_map[entry_name] = entry
        self.label_map[input['label']] = entry
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
        label = option_config['label']

        lbl = ttk.Label(self.frame, text=label + ":")
        lbl.grid(row=self.curr_row, column=0, sticky="w", pady=5)
        self.widget_map[f'label_{label}'] = lbl

        combobox_name = f'combobox_{widget_id}'
        combobox = ttk.Combobox(self.frame, values=display_values, state="readonly", width=38)
        combobox.set(default_value)
        combobox.hide = option_config.get('hide', [])
        combobox.disable = option_config.get('disable', [])
        self.widget_map[combobox_name] = combobox
        self.label_map[option_config['label']] = combobox
        # Optionally pass in a callback to dynamically update fields (i.e. enabled/ disabled
        if option_config.get('callback', None):
            callback_func = option_config['callback']

            def on_change(event=None):
                # Run the user-provided logic, passing 'self' (the dialog)
                # so the function can access other widgets.
                callback_func(self, display_to_data[combobox.get()])

            combobox.bind("<<ComboboxSelected>>", on_change)

            # Save this trigger to run it AFTER all widgets are created
            if not hasattr(self, '_initial_triggers'):
                self._initial_triggers = []
            self._initial_triggers.append(on_change)

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

        lbl = ttk.Label(self.frame, text=label + ":")
        lbl.grid(row=self.curr_row, column=0, sticky="nw", pady=5)
        self.widget_map[f'label_{label}'] = lbl

        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.widget_map[f"scrollbar_{label}"] = scrollbar
        initial_state = tk.DISABLED if disabled else tk.NORMAL

        # Get the custom filter function from config (if it exists)
        # It should accept the item dict and return True if it should be disabled
        disable_check_func = option_config.get('disable_check', lambda x: False)

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

        # 1. NEW: Store the source data on the widget so we can read it later
        listbox.source_data = info
        listbox.hide = option_config.get('hide', [])
        listbox.disable = option_config.get('disable', [])

        # 2. NEW: Attach the disabled set to the widget (instead of a local variable)
        listbox.disabled_indices = set()

        for idx, item in enumerate(info):
            display = item.get('value')
            listbox.insert(tk.END, display)

            is_disabled = item.get('disabled', False) or disable_check_func(item)
            if is_disabled:
                # A. VISUAL: Make text grey
                listbox.itemconfig(idx, {'fg': '#aaaaaa', 'selectbackground': '#ffffff', 'selectforeground': '#aaaaaa'})
                # B. LOGIC: Track this index
                listbox.disabled_indices.add(idx)

            elif item.get('selected', False):
                listbox.selection_set(idx)
        listbox.bind('<<ListboxSelect>>', lambda e: self._enforce_disabled_options(listbox, listbox.disabled_indices))

        scrollbar.config(command=listbox.yview)
        listbox_name = f'listbox_{widget_id}'
        self.widget_map[listbox_name] = listbox
        self.label_map[option_config['label']] = listbox

        listbox.grid(row=self.curr_row, column=1, sticky="ew", padx=5, pady=5)
        scrollbar.grid(row=self.curr_row, column=2, sticky='ns')

        self.curr_row += 1
        self.curr_label = widget_id + 1

    @staticmethod
    def _enforce_disabled_options(listbox, disabled_indices):
        """
        Event handler that prevents selecting items marked as disabled.
        """
        # Get current selection (returns a tuple of indices)
        current_selection = listbox.curselection()

        for index in current_selection:
            if index in disabled_indices:
                # If user clicked a greyed-out item, instantly deselect it
                listbox.selection_clear(index)

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

    def show_error(self, message: str = None):
        """
        Displays an error message at the bottom of the dialog.
        If message is None or empty, hides the error field.
        """
        if message:
            self.error_label.config(text=message)
            # Grid it at the bottom (use a high row number like 999)
            # columnspan=3 ensures it spans across Label | Input | Scrollbar
            self.error_label.grid(row=999, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 0))

            # Optional: Play a system beep
            self.root.bell()
        else:
            # Hide it but remember settings
            self.error_label.grid_remove()

    def ok(self):
        self.show_error(None)
        self.result = []
        # Optional validation callback
        if self.validate_callback:
            # We pass 'self' so the callback can read widgets and set errors
            is_valid = self.validate_callback(self)

            # If validation failed, STOP here. Do not close window.
            if not is_valid:
                return

        for item in self.fields:
            form_field = item.get('form_field', None)

            widget_id = item['widget_id']
            map_key = f'map_{widget_id}'
            display_to_data = self.data_maps.get(map_key, {})

            if form_field == 'input':
                # item['widget_id'] = self.curr_label
                entry = self.widget_map.get(f'entry_{widget_id}')
                if entry:
                    self.result.append(entry.get())
            elif form_field == 'combobox':
                combobox_name = f'combobox_{widget_id}'
                combobox = self.widget_map[combobox_name]
                display_text = combobox.get()
                self.result.append(display_to_data.get(display_text, display_text))
            elif form_field == 'listbox':
                listbox_name = f'listbox_{widget_id}'
                listbox = self.widget_map.get(listbox_name)
                selected_indices = listbox.curselection()
                display_items = [listbox.get(idx) for idx in selected_indices]
                final_list = [display_to_data.get(display, display) for display in display_items]
                self.result.append(final_list)
            else:
                print(f"Warning: Field {form_field} ignored.")

        # --- FIX 4: Only destroy self, do NOT quit root ---
        self.destroy()
        # --------------------------------------------------

    def cancel(self):
        self.result = None
        self.destroy()
