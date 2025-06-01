from PyQt6.QtCore import pyqtSlot, QDateTime, pyqtSignal  # Import von PyQt6-Signalen und Datumszeit-Funktionalität
from PyQt6.QtGui import QFont                            # Import für Schriftarten und -gewicht
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser  # Import grundlegender Qt-Widgets

from ChartView import ChartView  # Import einer benutzerdefinierten Diagramm-Komponente

class CentralWidget(QWidget):  # Definition einer eigenen Widget-Klasse, die QWidget erweitert
    send_cpu_temperature = pyqtSignal(QDateTime, float)  # Signal zur Übertragung von CPU-Temperaturdaten an das Diagramm
    send_gpu_temperature = pyqtSignal(QDateTime, float)  # Signal zur Übertragung von GPU-Temperaturdaten an das Diagramm

    def __init__(self, parent=None):  # Konstruktor der Klasse
        super(CentralWidget, self).__init__(parent)  # Aufruf des Konstruktors der Elternklasse

        chart_view = ChartView(parent)  # Erzeuge ein Objekt vom Typ ChartView (das Diagramm)

        self.send_cpu_temperature.connect(chart_view.append_to_cpu)  # Verbinde Signal für CPU mit entsprechender Methode im Chart
        self.send_gpu_temperature.connect(chart_view.append_to_gpu)  # Verbinde Signal für GPU mit entsprechender Methode im Chart

        self.__text_browser = QTextBrowser()  # Erzeuge ein Textfeld zur Anzeige der Messzeilen

        layout = QVBoxLayout()  # Vertikales Layout (alles untereinander)
        layout.addWidget(chart_view)           # Füge das Diagramm dem Layout hinzu (oben)
        layout.addWidget(self.__text_browser)  # Füge das Textfeld hinzu (unten)

        self.setLayout(layout)  # Setze das Layout für das CentralWidget

    @pyqtSlot(str)  # Dekorator: Methode ist ein Slot, reagiert auf ein Signal mit einem String als Eingabe
    def add_line(self, line):  # Methode zum Einfügen einer Zeile in Textfeld + Diagramm
        tokens = line.split(" ")  # Zerlege die Zeile in Einzelteile (Datum, Typ, Temperatur)

        datetime = QDateTime.fromString(tokens[0], "yyyy-MM-dd_hh:mm:ss")  # Erstelle QDateTime aus dem ersten Teil

        temperature = float(tokens[2])  # Wandle Temperatur von Text in Zahl um

        if temperature > 88.0:  # Wenn Temperatur kritisch hoch ist (z. B. Überhitzung)
            cursor = self.__text_browser.textCursor()  # Hole aktuellen Cursor im Textfeld
            format = cursor.charFormat()               # Hole aktuelles Textformat
            format.setFontWeight(QFont.Weight.Bold)    # Setze Schrift auf fett
            cursor.setCharFormat(format)               # Wende Format auf Cursor an
            self.__text_browser.setTextCursor(cursor)  # Setze Cursor zurück (mit neuem Format)

        self.__text_browser.append(line)  # Zeile ins Textfeld schreiben

        if tokens[1] == "CPU":  # Wenn Messung von der CPU stammt
            self.send_cpu_temperature.emit(datetime, temperature)  # Signal mit Daten senden
        elif tokens[1] == "GPU":  # Wenn Messung von der GPU stammt
            self.send_gpu_temperature.emit(datetime, temperature)  # Signal mit Daten senden
        else:
            print("Token", tokens[1], "unbekannt.")  # Falls Typ nicht erkannt wird, in Konsole ausgeben

        if temperature > 88.0:  # Nach dem Einfügen Format wieder auf normal setzen
            cursor = self.__text_browser.textCursor()  # Aktuellen Cursor holen
            format = cursor.charFormat()               # Format holen
            format.setFontWeight(QFont.Weight.Normal)  # Fett wieder entfernen
            cursor.setCharFormat(format)               # Format anwenden
            self.__text_browser.setTextCursor(cursor)  # Cursor zurücksetzen
