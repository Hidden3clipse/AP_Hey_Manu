from datetime import datetime

from PyQt6.QtCharts import QChartView, QChart, QDateTimeAxis, QValueAxis, QSplineSeries
from PyQt6.QtCore import Qt, QDateTime, pyqtSlot
from PyQt6.QtWidgets import QStatusBar


class ChartView(QChartView):
    def __init__(self, parent=None):
        super(ChartView, self).__init__(parent)

        chart = QChart()
        chart.setTitle("Temperaturverlauf")

        self.__temperature_cpu = QSplineSeries()
        self.__temperature_cpu.setName("CPU")

        self.__temperature_gpu = QSplineSeries()
        self.__temperature_gpu.setName("GPU")

        axis_datetime = QDateTimeAxis()
        axis_datetime.setFormat("hh:mm:ss")
        axis_datetime.setTitleText("Zeit")

        start_datetime = QDateTime(2025, 1, 20, 8, 13, 0)
        end_datetime = QDateTime.fromString("2025-01-20_08:14:30", "yyyy-MM-dd_hh:mm:ss")

        axis_datetime.setRange(start_datetime, end_datetime)

        axis_temperature = QValueAxis()
        axis_temperature.setRange(50.0, 90.0)
        axis_temperature.setTitleText("Temperatur in Grad Celsius")

        chart.addSeries(self.__temperature_cpu)
        chart.addSeries(self.__temperature_gpu)

        chart.addAxis(axis_datetime, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_temperature, Qt.AlignmentFlag.AlignLeft)

        self.__temperature_cpu.attachAxis(axis_datetime)
        self.__temperature_gpu.attachAxis(axis_datetime)

        self.__temperature_cpu.attachAxis(axis_temperature)
        self.__temperature_gpu.attachAxis(axis_temperature)

        self.setChart(chart)

    @pyqtSlot(QDateTime, float)
    def append_to_cpu(self, datetime, temperature):
        self.__temperature_cpu.append(datetime.toMSecsSinceEpoch(), temperature)

    @pyqtSlot(QDateTime, float)
    def append_to_gpu(self, datetime, temperature):
        self.__temperature_gpu.append(datetime.toMSecsSinceEpoch(), temperature)
