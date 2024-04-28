from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QObject, QEvent, Qt


def command_u_is_pressed(event: QEvent) -> bool:
    return (event.type() == QtCore.QEvent.Type.KeyPress
            and event.key() == QtCore.Qt.Key.Key_U
            and event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier)


def command_b_is_pressed(event: QEvent) -> bool:
    return (event.type() == QtCore.QEvent.Type.KeyPress
            and event.key() == QtCore.Qt.Key.Key_B
            and event.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier)


class ScratchPadEvents(QObject):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app

    def eventFilter(self, source: QObject, event: QEvent):
        if event.type() == QtCore.QEvent.Type.FocusOut:
            self.save_scratch_pad()

        if command_u_is_pressed(event):
            highlight_color = Qt.GlobalColor.green
            selected_text_background_color = self.parent.txt_scratch_pad.textBackgroundColor()
            if selected_text_background_color == Qt.GlobalColor.green:
                self.parent.txt_scratch_pad.setTextBackgroundColor(Qt.GlobalColor.white)
            else:
                self.parent.txt_scratch_pad.setTextBackgroundColor(highlight_color)

        if command_b_is_pressed(event):
            if self.parent.txt_scratch_pad.fontWeight() == QtGui.QFont.Weight.Bold:
                self.parent.txt_scratch_pad.setFontWeight(QtGui.QFont.Weight.Normal)
            else:
                self.parent.txt_scratch_pad.setFontWeight(QtGui.QFont.Weight.Bold)

        return super().eventFilter(source, event)

    def save_scratch_pad(self):
        scratch = self.parent.txt_scratch_pad.toHtml()

        self.app.data.update_scratch_note(scratch)


class ScratchPadController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.events = ScratchPadEvents(self.parent, self.app)

        # installing event filter
        self.parent.txt_scratch_pad.installEventFilter(self.events)

    def init(self):
        scratch_note = self.app.data.get_scratch_note()
        self.parent.txt_scratch_pad.setHtml(scratch_note)

    def save_scratch_pad(self):
        self.events.save_scratch_pad()
