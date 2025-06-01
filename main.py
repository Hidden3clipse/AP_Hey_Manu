# Das ist der Einstiegspunkt in die PyQt6-Anwendung

# 1. sys wird benötigt, um das Verhalten beim Programmende zu steuern (z. B. sys.exit)
import sys

# 2. QApplication ist die Hauptklasse für jede Qt-App – sie verwaltet das Event-System
from PyQt6.QtWidgets import QApplication

# 3. Import des Hauptfensters deiner Anwendung (selbst geschriebene Klasse)
from MainWindow import MainWindow

# 4. Standard-Python-Konstrukt: Nur ausführen, wenn diese Datei direkt gestartet wird
if __name__ == '__main__':
    # Erstelle eine QApplication-Instanz – notwendig für alle GUI-Anwendungen
    app = QApplication(sys.argv)

    # Erzeuge eine Instanz deines MainWindow (das ist dein selbst erstelltes Fenster)
    main_window = MainWindow()

    # Zeige das Fenster auf dem Bildschirm
    main_window.show()

    # Starte die Event-Schleife (Wartet z. B. auf Klicks, Tasteneingaben etc.)
    sys.exit(app.exec())
