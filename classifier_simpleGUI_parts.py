from PyQt4 import QtGui
from PyQt4 import QtCore
import cv2
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class dragarea(QtGui.QWidget):
    def __init__(self):
        super(dragarea, self).__init__()
        # self.resize(100, 100)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()


class detail_panel(QtGui.QWidget):
    def __init__(self, label_list):
        self.nclass = len(label_list)
        self.labels = label_list

        super(detail_panel, self).__init__()
        self.main_layout = QtGui.QVBoxLayout()
        self.top_layout = QtGui.QHBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addLayout(self.top_layout)

        self.image_view = QtGui.QGraphicsView()
        self.image_scene = QtGui.QGraphicsScene()
        self.image_view.setScene(self.image_scene)
        self.top_layout.addWidget(self.image_view)

        self.score_fig = plt.figure()
        self.score_fig.set_size_inches(7, 3)
        self.score_fig.set_dpi(80.0)
        self.score_graph = FigureCanvas(self.score_fig)
        self.main_layout.addWidget(self.score_graph)

        self.score_table = QtGui.QTableWidget()
        self.score_table.setRowCount(self.nclass)
        self.score_table.setColumnCount(3)
        horzHeaders = QtCore.QStringList()
        horzHeaders << "Class index" << "Class name" << "prob"
        self.score_table.setHorizontalHeaderLabels(horzHeaders)
        self.top_layout.addWidget(self.score_table)

        self.image_index = QtGui.QLabel()
        self.main_layout.addWidget(self.image_index)

    def set_information(self, image, score, index, filename):
        npbuf = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, c = image.shape
        bytesPerLine = w*c
        qimg = QtGui.QImage(npbuf, w, h, bytesPerLine,
                            QtGui.QImage.Format_RGB888)
        qitem = QtGui.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(qimg))
        self.image_scene.clear()
        self.image_scene.addItem(qitem)

        ax = self.score_fig.add_subplot(111)
        ax.hold(False)
        ax.set_xlabel("class index")
        ax.set_ylabel("probability")
        ax.plot(np.arange(1, self.nclass + 1), score, '*-')
        self.score_graph.draw()

        self.score_table.setSortingEnabled(False)
        for i, s_c in enumerate(zip(score, self.labels)):
            s, c = s_c
            self.score_table.setItem(i, 2, QtGui.QTableWidgetItem("{:8f}".format(s)))
            self.score_table.setItem(i, 0, QtGui.QTableWidgetItem("{:04d}".format(i + 1)))
            self.score_table.setItem(i, 1, QtGui.QTableWidgetItem(c))
        self.score_table.setSortingEnabled(True)

        self.image_index.setText("Image {}, file: {}".format(index + 1, filename))

        self.show()
        return self
