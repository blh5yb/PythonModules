# TK Thread Safe Dialog Widget
This package properly queue's tkinter to allow the widget to gracefully exit to avoid race conditions that can affect
your downstream code

## Example Implementation
```python
from src.tk_safe_dialog.decorators import *

@tkinter_thread_safe
def run_dialog(fields, ctx: AutomationContext=None):
    result = ctx.ask_input(title="Weekly Determinations Runtime Options", fields=fields)

    if result:
        print('dialog result:', result)
        print(f"\n✅ Result Check:")
        # continue with downstream business logic
    else:
        print('Input cancelled.')

if __name__ == "__main__":
    fields=[
        {'form_field': 'input', 'label': 'Username', 'type': 'text', 'default': 'abc@123'}, {'form_field': 'input', 'label': 'Token', 'type': 'password'}, # return str
        {'form_field': 'listbox', 'label': 'LB Options', 'multiple': True, 'info': [ # returns a list
            {'value': 'Project 1 Display', 'data': 'PROJ_1_ID', 'selected': True},
            {'value': 'Project 2 Display', 'data': 'PROJ_2_ID', 'selected': False},
            {'value': 'Project 3 Display', 'data': 'PROJ_3_ID', 'selected': False},
        ]}, {'form_field': 'combobox', 'label': 'CB Options', 'info': [ # returns single str
            {'value': 'Project 1 Display', 'data': 'PROJ_1_ID'},
            {'value': 'Project 2 Display', 'data': 'PROJ_2_ID'},
            {'value': 'Project 3 Display', 'data': 'PROJ_3_ID'},
        ]},{'form_field': 'listbox', 'label': 'Other Options', 'multiple': True, 'info': [ # returns list
            {'value': 'DEV Environment', 'data': 'DEV_ENV', 'selected': True},
            {'value': 'QA Environment', 'data': 'QA_ENV', 'selected': False},
            {'value': 'PROD Environment', 'data': 'PROD_ENV', 'selected': False},
        ]}
    ]
    run_dialog(fields)
```

## Modules

### InputDialog - dialog_ui.py
Currently supports 3 form field types
  1. input: text field
     - password option hides the text value
     - returns str value (input text)
  2. combobox: simple select options
     - returns str value selected value)
  3. listbox: multiple select options
     - set whether multiple options are allow
     - 'selected' attributes tells whether is should be selected to start
     - returns list of selected value

#### Input
  - parent: tk.Tk()
  - title: widget title to display
  - fields: list of form fields with values

#### Output
  - results: an array of values for each form field in order of how they were input in the fields list

### DialogService - service.py
Queues the tkinter dialog task
Handles setup and teardown

### AutomationContext - decorators.py
Context manager to decouple the dialog widget from the business logic

### tkinter_thread_safe - decorators.py
Wraps the method calling the tkinter ask_input method to perform inversion of control for the business logic
Initializes the dialog service, starts the context manager and passes to the wrapped method. Stops the worker tasks once
completed