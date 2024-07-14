import traceback
from colors_on_console import cc
from datetime import date


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(cc.GREEN, f"[LOG {date.today().ctime()}]\n", cc.RED, tb, cc.RESET)
