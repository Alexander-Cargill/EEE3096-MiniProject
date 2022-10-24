from PyQt5 import QtWidgets, QtSerialPort, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import serial

serialPort = serial.Serial(port = "COM3", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ""                           # Used to hold data coming over UART

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Steezy UART gang")

        self.label = QtWidgets.QLabel(self)
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("Welcome to the coolest UART interface this side of the Zambezi!")
        self.label1.adjustSize()
        self.label1.move(50,50)
        self.label.move(50,80)
        self.label.setText("")

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.move(20,0)
        self.b1.setText("Receive Transmission!")
        self.b1.adjustSize()
        self.b1.clicked.connect(self.serialVibes)
        
        self.b2 = QtWidgets.QPushButton(self)
        self.b2.move(160,0)
        self.b2.setText("Clear Text")
        self.b2.adjustSize()
        self.b2.clicked.connect(self.clear)
        
        self.output_text = QtWidgets.QTextEdit(readOnly=True)
        

    def update(self):
        self.label.adjustSize()
        self.label1.adjustSize()

    def serialVibes(self):
        self.label1.setText("Please wait...")
        self.update()
        temp = ""
        for i in range(14):
            serialString = serialPort.readline()
            temp = temp + serialString.decode('Ascii')
            #self.label.setText(serialString.decode('Ascii'))
            #print(serialString.decode('Ascii'))
        self.label.setText(temp)
        self.update()

    def clear(self):
        self.label.setText("")
        self.label1.setText("Welcome to the coolest UART interface this side of the Zambezi!")
        self.update()
    
    



def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())



window()
