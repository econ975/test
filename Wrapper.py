import sys
import numpy as np
import os.path
from GUI.uipy.GUI import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Hardware import AllHardware
from Threads.SweepThread import SweepThread


class mainGUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        fig = Figure()
        self.ui.mplMap = FigureCanvas(fig)
        self.ui.mplMap.setParent(self.ui.widget)
        self.ui.mplMap.setGeometry(QtCore.QRect(QtCore.QPoint(0, 0), self.ui.widget.size()))
        self.ui.mplMap.axes = fig.add_subplot(111)

        self.load_defaults()
        self.init_hardware()

        self.ui.pushButtonStart.clicked.connect(self.start)
        self.ui.pushButtonStop.clicked.connect(self.stop)
        self.ui.pushButtonSave.clicked.connect(self.save)

    def load_defaults(self, fName='defaults.txt'):
        if fName == 'defaults.txt':
            f = open(os.path.join(os.path.dirname(__file__), fName), 'r')
        else:
            f = open(fName, 'r')
        d = {}
        for line in f.readlines():
            if line[-1] == '\n':
                line = line[:-1]
            [key, value] = line.split('=')
            d[key] = value
        f.close()
        dic = {'StartFreq': self.ui.startFreqLineEdit,
               'StopFreq': self.ui.stopFreqLineEdit,
               'NumOfSteps': self.ui.stepsLineEdit,
               'DwellTime': self.ui.dwellTimeLineEdit,
               'NumOfAvgs': self.ui.numOfAvgsLineEdit,
               'Power': self.ui.powerLineEdit
               }
        for key, value in d.items():
            dic.get(key).setText(value)

    def save_defaults(self, fName='defaults.txt'):
        pairList = []
        pairList.append(('StartFreq', self.ui.startFreqLineEdit.text()))
        pairList.append(('StopFreq', self.ui.stopFreqLineEdit.text()))
        pairList.append(('NumOfSteps', self.ui.stepsLineEdit.text()))
        pairList.append(('DwellTime', self.ui.dwellTimeLineEdit.text()))
        pairList.append(('NumOfAvgs', self.ui.numOfAvgsLineEdit.text()))
        pairList.append(('Power', self.ui.powerLineEdit.text()))
        ofile = open(os.path.join(os.path.dirname(__file__), fName), 'w')
        for pair in pairList:
            ofile.write(pair[0] + "=" + pair[1] + "\n")
        ofile.close()

    def init_hardware(self):
        try:
            self.hardware = AllHardware()
            self.hardware.MW_source.init_port(port_num='COM3')
        except BaseException as e:
            print(e)
            return
        self.sThread = SweepThread(self.hardware)
        self.sThread.update.connect(self.update_plot)
        self.sThread.finished.connect(self.stopped)

    @QtCore.pyqtSlot()
    def start(self):
        self.ui.pushButtonStart.setEnabled(False)
        self.ui.pushButtonStop.setEnabled(True)
        self.parameters = {'StartFreq': eval(self.ui.startFreqLineEdit.text()),
                           'StopFreq': eval(self.ui.stopFreqLineEdit.text()),
                           'NumOfSteps': eval(self.ui.stepsLineEdit.text()),
                           'DwellTime': eval(self.ui.dwellTimeLineEdit.text()),
                           'NumOfAvgs': eval(self.ui.numOfAvgsLineEdit.text()),
                           'Power': eval(self.ui.powerLineEdit.text())
                           }
        self.sThread.parameters = self.parameters
        self.x_arr = np.linspace(self.parameters['StartFreq'], self.parameters['StopFreq'],
                                    self.parameters['NumOfSteps'], endpoint=False)
        self.data = []
        self.sThread.start()

    @QtCore.pyqtSlot()
    def stop(self):
        self.sThread.running = False

    @QtCore.pyqtSlot()
    def stopped(self):
        self.ui.pushButtonStart.setEnabled(True)
        self.ui.pushButtonStop.setEnabled(False)
        self.ui.pushButtonSave.setEnabled(True)
        if len(self.data) > 1:
            self.plot_data()

    @QtCore.pyqtSlot()
    def save(self):
        if len(self.data) == 0:
            return
        directory = QtWidgets.QFileDialog.getSaveFileName(self, 'Enter save file', "", "Text (*.txt)")
        directory = str(directory[0].replace('/', '\\'))
        if directory != '':
            f = open(directory, 'w')
            for each_avg in self.data:
                for index in range(len(self.x_arr)):
                    f.write(str(self.x_arr[index]) + '\t' + str(each_avg[index]) + '\n')
            f.close()
        else:
            sys.stderr.write('No file selected\n')

    @QtCore.pyqtSlot()
    def discard(self):
        pass

    @QtCore.pyqtSlot()
    def prev(self):
        pass

    @QtCore.pyqtSlot()
    def next(self):
        pass

    @QtCore.pyqtSlot(list)
    def update_plot(self, l):
        self.data.append(l)
        avg = np.mean(self.data, axis=0)
        try:
            del self.errorPlot
            self.ui.mplMap.figure.clear()
            self.ui.mplMap.axes = self.ui.mplMap.figure.add_subplot(111)
        except AttributeError:
            pass
        try:
            self.linePlot.set_ydata(avg)
        except AttributeError:
            self.linePlot, = self.ui.mplMap.axes.plot(self.x_arr, avg)
        finally:
            self.ui.mplMap.draw()

    def plot_data(self):
        del self.linePlot
        self.ui.mplMap.figure.clear()
        self.ui.mplMap.axes = self.ui.mplMap.figure.add_subplot(111)
        avg = np.mean(self.data, axis=0)
        std = np.std(self.data, axis=0, ddof=1)
        err = std / np.sqrt(len(self.data))
        self.errorPlot = self.ui.mplMap.axes.errorbar(self.x_arr, avg, yerr=err, fmt='.')
        self.ui.mplMap.draw()

    @QtCore.pyqtSlot(QtCore.QEvent)
    def closeEvent(self, event):
        quit_msg = "Save parameters as Defaults?"
        reply = QtWidgets.QMessageBox.question(self, 'Message', quit_msg,
                                               QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
        if reply == QtWidgets.QMessageBox.Save:
            self.save_defaults()
            event.accept()
        elif reply == QtWidgets.QMessageBox.Discard:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWindow = mainGUI()
    myWindow.show()
    sys.exit(app.exec_())