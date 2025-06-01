from datetime import datetime  # Für Datum-/Zeitoperationen, wird hier aber nicht direkt verwendet

# Importiere Klassen für Diagramme (Chart, Achsen, Linien)
from PyQt6.QtCharts import (
    QChartView, QChart, QDateTimeAxis, QValueAxis, QSplineSeries
)

from PyQt6.QtCore import Qt, QDateTime, pyqtSlot  # Importiere Qt-Achsen-Ausrichtung, Datumstypen und Slot-Makro
from PyQt6.QtWidgets import QStatusBar  # Wird hier nicht verwendet, evtl. für spätere Erweiterungen

# Definition einer Klasse, die für die Anzeige eines Temperaturdiagramms zuständig ist
class ChartView(QChartView):  # ChartView erbt von QChartView (eine Art Qt-Widget für Diagramme)
    def __init__(self, parent=None):  # Konstruktor der Klasse
        super(ChartView, self).__init__(parent)  # Aufruf des Elternkonstruktors

        chart = QChart()  # Erstelle ein leeres Diagramm (Chart)
        chart.setTitle("Temperaturverlauf")  # Setze einen Titel für das Diagramm

        # QSplineSeries erzeugt eine glatte Linie — hier für CPU-Temperatur
        self.__temperature_cpu = QSplineSeries()  # Interne Variable für CPU-Datenreihe
        self.__temperature_cpu.setName("CPU")     # Benennung der Datenreihe (für Legende)

        # QSplineSeries auch für GPU-Temperatur
        self.__temperature_gpu = QSplineSeries()  # Interne Variable für GPU-Datenreihe
        self.__temperature_gpu.setName("GPU")     # Benennung der Datenreihe

        # Zeitachse (X-Achse): zeigt Uhrzeiten an
        axis_datetime = QDateTimeAxis()  # X-Achse für Zeit
        axis_datetime.setFormat("hh:mm:ss")  # Format der Zeitbeschriftung auf der Achse
        axis_datetime.setTitleText("Zeit")   # Achsentitel

        # Start- und Endzeit der Zeitachse festlegen
        start_datetime = QDateTime(2025, 1, 20, 8, 13, 0)  # Startzeitpunkt
        end_datetime = QDateTime.fromString("2025-01-20_08:14:30", "yyyy-MM-dd_hh:mm:ss")  # Endzeitpunkt
        axis_datetime.setRange(start_datetime, end_datetime)  # Bereich setzen

        # Temperaturachse (Y-Achse): zeigt Temperatur in Grad
        axis_temperature = QValueAxis()  # Y-Achse für numerische Werte
        axis_temperature.setRange(50.0, 90.0)  # Wertebereich der Achse
        axis_temperature.setTitleText("Temperatur in Grad Celsius")  # Achsentitel

        # Füge beide Datenreihen zum Diagramm hinzu
        chart.addSeries(self.__temperature_cpu)
        chart.addSeries(self.__temperature_gpu)

        # Füge beide Achsen zum Diagramm hinzu
        chart.addAxis(axis_datetime, Qt.AlignmentFlag.AlignBottom)  # Zeitachse unten
        chart.addAxis(axis_temperature, Qt.AlignmentFlag.AlignLeft)  # Temperaturachse links

        # Verbinde CPU-Serie mit beiden Achsen
        self.__temperature_cpu.attachAxis(axis_datetime)     # X-Achse (Zeit)
        self.__temperature_cpu.attachAxis(axis_temperature)  # Y-Achse (Temperatur)

        # Verbinde GPU-Serie mit beiden Achsen
        self.__temperature_gpu.attachAxis(axis_datetime)     # X-Achse (Zeit)
        self.__temperature_gpu.attachAxis(axis_temperature)  # Y-Achse (Temperatur)

        self.setChart(chart)  # Setze das konfigurierte Diagramm in die Ansicht (ChartView)

    # Slot für das Hinzufügen eines neuen Werts zur CPU-Datenreihe
    @pyqtSlot(QDateTime, float)  # Dekorator: Diese Methode empfängt Datum und Temperatur
    def append_to_cpu(self, datetime, temperature):
        # Konvertiert Datum in Millisekunden (Unix-Timestamp) und fügt Wert zur CPU-Serie hinzu
        self.__temperature_cpu.append(datetime.toMSecsSinceEpoch(), temperature)

    # Slot für das Hinzufügen eines neuen Werts zur GPU-Datenreihe
    @pyqtSlot(QDateTime, float)
    def append_to_gpu(self, datetime, temperature):
        # Auch hier: Datum in Millisekunden umrechnen und der GPU-Serie hinzufügen
        self.__temperature_gpu.append(datetime.toMSecsSinceEpoch(), temperature)
