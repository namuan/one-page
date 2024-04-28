from PyQt6.QtGui import QKeySequence
from PyQt6.QtGui import QShortcut


class ShortcutController:
    def __init__(self, parent_window, app):
        self.parent = parent_window
        self.app = app

    def init_items(self):
        short = QShortcut(QKeySequence("Ctrl+S"), self.parent)
        short.activated.connect(self.parent.scratch_pad_controller.save_scratch_pad)
        config = QShortcut(QKeySequence("Ctrl+,"), self.parent)
        config.activated.connect(self.parent.config_controller.show_dialog)
