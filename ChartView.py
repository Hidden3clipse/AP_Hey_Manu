from datetime import datetime

from PyQt6.QtCharts import (
    QChartView, QChart, QDateTimeAxis, QValueAxis, QSplineSeries
)
from PyQt6.QtCore import Qt, QDateTime, pyqtSlot
from PyQt6.QtWidgets import QStatusBar


class ChartView(QChartView):
    def __init__(self, parent=None):
        super(ChartView, self).__init__(parent)

        # Erstelle ein neues Chart-Objekt (Diagramm)
        chart = QChart()
        chart.setTitle("Temperaturverlauf")  # Titel des Diagramms

        # Erstelle eine Spline-Serie für CPU-Temperatur
        self.__temperature_cpu = QSplineSeries()
        self.__temperature_cpu.setName("CPU")

        # Erstelle eine Spline-Serie für GPU-Temperatur
        self.__temperature_gpu = QSplineSeries()
        self.__temperature_gpu.setName("GPU")

        # Erstelle eine Zeitachse (X-Achse)
        axis_datetime = QDateTimeAxis()
        axis_datetime.setFormat("hh:mm:ss")  # Anzeigeformat
        axis_datetime.setTitleText("Zeit")

        # Definiere den Zeitbereich
        start_datetime = QDateTime(2025, 1, 20, 8, 13, 0)
        end_datetime = QDateTime.fromString("2025-01-20_08:14:30", "yyyy-MM-dd_hh:mm:ss")
        axis_datetime.setRange(start_datetime, end_datetime)

        # Erstelle eine Y-Achse für die Temperaturwerte
        axis_temperature = QValueAxis()
        axis_temperature.setRange(50.0, 90.0)  # Temperaturbereich
        axis_temperature.setTitleText("Temperatur in Grad Celsius")

        # Serien dem Diagramm hinzufügen
        chart.addSeries(self.__temperature_cpu)
        chart.addSeries(self.__temperature_gpu)

        # Achsen zum Diagramm hinzufügen
        chart.addAxis(axis_datetime, Qt.AlignmentFlag.AlignBottom)  # X-Achse unten
        chart.addAxis(axis_temperature, Qt.AlignmentFlag.AlignLeft)  # Y-Achse links

        # Serien an Achsen binden
        self.__temperature_cpu.attachAxis(axis_datetime)
        self.__temperature_gpu.attachAxis(axis_datetime)

        self.__temperature_cpu.attachAxis(axis_temperature)
        self.__temperature_gpu.attachAxis(axis_temperature)

        # Diagramm im ChartView setzen
        self.setChart(chart)

    # Slot zum Hinzufügen eines CPU-Werts
    @pyqtSlot(QDateTime, float)
    def append_to_cpu(self, datetime, temperature):
        self.__temperature_cpu.append(datetime.toMSecsSinceEpoch(), temperature)

    # Slot zum Hinzufügen eines GPU-Werts
    @pyqtSlot(QDateTime, float)
    def append_to_gpu(self, datetime, temperature):
        self.__temperature_gpu.append(datetime.toMSecsSinceEpoch(), temperature)
