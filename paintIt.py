import os, time, random
from PyQt5 import QtWidgets, QtGui, QtCore, Qt
from PyQt5.QtGui import QPixmap, QImage, QPainter, QGuiApplication
from PyQt5.QtCore import QObject, QPoint, QTimer, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QGraphicsPixmapItem, QGraphicsScene, QDesktopWidget


screen_x, screen_y = 640, 480

class Ui_MainWindow(QObject):
    def setupUi(self, MainWindow):
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.screen_y, self.screen_x = sizeObject.height(), sizeObject.width()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.screen_x, self.screen_y)
        #     MainWindow.setMaximumSize(QtCore.QSize(screen_x, screen_y))
        #     MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, self.screen_x, self.screen_y))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setHorizontalScrollBarPolicy(1);
        self.graphicsView.setVerticalScrollBarPolicy(1);
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 12))
        self.menubar.setObjectName("menubar")
        self.menuOpen = QtWidgets.QMenu(self.menubar)
        self.menuOpen.setObjectName("menuOpen")
        MainWindow.setMenuBar(self.menubar)
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.transition)

        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuOpen.addAction(self.actionOpen)
        self.menubar.addAction(self.menuOpen.menuAction())
        self.actionOpen.triggered.connect(theMaster.mastering)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Viewer"))
        self.menuOpen.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))


class Master():

    def __init__(self):
        #get screen size
        screen = QGuiApplication.primaryScreen()
        screenGeometry = screen.geometry()
        self.screen_y = screenGeometry.height()
        self.screen_x = screenGeometry.width()

    def mastering(self):
        image_list = self.getFileList()
        transitioner.pix = QPixmap(theMaster.screen_x, theMaster.screen_y)
        transitioner.painter.begin(transitioner.pix)
        for img in image_list:
            newImage = self.scaleImage(QImage(img))
            transitioner.initTransition(newImage)
            transitioner.transition()


    def getFileList(self):
        # fdialog = QFileDialog()
        # fdialog.setFileMode(QFileDialog.DirectoryOnly)
        # file_name = QFileDialog.getExistingDirectory(None, 'Choose Directory', "/Users/rich")
        file_name = "/Users/rich/smallFrame"
        image_list = [os.path.join(file_name, f) for f in os.listdir(file_name) if f.endswith('.jpg')]
        return image_list


    def scaleImage(self, im):
        if im.height() == self.screen_y and im.width() <= self.screen_x:
            return im
        else:
            scaledImage = im.scaledToHeight(self.screen_y, QtCore.Qt.FastTransformation)
            if scaledImage.width() > self.screen_x:                                               # width needs to be cropped
                increment = (scaledImage.width() - self.screen_x) / 2                             # crop 1/2 oversize from each side
                scaledImage = scaledImage.copy(increment, 0, int(scaledImage.width() - (2*increment)), int(self.screen_y))
                return scaledImage
            elif scaledImage.width() < self.screen_x:
                increment = (self.screen_x - scaledImage.width()) / 2
                blkbox = QImage("blackImage.jpg")
                myPainter = QPainter(blkbox)
                dest = QPoint(increment,0)
                myPainter.begin(blkbox)
                myPainter.drawImage(dest, scaledImage)
                myPainter.end()
                return  blkbox


class TransitionMaster():

    def __init__(self):
        self.pix = QPixmap()
        self.painter = QPainter(self.pix)
        self.tranTimer = QTimer()
      #  self.newImage = QImage()
     #   self.displayImage = QImage()
        self.scene = QGraphicsScene()
        self.numSlices = 9

    def initTransition(self, im):
        self.newImage = im
        self.slice = 0
        # self.transition_type = random.randint(0,6)
        self.transition_type = 4
   #     self.displayImage = QImage("DSC_0035.jpg")


    def transition(self):
        self.slice += 1
        self.theTransition()
        if self.slice > self.numSlices:
            self.displayImage = self.pix.toImage()
        else:
            item = QGraphicsPixmapItem(self.pix)
            self.scene.addItem(item)
            ui.graphicsView.setScene(self.scene)
            self.tranTimer.start(50)


    def theTransition(self):
        if self.transition_type == 1:                  #wipe right
            cropped = self.newImage.copy(0, 0, int((self.newImage.width() * self.slice) / self.numSlices),  self.h)
            dest_point = QPoint(0,0,)
            self.painter.drawImage(dest_point, cropped)
        elif self.transition_type == 2:                #wipe left
            self.chunk = int((self.w * self.slice) / self.numSlices)
            cropped = self.newImage.copy(self.newImage.width()-self.chunk, 0, self.newImage.width(),  self.newImage.height())
            dest_point = QPoint(self.newImage.width()-self.chunk,0)
            self.painter.drawImage(dest_point, cropped)
        elif self.transition_type == 3:               #wipe down
            self.chunk = int((self.newImage.height() * self.slice) / self.numSlices)
            cropped = self.newImage.copy(0, 0, self.newImage.width(), self.chunk)
            dest_point = QPoint(0,0)
            self.painter.drawImage(dest_point, cropped)
        elif self.transition_type == 4:                 #wipe up
            self.chunk = int((self.newImage.height() * self.slice) / self.numSlices)
            self.cropped = self.newImage.copy(0, self.newImage.height()-self.chunk, self.newImage.width(), self.newImage.height())
            dest_point = QPoint(0,self.newImage.height()-self.chunk)
            self.painter.drawImage(dest_point, self.cropped)
        #    self.painter.end()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    transitioner = TransitionMaster()
    transitioner.tranTimer.timeout.connect(transitioner.transition)
    theMaster = Master()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())