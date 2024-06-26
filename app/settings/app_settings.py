import logging
import logging.handlers
from pathlib import Path
from typing import Any, Union

from PyQt6.QtCore import QSettings, QStandardPaths
from PyQt6.QtWidgets import QApplication

from app.data.data_store import DataStore
from app.settings.app_config import AppConfig


class AppSettings:
    def __init__(self):
        self.settings: QSettings = None
        self.app_name: str = None
        self.app_dir: Union[Path, Any] = None
        self.docs_location: Path = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DocumentsLocation
            )
        )
        self.data: DataStore = None

    def init(self):
        self.app_name = QApplication.applicationName().lower()
        self.app_dir = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppConfigLocation
            )
        )
        self.app_dir.mkdir(exist_ok=True)
        settings_file = f"{self.app_name}.ini"
        self.settings = QSettings(
            self.app_dir.joinpath(settings_file).as_posix(), QSettings.Format.IniFormat
        )
        self.settings.sync()
        app_config = self.load_configuration()
        self.data = DataStore(app_config.notes_file)

    def init_logger(self):
        log_file = f"{self.app_name}.log"
        handlers = [
            logging.handlers.RotatingFileHandler(
                self.app_dir.joinpath(log_file), maxBytes=1000000, backupCount=1
            ),
            logging.StreamHandler(),
        ]

        logging.basicConfig(
            handlers=handlers,
            format="%(asctime)s - %(filename)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG,
        )
        logging.captureWarnings(capture=True)

    def save_window_state(self, geometry, window_state):
        self.settings.setValue("geometry", geometry)
        self.settings.setValue("windowState", window_state)
        self.settings.sync()

    def save_configuration(self, app_config: AppConfig):
        self.settings.setValue(AppConfig.NOTES_FILE_KEY, app_config.notes_file)
        self.settings.sync()
        self.data.update_store(app_config.notes_file)

    def load_configuration(self):
        app_config = AppConfig()
        app_config.notes_file = self.settings.value(
            AppConfig.NOTES_FILE_KEY,
            app_config.notes_file or f"{self.app_dir}/onepage.txt",
        )
        return app_config

    def geometry(self):
        return self.settings.value("geometry", None)

    def window_state(self):
        return self.settings.value("windowState", None)


app = AppSettings()
