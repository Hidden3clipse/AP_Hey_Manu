from time import sleep

from PyQt6.QtCore import pyqtSlot, QFile, QIODevice, QTextStream, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QMainWindow, QProgressBar, QStatusBar, QLabel,
    QMenuBar, QFileDialog, QMessageBox, QMenu
)

from CentralWidget import CentralWidget  # Import des zentralen Widgets


class MainWindow(QMainWindow):
    # Signal, das eine einzelne Textzeile sendet
    write_line = pyqtSignal(str)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Zentrales Widget instanziieren und als Hauptbereich setzen
        central_widget = CentralWidget(self)
        self.write_line.connect(central_widget.add_line)  # Signal mit Slot im CentralWidget verbinden

        self.setCentralWidget(central_widget)

        # Fenster-Eigenschaften setzen
        self.setWindowTitle("Temperaturüberwachung")
        self.setFixedSize(800, 800)

        # Fortschrittsbalken und Statuslabel vorbereiten
        self.__progress_bar = QProgressBar()
        self.__label = QLabel("No file loaded")

        # Statusleiste erstellen und Komponenten hinzufügen
        status_bar = QStatusBar()
        status_bar.addWidget(self.__label)
        status_bar.addWidget(self.__progress_bar)
        self.setStatusBar(status_bar)

        # Menüleiste und "Files"-Menü anlegen
        menu_bar = QMenuBar(self)
        files = QMenu("Files", menu_bar)

        # Menüeintrag "Open ..." zum Öffnen von Dateien
        action_file_open = files.addAction("Open ...")
        action_file_open.triggered.connect(self.open_file)  # Methode bei Klick ausführen

        # Menü zur Menüleiste hinzufügen
        menu_bar.addMenu(files)
        self.setMenuBar(menu_bar)

        # Standard-Dateifilter definieren
        self.__initial_filter = "Log files (*.log)"
        self.__filter = self.__initial_filter + ";;All files (*)"

        # Startverzeichnis leer lassen
        self.__directory = ""

    @pyqtSlot()
    def open_file(self):
        # Öffnet eine Datei-Auswahl-Dialogbox
        (path, self.__initial_filter) = QFileDialog.getOpenFileName(
            self, "Open File", self.__directory, self.__filter, self.__initial_filter
        )

        # Falls ein Pfad ausgewählt wurde
        if path:
            # Verzeichnis und Dateiname extrahieren
            self.__directory = path[:path.rfind("/")]
            self.__label.setText(path[path.rfind("/") + 1:])  # Dateiname in Statusleiste

            file = QFile(path)

            # Datei im Lesemodus öffnen
            if not file.open(QIODevice.OpenModeFlag.ReadOnly):
                QMessageBox.information(self, "Unable to open file", file.errorString())
                return

            # Dateiinhalt lesen
            stream = QTextStream(file)
            text_in_file = stream.readAll()
            lines = text_in_file.split("\n")

            # Fortschrittsbalken konfigurieren
            self.__progress_bar.setRange(0, len(lines))

            # Alle Zeilen an das CentralWidget senden
            for i in range(len(lines)):
                self.write_line.emit(lines[i])  # Signal senden
                self.__progress_bar.setValue(i + 1)  # Fortschritt aktualisieren

            file.close()  # Datei schließen
