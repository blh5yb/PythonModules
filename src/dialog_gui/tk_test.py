from src.dialog_gui.decorators import AutomationContext, tkinter_thread_safe
from src.shared import CustomException


############## ------------- For Testing outside the main application ---------- #############################
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
    # result = InputDialog.get_input(
    #     title="Dynamic Configuration",
    #     fields=fields
    # )