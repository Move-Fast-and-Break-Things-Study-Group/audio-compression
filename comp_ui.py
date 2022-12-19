from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton
from pydub import AudioSegment
import soundfile as sf
import numpy as np


class Ui_MainWindow(QPushButton):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 251)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 80, 101, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 20, 141, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 55, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 150, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.evt_btn1_clicked)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(160, 50, 121, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(70, 120, 171, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 80, 121, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.evt_btn_clicked)
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(160, 20, 121, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 180, 201, 41))
        self.label_4.setScaledContents(False)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ComSound"))
        self.label.setText(_translate("MainWindow", "Путь к файлу:"))
        self.label_2.setText(_translate("MainWindow", "Частота дискретизации"))
        self.label_3.setText(_translate("MainWindow", "Битрейт"))
        self.pushButton.setText(_translate("MainWindow", "Сжать файл"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Default"))
        self.comboBox.setItemText(1, _translate("MainWindow", "6600"))
        self.comboBox.setItemText(2, _translate("MainWindow", "14250"))
        self.comboBox.setItemText(3, _translate("MainWindow", "23850"))
        self.pushButton_2.setText(_translate("MainWindow", "Выбрать файл"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Default"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "30000"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "35000"))
        self.comboBox_2.setItemText(3, _translate("MainWindow", "40000"))
        self.comboBox_2.setItemText(4, _translate("MainWindow", "50000"))
        self.comboBox_2.setItemText(5, _translate("MainWindow", "55000"))
        self.label_4.setText(_translate("MainWindow", ""))
        
    def evt_btn_clicked(self):
        global SFile
        SFile =  QFileDialog.getOpenFileName(self, 'Open file', '../Roha990/', "")
    def evt_btn1_clicked(self):
        self.progressBar.setValue(0)
        self.label_4.setText("")
        try:
            
            data, samplerate = sf.read(SFile[0])
            n = len(data)
            needChangeBitrate= True
            self.progressBar.setValue(10)
            if self.comboBox_2.currentText()=="Default":
                Fs=samplerate
            if self.comboBox_2.currentText()=="30000":
                Fs=30000
            if self.comboBox_2.currentText()=="35000":
                Fs=35000
            if self.comboBox_2.currentText()=="40000":
                Fs=40000
            if self.comboBox_2.currentText()=="50000":
                Fs=50000
            if self.comboBox_2.currentText()=="55000":
                Fs=55000
            if self.comboBox.currentText()=="Default":
                needChangeBitrate= False
            if self.comboBox.currentText()=="6600":
                BitRate=6600
            if self.comboBox.currentText()=="14250":
                BitRate=14250
            if self.comboBox.currentText()=="23850":
                BitRate=23850
            print("Sample rate : {} Hz".format(Fs))
            self.progressBar.setValue(25)
            ch1 = np.array([data[i][0] for i in range(n)]) #channel 1
            ch2 = np.array([data[i][1] for i in range(n)]) #channel 2
            ch1_Fourier = np.fft.fft(ch1) 
            abs_ch1_Fourier = np.absolute(ch1_Fourier[:n//2])
            eps = 1e-5
            frequenciesToRemove = (1 - eps) * np.sum(abs_ch1_Fourier) < np.cumsum(abs_ch1_Fourier)
            f0 = (len(frequenciesToRemove) - np.sum(frequenciesToRemove) )* (Fs / 2) / (n / 2)
            print("f0 : {} Hz".format(int(f0)))
            self.progressBar.setValue(50)
            wavCompressedFile = "Output_Data\wav_audio_compressed.wav"
            mp3CompressedFile = "Output_Data\mp3_audio_compressed.mp3"
            D = int(Fs / f0)
            self.progressBar.setValue(75)
            print("Downsampling factor : {}".format(D))
            new_data = data[::D, :]
            sf.write(wavCompressedFile, new_data, int(Fs / D), 'PCM_16')
            self.progressBar.setValue(85)
            audioCompressed = AudioSegment.from_wav(wavCompressedFile)
            if needChangeBitrate:
                audioCompressed.export(mp3CompressedFile, format="mp3", bitrate="{}".format(BitRate))
            else:
                audioCompressed.export(mp3CompressedFile, format="mp3")
            print("vse ok")
            self.progressBar.setValue(100)
        except BaseException:

            self.label_4.setText("Ошибка: Выберите файл другого формата")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
