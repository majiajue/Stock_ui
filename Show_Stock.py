
import SelectStock as sl
import macd_base as mb
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import stock_base as stb


class MACD_Calc(QThread):
    macd_m = None
    para_m = ''
    macd_w = None
    para_w = ''
    macd_d = None
    para_d = ''
    def __init__(self):
        super().__init__()

    def set_macd_m(self, what_macd, what_para):
        self.macd_m = what_macd
        self.para_m = what_para

    def set_macd_w(self, what_macd, what_para):
        self.macd_w = what_macd
        self.para_w = what_para

    def set_macd_d(self, what_macd, what_para):
        self.macd_d = what_macd
        self.para_d = what_para
    def __del__(self):
        self.wait()

    def run(self):
        self.macd_m(self.para_m)
        self.macd_w(self.para_w)
        self.macd_d(self.para_d)


class Slt_Stock(QtWidgets.QMainWindow, sl.Ui_MainWindow):
    '''根据界面、逻辑分离原则 初始化界面部分'''

    def __init__(self, parent=None):
        super(Slt_Stock, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.init_mwd)

    def init_mwd(self):

        macd_m = mb.MACD_INDEX('m')
        macd_w = mb.MACD_INDEX('w')
        macd_d = mb.MACD_INDEX('d')
        macd_m.signal.send.connect(self.macd_progress)
        self.thread = MACD_Calc()
        self.thread.set_macd_m(macd_m.save_golden, 'all')
        self.thread.set_macd_w(macd_w.save_golden, 'D:\\0_stock_macd\\_月K线金叉.csv')
        self.thread.set_macd_d(macd_d.save_golden, 'D:\\0_stock_macd\\_周K线金叉.csv')
        self.thread.start()

    def macd_progress(self, curr ):
        self.statusbar.showMessage(curr)
        QtWidgets.QApplication.processEvents()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MP = Slt_Stock()
    MP.show()
    sys.exit(app.exec_())
