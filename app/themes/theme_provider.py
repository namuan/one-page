from PyQt6.QtGui import QFont, QIcon, QFontDatabase


def configure_theme(app):
    app.setWindowIcon(QIcon("icons:app.ico"))

    QFontDatabase.addApplicationFont("fonts:JetBrainsMono-Regular.ttf")

    current_font: QFont = QFont("JetBrains Mono")
    current_font.setPointSize(14)
    app.setFont(current_font)
