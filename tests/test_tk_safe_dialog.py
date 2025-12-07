import pytest
from unittest.mock import MagicMock, patch, call, ANY, call, ANY

import queue
from src.dialog_gui.decorators import *
import sys
import importlib

class FakeToplevel:
    """
    A dumb container that swallows calls to __init__
    and creates MagicMocks for any method called on it (like .withdraw()).
    """
    def __init__(self, master=None, cnf={}, **kw):
        # Swallow the init arguments so super().__init__ doesn't crash
        pass

    def __getattr__(self, name):
        # If the code calls self.withdraw() or self.geometry(), return a Mock
        return MagicMock()

@pytest.fixture(scope='class')
def mock_tk_inheritance():
    # 1. Create a fake tkinter module
    mock_tk = MagicMock()

    # 2. Assign our dumb class instead of MagicMock
    mock_tk.Toplevel = FakeToplevel

    # 3. Patch the modules
    with patch.dict(sys.modules, {
        'tkinter': mock_tk,
        'tkinter.ttk': MagicMock(),
        'tkinter.font': MagicMock()
    }):
        # 4. Import INSIDE the patch so it inherits from FakeToplevel
        import src.dialog_gui.dialog_gui as dialog_module
        importlib.reload(dialog_module)
        yield dialog_module.InputDialog

fields = [{'form_field': 'input', 'label': 'Test', 'default': '123'}]

@pytest.fixture(scope='class')
def tk_instance_setup(request, mock_tk_inheritance):
    """Initialize the InputDialog class"""
    InputDialogClass = mock_tk_inheritance

    parent = MagicMock()

    # This will now call MagicMock.__init__ instead of Toplevel.__init__
    mock_dialog_instance = InputDialogClass(parent, "Test Title", fields)

    request.cls.tk_instance = mock_dialog_instance
    yield mock_dialog_instance

@pytest.mark.usefixtures('tk_instance_setup')
class TestInputDialog:
    tk_instance: MagicMock = None
    def test_collect_results_ok(self):
        """
        Verify that clicking OK collects data from the widgets.
        """
        fields = [
            {'form_field': 'input', 'label': 'User'},
            {'form_field': 'combobox', 'label': 'Env', 'info': [{'value': 'A', 'data': 'DATA_A'}]},
            {'form_field': 'listbox', 'label': 'LB_Label', 'info': [{'value': 'B', 'data': 'DATA_B', 'selected': True}]},
        ]
        self.tk_instance.fields = fields

        self.tk_instance.create_dialog_window()

        # 2. Mock the internal widgets and their .get() methods
        # We have to manually inject mocks into widget_map because we aren't running real mainloop
        mock_entry = MagicMock()
        mock_entry.get.return_value = "my_username"

        mock_combo = MagicMock()
        mock_combo.get.return_value = "A"

        mock_listbox = MagicMock()
        mock_listbox.get.return_value = "B"
        mock_listbox.curselection.return_value = [0]

        self.tk_instance.widget_map['entry_0'] = mock_entry
        self.tk_instance.widget_map['combobox_1'] = mock_combo
        self.tk_instance.widget_map['listbox_2'] = mock_listbox

        # 3. Simulate clicking OK
        # We mock destroy/quit so the test doesn't error out
        self.tk_instance.destroy = MagicMock()
        self.tk_instance.root.quit = MagicMock()

        self.tk_instance.ok()

        # 4. Assertions
        assert self.tk_instance.result[0] == "my_username"
        assert self.tk_instance.result[1] == "DATA_A"  # Should return the data value, not display value
        assert self.tk_instance.result[2] == ["DATA_B"]  # Should return the data value, not display value

@pytest.fixture(scope='class')
def mock_dialog_service_setup(request):
    """Initialize the InputDialog class"""
    with patch('src.dialog_gui.decorators.DialogService') as mock_dialog_service_cls:
        mock_service_instance = mock_dialog_service_cls.return_value
        mock_service_instance.request_queue = queue.Queue()
        mock_service_instance.result_queue = queue.Queue()
        mock_service_instance.start = MagicMock()
        mock_service_instance.check_queue = MagicMock()
        request.cls.dialog_service_instance = mock_service_instance

        yield mock_service_instance

@pytest.mark.usefixtures('mock_dialog_service_setup')
class TestDecorator:
    dialog_service_instance: MagicMock = None
    def test_automation_context_communication(self):
        """
        Verify the Context object puts the correct data into the queue.
        """
        req_q = queue.Queue()
        res_q = queue.Queue()
        ctx = AutomationContext(req_q, res_q)

        # Test quit_ui
        ctx.quit_ui()
        item = req_q.get()
        assert item['action'] == 'quit'

    def test_decorator_flow(self):
        """
        Test the full lifecycle of the decorator without launching a real GUI.
        """
        # dummy function to be decorated to test the wrapper logic
        self.dialog_service_instance.request_queue = MagicMock()
        self.dialog_service_instance.request_queue.put = MagicMock()
        self.dialog_service_instance.result_queue = MagicMock()
        self.dialog_service_instance.result_queue.put = MagicMock()
        @tkinter_thread_safe
        def my_automation(config, ctx):
            assert isinstance(ctx, AutomationContext)
            config['was_run'] = True
            ctx.ask_input('title', [])

        test_config = {'was_run': False}
        my_automation(test_config)

        self.dialog_service_instance.request_queue.put.assert_has_calls([
            call({'action': 'show_input', 'title': 'title', 'fields': []}),
            call({'action': 'quit'})
        ])
        assert test_config['was_run'] == True

    def test_decorator_handles_exception(self):
        """
        Verify that if the automation crashes, the UI is still told to quit.
        """
        self.dialog_service_instance.reset_mock()
        self.dialog_service_instance.request_queue = queue.Queue()
        self.dialog_service_instance.result_queue = queue.Queue()
        @tkinter_thread_safe
        def crashing_automation(config, ctx):
            raise ValueError("Boom")

        # Run it
        crashing_automation({})

        # Verify quit was sent to queue despite the crash
        # We check if put was called with action: quit
        # args, _ = self.dialog_service_instance.request_queue.put.call_args
        # assert args[0]['action'] == 'quit'
        item = self.dialog_service_instance.request_queue.get(timeout=1)
        assert item['action'] == 'quit'


@pytest.fixture(scope='class')
def mock_queue():
    with patch('src.dialog_gui.service.queue') as queue_mock:
        queue_mock.Empty = Exception
        queue_mock.Queue.return_value.put = MagicMock()
        queue_mock.Queue.return_value.get = MagicMock()
        queue_mock.Queue.return_value.get_nowait = MagicMock()
        yield queue_mock

@pytest.fixture(scope='class')
def dialog_service_instance_setup(request, mock_queue):
    """Initialize the InputDialog class"""
    with patch('src.dialog_gui.service.tk.Tk') as mock_root:
        dialog_service_instance = DialogService()
        request.cls.dialog_service_instance = dialog_service_instance
        request.cls.mock_queue = mock_queue

        yield dialog_service_instance

@pytest.mark.usefixtures('dialog_service_instance_setup')
class TestService:
    dialog_service_instance: MagicMock = None
    def test_start(self):
        self.dialog_service_instance.start()
        self.dialog_service_instance.root.mainloop.assert_called_once()

    @pytest.mark.parametrize(
        'action', ['show_input', 'quit']
    )
    @patch('src.dialog_gui.service.InputDialog')
    def test_check_queue(self, mock_input_dialog, action):
        mock_input_dialog.return_value.create_dialog_window = MagicMock()
        mock_input_dialog.return_value.result = ['res1', 'res2']
        self.dialog_service_instance.request_queue.get_nowait.return_value = {'action': action, 'title': 'title', 'fields': []}

        self.dialog_service_instance.root.withdraw.reset_mock()
        self.dialog_service_instance.check_queue()
        if action == 'show_input':
            self.dialog_service_instance.root.withdraw.assert_called_once()
            mock_input_dialog.assert_called_once_with(self.dialog_service_instance.root, 'title', [])
            mock_input_dialog.return_value.create_dialog_window.assert_called_once()
            self.dialog_service_instance.root.wait_window.assert_called_once_with(mock_input_dialog.return_value)
            self.dialog_service_instance.result_queue.put.assert_called_once_with(mock_input_dialog.return_value.result)
        else:
            self.dialog_service_instance.root.destroy.assert_called_once()

        self.dialog_service_instance.root.after.assert_called()
