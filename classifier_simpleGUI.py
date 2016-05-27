import classifier
from PyQt4 import QtGui
from PyQt4 import QtCore
from classifier_simpleGUI_parts import dragarea, detail_panel
import sys
import cv2
import os.path


class UI(QtGui.QMainWindow):
    def __init__(self, classifier_folder):
        self.class_name = classifier_folder
        self.image_size = (227, 227)
        net_model = classifier_folder + "/net.caffemodel"
        net_proto = classifier_folder + "/deploy.prototxt"
        net_label = classifier_folder + "/labels.txt"
        self.classifier = classifier.Classifier(image_size=self.image_size,
                                                net=net_proto,
                                                weight=net_model,
                                                class_label=net_label)
        labels = self.classifier.get_label_list()

        super(UI, self).__init__()
        self.setGeometry(300, 300, 720, 720)
        self.setWindowTitle(self.class_name)
        self.w = dragarea()
        self.w.dropEvent = self.load_images_dd
        self.root_vbox = QtGui.QVBoxLayout()
        self.w.setLayout(self.root_vbox)
        self.setCentralWidget(self.w)

        self.detail_btn = QtGui.QPushButton("Details")
        self.detail_btn.clicked.connect(self.click_detail)

        self.detail_w = detail_panel(labels)
        self.detail_page = QtGui.QWidget()
        self.controller_hbox = QtGui.QHBoxLayout()
        self.detail_page.setLayout(self.controller_hbox)
        self.prev_image = QtGui.QPushButton(" < prev")
        self.prev_image.clicked.connect(self.prev_detail)
        self.next_image = QtGui.QPushButton(" next >")
        self.next_image.clicked.connect(self.next_detail)
        self.return_table = QtGui.QPushButton(" score table ")
        self.return_table.clicked.connect(self.display_table)
        self.controller_hbox.addWidget(self.prev_image)
        self.controller_hbox.addWidget(self.return_table)
        self.controller_hbox.addWidget(self.next_image)

        self.image_added = False
        self.image_acceptable = True
        self.detail_view = False
        self.detail_index = -1
        self.table = None
        self.images = []
        self.scores = []
        self.show()

    def clean_display(self):
        for i in reversed(range(self.root_vbox.count())):
            self.root_vbox.itemAt(i).widget().setParent(None)

    def display_table(self):
        if self.table is None:
            print "There is no table data to display"
            return
        self.clean_display()
        self.detail_view = False
        self.root_vbox.addWidget(self.table)
        self.root_vbox.addWidget(self.detail_btn)
        self.show()

    def create_table(self, filenames, labels):
        nimage = len(filenames)
        self.table = QtGui.QTableWidget()
        self.table.setRowCount(nimage)
        self.table.setColumnCount(6)

        horzHeaders = QtCore.QStringList()
        horzHeaders << "File" << "1" << "2" << "3" << "4" << "5"
        self.table.setHorizontalHeaderLabels(horzHeaders)

        for i, fn_lbl in enumerate(zip(filenames, labels)):
            fn, lbl = fn_lbl
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(fn))
            for j, k in enumerate(lbl):
                self.table.setItem(i, j + 1, QtGui.QTableWidgetItem(k[1]))
                p = k[2]
                b = 255 - int((1.0 - p)*155)
                self.table.item(i, j + 1).setBackground(QtGui.QColor(b, b, b))

    def load_images_dd(self, event):
        if not self.image_acceptable:
            return
        self.image_acceptable = False
        urls = event.mimeData().urls()
        self.images = []
        self.scores = []
        self.filenames = []
        top5_labels = []
        self.image_added = False
        for url in urls:
            fn_qstring = url.toString().toLocal8Bit()
            imgfn = str(fn_qstring)[8:]  # remove file:///
            self.filenames.append(os.path.basename(imgfn))
            img = cv2.resize(cv2.imread(imgfn, 1),
                             self.image_size)
            s = self.classifier(img)
            self.images.append(img)
            self.scores.append(s)
            top5_labels.append(self.classifier.get_class_top(5, s))

        if len(self.filenames) > 0:
            self.create_table(self.filenames, top5_labels)
            self.display_table()
        self.image_acceptable = True
        self.image_added = True

    def click_detail(self):
        qsel = self.table.selectedIndexes()
        selected = 0
        if len(qsel) > 0:
            selected = qsel[0].row()
        self.display_detail(selected)

    def display_detail(self, n):
        if n < 0 or n > len(self.images):
            print "Invalid index"
            return
        self.detail_index = n
        self.clean_display()
        self.detail_w.set_information(self.images[n], self.scores[n],
                                      self.detail_index, self.filenames[n])
        self.root_vbox.addWidget(self.detail_w)
        self.root_vbox.addWidget(self.detail_page)
        self.show()

    def next_detail(self):
        n = self.detail_index + 1
        if n == len(self.images):
            n = 0
        self.display_detail(n)

    def prev_detail(self):
        n = self.detail_index - 1
        if n < 0:
            n = len(self.images) - 1
        self.display_detail(n)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    test = UI("alexnet")
    app.exec_()
