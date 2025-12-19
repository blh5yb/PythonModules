from src.dialog_gui.decorators import AutomationContext, tkinter_thread_safe
from src.shared import CustomException
from src.dialog_gui.types import FormConfiguration, combobox_field, option, input_field, listbox_field
import random

############## ------------- For Testing outside the main application ---------- #############################
import darkdetect

THEME_COLORS = {
  "light": {
    "text": "black", "disabled_text": "#aaaaaa", "bg": "white", "disabled_select_bg": "white",
    "select_bg": "#0078d7"
  },
  "dark": {
    "text": "white", "disabled_text": "#666666",
    "bg": "#2d2d2d",
    "disabled_select_bg": "#2d2d2d",
    "select_bg": "#0078d7"
  }
}
import sys
def get_current_theme(): # Returns 'dark' or 'light'
    mode = darkdetect.theme() if darkdetect else 'light'
    return mode.lower() if mode and sys.platform != 'win32' else 'light'

# Load the colors for the current mode current_mode = get_current_theme() PALETTE = THEME_COLORS[current_mode]

@tkinter_thread_safe
def run_dialog(fields, ctx: AutomationContext=None):
    result = ctx.ask_input(title="Weekly Determinations Runtime Options", fields=fields)

    if result:
        # username, token, project_id_list, env_list = result
        print('dialog result:', result)
        print(f"\n✅ Result Check:")
        # print(f"   Project IDs Retrieved (Should be IDs): {project_id_list}")
        # print(f"   Environments Retrieved (Should be IDs): {env_list}")
    else:
        print('Input cancelled.')
        raise CustomException('Input cancelled.')

def toggle_listbox_values(options_list, mode):
    """
    Updates field states AND individual listbox item availability
    based on the selected mode.
    """
    current_mode = get_current_theme()
    colors = THEME_COLORS[current_mode]
    # Clear current disabled states (start fresh)
    options_list.disabled_indices.clear()

    # Iterate over the stored data to re-evaluate logic
    for index, item_data in enumerate(options_list.source_data):
        should_disable = False

        # Example: If mode is 'field', disable items don't have something configured
        if mode == 'second' and not item_data.get('field', False):
            should_disable = True

        # Apply Visuals and Logic
        if should_disable:
            # Grey it out
            options_list.itemconfig(index, {
                'fg': colors['disabled_text'], # '#aaaaaa',
                'selectbackground': colors['disabled_select_bg'], # '#ffffff',
                'selectforeground': colors['disabled_text'] # '#aaaaaa'
                })
            # Add to block list
            options_list.disabled_indices.add(index)

            # optional: Deselect if it was currently selected
            if options_list.selection_includes(index):
                options_list.selection_clear(index)
        else:
            # Restore normal look
            options_list.itemconfig(index, {
                'fg': colors['text'],
                'selectbackground': colors['select_bg'],
                'selectforeground': 'white'
            })
            if item_data.get('selected', False):
                options_list.selection_set(index)

def toggle_fields(dialog, value):
    """
    Custom logic to enable/disable fields based on Combobox selection.
    """
    def set_visibility(widget, label, visible):
        if not widget: return

        if visible:
            # .grid() restores it to its remembered position
            widget.grid()
            if label: label.grid()
        else:
            # .grid_remove() hides it but remembers options
            widget.grid_remove()
            if label: label.grid_remove()

    # 1. Get references to the target widgets using their Labels
    # (Make sure these match the 'label' in your fields config exactly)
    labels = dialog.get_labels()
    for label_text in labels.keys():
        item = dialog.get_widget(label_text)
        label = dialog.widget_map.get(f"label_{label_text}")
        scrollbar = dialog.widget_map.get(f"scrollbar_{label_text}")
        checkbox = dialog.widget_map.get(f"check_box_{label_text}")

        if item: item.config(state='normal') # start normal
        if item.hide and value in item.hide:
            if item: set_visibility(item, label, False)
            if item: set_visibility(item, scrollbar, False)
            if item: set_visibility(item, checkbox, False)

        else:
            if item: set_visibility(item, label, True)
            if item: set_visibility(item, scrollbar, True)
            if item: set_visibility(item, checkbox, True)

            if value in item.disable: # only need to worry about disabling if visable
                if item: item.config(state='disabled')

    options_list = dialog.get_widget("Mode 2 Options")
    if options_list:
        toggle_listbox_values(options_list, value)

if __name__ == "__main__":
    fields: FormConfiguration = [
        combobox_field(
            label='Mode',
            info=[option(value='Mode 1', data='first'), option(value='Mode 2', data='second')],
            default='Mode 1',
            callback=toggle_fields,
        ),
        input_field(
            label='Username', type='text', default='user name', # disabled=(not config.get('dates_enabled', True)),
            hide=['second']
        ),
        input_field(
            label='Email', type='text', default='email', # disabled=(not config.get('dates_enabled', True)),
            hide=['first']
        ),
        input_field(
            label='Password', type='password', default='password', # disabled=(not config.get('dates_enabled', True)),
        ),
        combobox_field(
            label='Mode 1 Options',
            info=[
                option(value='Project 1 Display', data='PROJ_1_ID'),
                option(value='Project 2 Display', data='PROJ_2_ID'),
                option(value='Project 3 Display', data='PROJ_3_ID')
            ], hide=['second']
        ),
        listbox_field(
            label='Mode 2 Options', multiple=True, hide=['first'],
            info=[
                option(
                    value='Project 1 Display', data='PROJ_1_ID', selected=False,
                    field=random.choice([True, False]) # extra field for my callback filter
                ),
                option(
                    value='Project 2 Display', data='PROJ_2_ID', selected=False,
                    field=random.choice([True, False]) # extra field for my callback filter
                ),
                option(
                    value='Project 3 Display', data='PROJ_3_ID', selected=False,
                    field=random.choice([True, False]) # extra field for my callback filter
                )
            ]
        ),
        listbox_field(
            label='Options - Always Visible', multiple=True,
            info=[
                option(value='DEV Environment', data='DEV_ENV', selected=random.choice([True, False])),
                option(value='QA Environment', data='QA_ENV', selected=random.choice([True, False])),
                option(value='PROD Environment', data='PROD_ENV', selected=random.choice([True, False]))
            ]
        ),
    ]
    run_dialog(fields)
    # result = InputDialog.get_input(
    #     title="Dynamic Configuration",
    #     fields=fields
    # )