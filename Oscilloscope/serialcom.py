import serial
from serial.tools import list_ports
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel , QPushButton , QComboBox,QMainWindow,QDockWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

class Window(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        #textLabel = QLabel(self)
        #textLabel.setText("Hello World!")
        #textLabel.move(110,85)

        self.graph=QDockWidget("Dockable", self)
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setGeometry(50,50,320,200)
        self.graph.setWidget(self.graphWidget)
        self.graph.setFloating(True)
        #self.setCentralWidget(self.graphWidget)
        self.setGeometry(50,50,320,200)
        
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        # plot data: x, y values
        self.graphWidget.plot(hour, temperature)
        
        button1 = QPushButton(self)
        button1.setText("Refresh")
        button1.move(64,32)
        button1.clicked.connect(self.refresh)

        port_list=list_ports.comports()
        combo = QComboBox(self)
        for port in port_list:
            combo.addItem(str(port.device))
        combo.activated[str].connect(self.refresh)
        self.setGeometry(50,50,320,200)
        self.setWindowTitle("PyQt5 Example")
        self.show()
        sys.exit(app.exec_())

    def refresh(self,text):
        print("Refresh "+text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Window()
    widget.show()
    port_list=list_ports.comports()
    for port in port_list:
        print(port)
    print(str(port.description)+" "+str(port.device)+" "+str(port.hwid)+" "+str(port.interface)+" "+str(port.name))
    ser = serial.Serial(port_list[0].device, 9600)


