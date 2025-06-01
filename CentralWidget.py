from PyQt6.QtCore import pyqtSlot, QDateTime, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser

from ChartView import ChartView


class CentralWidget(QWidget):
    # Signale zum Übertragen von Temperaturdaten an das Diagramm
    send_cpu_temperature = pyqtSignal(QDateTime, float)
    send_gpu_temperature = pyqtSignal(QDateTime, float)

    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        # Erstelle das Diagramm (ChartView)
        chart_view = ChartView(parent)

        # Verbinde die Signale mit den Slots im ChartView
        self.send_cpu_temperature.connect(chart_view.append_to_cpu)
        self.send_gpu_temperature.connect(chart_view.append_to_gpu)

        # Textbereich für Temperaturzeilen
        self.__text_browser = QTextBrowser()

        # Layout definieren
        layout = QVBoxLayout()
        layout.addWidget(chart_view)           # Diagramm oben
        layout.addWidget(self.__text_browser)  # Textbrowser unten

        self.setLayout(layout)

    # Slot zum Hinzufügen einer Zeile in das Textfeld und Diagramm
    @pyqtSlot(str)
    def add_line(self, line):
        # Zeile zerlegen (Format z. B.: "2025-01-20_08:13:45 CPU 84.0")
        tokens = line.split(" ")

        # Datum extrahieren
        datetime = QDateTime.fromString(tokens[0], "yyyy-MM-dd_hh:mm:ss")

        # Temperatur extrahieren und in float umwandeln
        temperature = float(tokens[2])

        # Wenn Temperatur > 88, Text fett darstellen
        if temperature > 88.0:
            cursor = self.__text_browser.textCursor()
            format = cursor.charFormat()
            format.setFontWeight(QFont.Weight.Bold)
            cursor.setCharFormat(format)
            self.__text_browser.setTextCursor(cursor)

        # Zeile in Textfeld einfügen
        self.__text_browser.append(line)

        # An Diagramm übergeben je nach CPU oder GPU
        if tokens[1] == "CPU":
            self.send_cpu_temperature.emit(datetime, temperature)
        elif tokens[1] == "GPU":
            self.send_gpu_temperature.emit(datetime, temperature)
        else:
            # Optional: unbekannter Typ wird in der Konsole ausgegeben
            print("Token", tokens[1], "unbekannt.")

        # Schrift wieder auf normal setzen (damit nur betroffene Zeile fett ist)
        if temperature > 88.0:
            cursor = self.__text_browser.textCursor()
            format = cursor.charFormat()
            format.setFontWeight(QFont.Weight.Normal)
            cursor.setCharFormat(format)
            self.__text_browser.setTextCursor(cursor)
