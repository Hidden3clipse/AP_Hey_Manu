from PyQt6.QtCore import pyqtSlot, QDateTime, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser

from ChartView import ChartView


class CentralWidget(QWidget):
    send_cpu_temperature = pyqtSignal(QDateTime, float)
    send_gpu_temperature = pyqtSignal(QDateTime, float)

    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        chart_view = ChartView(parent)
        self.send_cpu_temperature.connect(chart_view.append_to_cpu)
        self.send_gpu_temperature.connect(chart_view.append_to_gpu)

        self.__text_browser = QTextBrowser()

        layout = QVBoxLayout()

        layout.addWidget(chart_view)
        layout.addWidget(self.__text_browser)

        self.setLayout(layout)

    @pyqtSlot(str)
    def add_line(self, line):
        tokens = line.split(" ")

        datetime = QDateTime.fromString(tokens[0], "yyyy-MM-dd_hh:mm:ss")
        temperature = float(tokens[2])

        if temperature > 88.0:
            cursor = self.__text_browser.textCursor()

            format = cursor.charFormat()
            format.setFontWeight(QFont.Weight.Bold)

            cursor.setCharFormat(format)

            self.__text_browser.setTextCursor(cursor)

        self.__text_browser.append(line)

        if tokens[1] == "CPU":
            self.send_cpu_temperature.emit(datetime, temperature)
        elif tokens[1] == "GPU":
            self.send_gpu_temperature.emit(datetime, temperature)
        #Optional - nicht gefordert
        else:
            print("Token", tokens[1], "unbekannt.")

        if temperature > 88.0:
            cursor = self.__text_browser.textCursor()

            format = cursor.charFormat()
            format.setFontWeight(QFont.Weight.Normal)

            cursor.setCharFormat(format)

            self.__text_browser.setTextCursor(cursor)
