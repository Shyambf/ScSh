from PyQt5.QtWidgets import QApplication, QMessageBox, QApplication, QMainWindow
from PyQt5 import QtCore
import sys
import subprocess
from Ui import Ui_MainWindow


class Window_SCSH(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window_SCSH, self).__init__()
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.pushButton.clicked.connect(self.set_time)
        self.pushButton_2.clicked.connect(self.close_time)

    def check_pass(self):
        passwd = self.lineEdit.text()
        with subprocess.Popen(["sudo", "-S", "-v"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            out_1 = proc.communicate(bytes(f"{passwd}\n", "UTF-8"))
            if 'sudo: no password was provided' in str(out_1[1].decode('utf-8')):
                return False
            else: return True

    def close_time(self):
        passwd = self.lineEdit.text()
        with subprocess.Popen(["sudo", "-S", "shutdown", "-c"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            ans = proc.communicate(bytes(f"{passwd}\n", "UTF-8"))
            msg = QMessageBox(self)
            msg.setWindowTitle("OK")
            msg.setText('The system shutdown has been cancelled')
            x = msg.exec_()

    def set_time(self):
        passwd = self.lineEdit.text()
        time = self.timeEdit.time()
        minuts = time.hour() * 60 + time.minute()
        with subprocess.Popen(["sudo", "-S", "shutdown", "-h", str(minuts)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
            out_1 = proc.communicate(bytes(f"{passwd}\n", "UTF-8"))
            out = str('Shutdown ' + ''.join(str(out_1[1].decode('utf-8')).split('Shutdown')[1]).split(',')[0])
        QMessageBox.about(self, "OK", out)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window_SCSH()
    ex.show()
    sys.exit(app.exec())