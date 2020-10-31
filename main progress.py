
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import psutil
import GPUtil


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setWindowTitle("Hardware Info")
        self.thread = Worker()
        self.buttonStart = QPushButton("start monitoring")
        self.progresscpu = QProgressBar(self)
        self.progressgpu = QProgressBar(self)
        self.progressram = QProgressBar(self)
        self.cputemp = QProgressBar(self)
        self.progresscpu.setGeometry(0, 0, 300, 25)
        self.progresscpu.setMaximum(100)
        self.progresscpu.setValue(100)
        self.progressgpu.setGeometry(0, 0, 300, 25)
        self.progressgpu.setMaximum(100)
        self.progressgpu.setValue(100)
        self.progressram.setGeometry(0, 0, 300, 25)
        self.progressram.setMaximum(100)
        self.progressram.setValue(100)
        self.cputemp.setGeometry(0, 0, 300, 25)
        self.cputemp.setMaximum(100)
        self.cputemp.setValue(100)
        self.l1 = QLabel()
        self.l2 = QLabel()
        self.l3 = QLabel()
        self.l4 = QLabel()
        self.l1.setText("CPU LOAD")
        self.l2.setText("GPU LOAD")
        self.l3.setText("RAM LOAD")
        self.l4.setText("CPU TEMPERATURE")
        layout = QGridLayout(self)
        layout.addWidget(self.l1, 0, 0)
        layout.addWidget(self.l4, 0, 1)
        layout.addWidget(self.progresscpu, 1, 0)
        layout.addWidget(self.l2, 2, 0)
        layout.addWidget(self.progressgpu, 3, 0)
        layout.addWidget(self.l3, 4, 0)
        layout.addWidget(self.progressram, 5, 0)
        layout.addWidget(self.buttonStart, 6, 0)
        layout.addWidget(self.cputemp, 1, 1)

        self.buttonStart.clicked.connect(self.CPUStart)
        self.thread.cpuout.connect(self.CPUBar)
        self.thread.gpuout.connect(self.GpuBar)
        self.thread.ramout.connect(self.RAMBar)
        self.thread.cputempout.connect(self.CPUTemp)

    def CPUStart(self):
        self.buttonStart.setEnabled(False)
        self.thread.start()

    def CPUBar(self, value):
        self.progresscpu.setValue(value)

    def GpuBar(self, value):
        self.progressgpu.setValue(value)

    def RAMBar(self, value):
        self.progressram.setValue(value)

    def CPUTemp(self, value):
        self.cputemp.setValue(value)


class Worker(QThread):
    cpuout = pyqtSignal(int)
    gpuout = pyqtSignal(int)
    ramout = pyqtSignal(int)
    cputempout = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.working = True
        self.num = 0
        self.v = 0

    def __del__(self):
        self.working = False
        self.wait()

    def run(self):
        while self.working:
            cputemp = psutil.sensors_temperatures()
            cputemp2 = cputemp['k10temp']
            cputemp3 = cputemp2[1]
            cputempouts = cputemp3[1]
            cputempouts = round(cputempouts)
            valuecpu = psutil.cpu_percent()
            valuecpu = round(valuecpu)
            gpu = GPUtil.getGPUs()
            gpuload = gpu[0].load
            gpuload = gpuload * 100
            gpuload = int(gpuload)
            outram = psutil.virtual_memory()
            ramusage = outram.percent
            ramusage = round(ramusage)
            self.cputempout.emit(cputempouts)
            self.cpuout.emit(valuecpu)
            self.gpuout.emit(gpuload)
            self.ramout.emit(ramusage)
            self.sleep(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWidget()
    demo.show()
    sys.exit(app.exec_())
