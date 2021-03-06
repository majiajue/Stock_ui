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
        print(self.macd_m)
        if self.macd_m is not None:
            self.macd_m(self.para_m)
            self.macd_m.disconnect()

        if self.macd_w is not None:
            self.macd_w(self.para_w)
            self.macd_w.disconnect()

        if self.macd_d is not None:
            self.macd_d(self.para_d)
            self.macd_d.disconnect()


class Slt_Stock(QtWidgets.QMainWindow, sl.Ui_MainWindow):
    '''根据界面、逻辑分离原则 初始化界面部分'''

    def __init__(self, parent=None):
        super(Slt_Stock, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.init_mwd)
        self.pushButton_2.clicked.connect(self.init_d)
        self.pushButton_3.clicked.connect(self.init_wd)

        self.pushButton_4.clicked.connect(self.conditions)
        self.set_init_conditions()

    def init_mwd(self):
        '''全部股票代码选出月线金叉，在此基础上选周线金叉，在此基础上再选日线金叉'''
        self.statusbar.showMessage('金叉初始化(月周日)')
        macd_m = mb.MACD_INDEX('m')
        macd_m.signal.send.connect(self.macd_progress)

        macd_w = mb.MACD_INDEX('w')
        macd_w.signal.send.connect(self.macd_progress)

        macd_d = mb.MACD_INDEX('d')
        macd_d.signal.send.connect(self.macd_progress)
        self.thread = MACD_Calc()
        self.thread.set_macd_m(macd_m.save_golden, 'all')
        self.thread.set_macd_w(  macd_w.save_golden,
            'D:\\0_stock_macd\\_月K线金叉.csv')
        self.thread.set_macd_d(  macd_d.save_golden,
            'D:\\0_stock_macd\\_周K线金叉.csv')
        self.thread.start()

    def init_wd(self):
        '''全部股票代码选出周线金叉，在此基础上再选日线金叉'''
        self.statusbar.showMessage('金叉初始化(周日)')
        macd_w = mb.MACD_INDEX('w')
        macd_w.signal.send.connect(self.macd_progress)
        macd_d = mb.MACD_INDEX('d')
        macd_d.signal.send.connect(self.macd_progress)

        self.thread = MACD_Calc()
        self.thread.set_macd_w(
            macd_w.save_golden, 'all')

        self.thread.set_macd_d( macd_d.save_golden,
            'D:\\0_stock_macd\\_周K线金叉.csv')
        self.thread.start()

    def init_d(self):
        '''全部股票代码选出日线金叉'''
        self.statusbar.showMessage('金叉初始化(日)')
        macd_d = mb.MACD_INDEX('d')
        macd_d.signal.send.connect(self.macd_progress)

        self.thread = MACD_Calc()
        self.thread.set_macd_d(macd_d.save_golden, 'all')
        self.thread.start()

    def set_init_conditions(self):
        self.radioButton_2.setChecked(True)
        self.radioButton_6.setChecked(True)
        self.radioButton_9.setChecked(True)

    def conditions(self):
        self.statusbar.showMessage('正在计算...')
        self.textEdit.clear()

        if self.radioButton.isChecked():
            # print('radioButton 月线')
            path = 'D:\\0_stock_macd\\_月K线金叉.csv'

        if self.radioButton_2.isChecked():
            # print('radioButton_2 周线')
            path = 'D:\\0_stock_macd\\_周K线金叉.csv'

        if self.radioButton_3.isChecked():
            # print('radioButton_3 日线')
            path = 'D:\\0_stock_macd\\_日K线金叉.csv'

        if self.radioButton_6.isChecked():
            # print('radioButton_6 60 分钟级别')
            macd_jb = mb.MACD_INDEX('60')
            macd_jb.signal.send.connect(self.macd_progress)
        if self.radioButton_7.isChecked():
            # print('radioButton_7 15 分钟级别')
            macd_jb = mb.MACD_INDEX('15')
            macd_jb.signal.send.connect(self.macd_progress)

        if self.radioButton_8.isChecked():
            # print('radioButton_8 已金叉')
            macd_jb.save_golden(path)

        if self.radioButton_9.isChecked():
            # print('radioButton_9 即将金叉 ')
            macd_jb.save_bing_golden(path)

        if self.radioButton_10.isChecked():
            # print('radioButton_10 底背离')
            macd_jb.save_bottom(path)

        if self.radioButton_11.isChecked():
            print('radioButton_11 刚刚金叉')
            macd_jb.save_golden_now(path)

        macd_jb.disconnect()

        self.label.setText('  ')
        stock_code = stb.get_stock_code('D:\\0_stock_macd\\_日K线金叉.csv')
        cnt = stock_code.shape[0]
        self.statusbar.showMessage('计算完成, 共选出 ' + str(cnt) + ' 只')
        print('xxx'*9)
        all_stock = stb.get_market_code('all')
        print('yyy' * 9)
        print( all_stock.shape[0] )
        for x in range(cnt):
            code = stock_code.iloc[x]['stock_code']
            print('zzz' * 9)
            for i in range(1, all_stock.shape[0]):
                if all_stock.iloc[i]['stock_code'].find(code[3:]) > 0:
                    rst = '{: <4d}'.format(x + 1) + code
                    rst = rst + '\t' + all_stock.iloc[i]['stock_name']
                    self.textEdit.append(rst)

    def macd_progress(self, curr):
        self.label.setText(curr)
        QtWidgets.QApplication.processEvents()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MP = Slt_Stock()
    MP.show()
    sys.exit(app.exec_())
