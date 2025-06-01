from time import sleep  # Wird hier nicht verwendet, könnte entfernt werden

# PyQt6-Klassen für Signale, Dateien, Textströme usw.
from PyQt6.QtCore import pyqtSlot, QFile, QIODevice, QTextStream, pyqtSignal
from PyQt6.QtGui import QAction  # Für Menüaktionen
from PyQt6.QtWidgets import (
    QMainWindow, QProgressBar, QStatusBar, QLabel,
    QMenuBar, QFileDialog, QMessageBox, QMenu
)

from CentralWidget import CentralWidget  # Import des selbst definierten zentralen Widgets

# Hauptfensterklasse der Anwendung
class MainWindow(QMainWindow):
    # Signal, das eine einzelne Textzeile (str) an andere Objekte senden kann
    write_line = pyqtSignal(str)

    def __init__(self, parent=None):  # Konstruktor des Hauptfensters
        super(MainWindow, self).__init__(parent)  # Konstruktor der Elternklasse aufrufen

        # Erstelle das zentrale Widget und verbinde das Signal mit dessen Slot
        central_widget = CentralWidget(self)
        self.write_line.connect(central_widget.add_line)  # Signal wird mit Methode verknüpft

        self.setCentralWidget(central_widget)  # Zentrales Widget im Fenster setzen

        # Fenster-Titel setzen und Größe festlegen
        self.setWindowTitle("Temperaturüberwachung")
        self.setFixedSize(800, 800)  # Feste Fenstergröße

        # Fortschrittsbalken und Label für den Dateinamen vorbereiten
        self.__progress_bar = QProgressBar()
        self.__label = QLabel("No file loaded")  # Anfangstext im Label

        # Statusleiste unten im Fenster einrichten
        status_bar = QStatusBar()
        status_bar.addWidget(self.__label)  # Dateiname anzeigen
        status_bar.addWidget(self.__progress_bar)  # Fortschrittsbalken anzeigen
        self.setStatusBar(status_bar)  # Als Statusleiste setzen

        # Menüleiste erstellen mit einem "Files"-Menü
        menu_bar = QMenuBar(self)
        files = QMenu("Files", menu_bar)  # Menü mit der Bezeichnung "Files"

        # Menüpunkt "Open ..." zum Öffnen von Dateien hinzufügen
        action_file_open = files.addAction("Open ...")
        action_file_open.triggered.connect(self.open_file)  # Klick löst Methode aus

        # "Files"-Menü zur Menüleiste hinzufügen
        menu_bar.addMenu(files)
        self.setMenuBar(menu_bar)  # Menüleiste im Fenster setzen

        # Standard-Dateifilter für Dateiauswahl definieren
        self.__initial_filter = "Log files (*.log)"
        self.__filter = self.__initial_filter + ";;All files (*)"  # Benutzer kann auch alle Dateien anzeigen

        # Startverzeichnis für Datei-Auswahl leer lassen
        self.__directory = ""

    @pyqtSlot()  # Slot-Dekorator für Qt-Signale
    def open_file(self):
        # Öffnet Dialogfenster zum Datei auswählen
        (path, self.__initial_filter) = QFileDialog.getOpenFileName(
            self, "Open File", self.__directory, self.__filter, self.__initial_filter
        )

        # Wenn ein Pfad ausgewählt wurde (Benutzer hat also nicht abgebrochen)
        if path:
            # Ordnerpfad extrahieren (bis zum letzten "/")
            self.__directory = path[:path.rfind("/")]
            # Nur Dateiname anzeigen (nach letztem "/")
            self.__label.setText(path[path.rfind("/") + 1:])

            file = QFile(path)  # QFile-Objekt mit Pfad erstellen

            # Versuche, die Datei im Lesemodus zu öffnen
            if not file.open(QIODevice.OpenModeFlag.ReadOnly):
                # Wenn Öffnen fehlschlägt, zeige Fehlermeldung an
                QMessageBox.information(self, "Unable to open file", file.errorString())
                return

            # Dateiinhalt mit QTextStream lesen
            stream = QTextStream(file)
            text_in_file = stream.readAll()  # Gesamter Dateiinhalt als Text
            lines = text_in_file.split("\n")  # In Zeilen aufteilen

            # Fortschrittsbalken auf die Anzahl der Zeilen setzen
            self.__progress_bar.setRange(0, len(lines))

            # Jede Zeile einzeln verarbeiten
            for i in range(len(lines)):
                self.write_line.emit(lines[i])  # Signal mit Zeile senden (an CentralWidget)
                self.__progress_bar.setValue(i + 1)  # Fortschritt aktualisieren

            file.close()  # Datei wieder schließen
