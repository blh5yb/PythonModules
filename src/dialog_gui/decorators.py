import functools
import threading
import traceback
from .service import DialogService
from ..shared import logger, CustomException


def ask_user_input(request_queue, result_queue, title, fields):
    request_queue.put({
        'action': 'show_input',
        'title': title,
        'fields': fields
    })
    return result_queue.get()

class AutomationContext:
    """
    Wraps the communication queues so the main logic
    doesn't need to deal with raw queue.put/get calls.
    """
    def __init__(self, request_queue, result_queue):
        self._req = request_queue
        self._res = result_queue

    def ask_input(self, title, fields):
        """Clean wrapper for asking user input."""
        return ask_user_input(self._req, self._res, title, fields)

    def quit_ui(self):
        """Signals the tkinter UI to close."""
        self._req.put({'action': 'quit'})


def tkinter_thread_safe(func):
    """
    Lifecycle Decorator.

    1. Initializes the UI Service (Main Thread).
    2. Spawns a background thread for the decorated function.
    3. Injects an 'AutomationContext' into the function.
    4. Starts the blocking UI Main Loop.
    5. Ensures clean shutdown when the function finishes or errors.
    """
    @functools.wraps(func)
    def wrapper(config, *args, **kwargs):
        print("DEBUG: Initializing UI Framework...")

        # 1. Initialize Service on Main Thread
        ui_service = DialogService()

        # 2. Create the Context Bridge
        ctx = AutomationContext(ui_service.request_queue, ui_service.result_queue)

        # 3. Define the Worker Task
        def worker_task():
            try:
                # Run the actual automation logic
                func(config, ctx, *args, **kwargs)
            except InterruptedError:
                logger.error(f'Process interrupted by user.')
            except CustomException:
                logger.error("User cancelled the dialog widget.")
            except Exception as e:
                print(f"CRITICAL ERROR: {e}")
                traceback.print_exc()
            finally:
                # CRITICAL: Always kill the UI loop when work is done
                print("Signaling UI to close.")
                ctx.quit_ui()

        # 4. Start the Background Thread
        worker = threading.Thread(target=worker_task, daemon=True)
        worker.start()

        # 5. Start the Blocking UI Loop (Main Thread)
        try:
            ui_service.start()
        except KeyboardInterrupt:
            print("Force killed by user.")

        # 6. Cleanup
        worker.join()
        print("Application Exit.")

    return wrapper