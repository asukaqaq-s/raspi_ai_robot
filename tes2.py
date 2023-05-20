from PyQt5.QtCore import QThread, pyqtSignal, QDateTime, QObject
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QLabel
import time
import sys
import modules.ui as ui
import threading


def func():
    while True:
        print(1)


class UI(threading.Thread):
    
    def run(self):
        app = QApplication(sys.argv)
        win = ui.Window()
        win.show()

        #func()
        app.exec_()

if __name__ == '__main__':
    
    u = UI()
    u.start()
    while True:
        print("111")
        time.sleep(1)
    sys.exit()

