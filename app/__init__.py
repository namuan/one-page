__version__ = "0.4.0"
__appname__ = "OnePage"
__description__ = "Simple ScratchPad"
__desktopid__ = "dev.deskriders.OnePage"

from pathlib import Path

from PyQt6.QtCore import QDir

resources_path = Path(__file__).parent.parent / "resources"
QDir.addSearchPath('themes', resources_path.joinpath("themes").as_posix())
QDir.addSearchPath('images', resources_path.joinpath("images").as_posix())
QDir.addSearchPath('fonts', resources_path.joinpath("fonts").as_posix())
QDir.addSearchPath('icons', resources_path.joinpath("icons").as_posix())
