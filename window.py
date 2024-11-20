import sys
from PyQt5.QtWidgets import QDesktopWidget, QApplication
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

from siui.core import SiColor, SiGlobal
from siui.templates.application.application import SiliconApplication

from gui.components.page_homepage import GUIHomepage
from gui.components.page_functional import GUIDownloadPage
from gui.components.page_about import About

from version import show_version_message


class GUIWindow(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        screen_geo = QDesktopWidget().screenGeometry()
        self.setMinimumSize(1024, 300)
        self.resize(1280, 800)
        self.move((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2)
        self.layerMain().setTitle("Hanime!")
        self.setWindowTitle("Hanime!")
        self.setWindowIcon(QIcon("assets/icons/tab_logo_new.png"))

        self.layerMain().addPage(GUIHomepage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
                                 hint="主页", side="top")
        self.layerMain().addPage(GUIDownloadPage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_arrow_download_filled"),
                                 hint="Download", side="top")

        self.layerMain().addPage(About(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_info_filled"),
                                 hint="关于", side="bottom")

        SiGlobal.siui.reloadAllWindowsStyleSheet()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = GUIWindow()
    window.show()

    timer = QTimer(window)
    timer.singleShot(500, lambda: show_version_message(window))

    sys.exit(app.exec_())
