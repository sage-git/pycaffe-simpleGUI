Simple caffe Classifier
=======================

GUI tool to test caffe neural networks.

## Description

Provides a simple GUI tool to use CNN.
To classify images, you only need to drag and drop.

## Requirements

* Python 2.7
* PyQt4
* pycaffe (python interface of caffe)
* numpy
* matplotlib
* cv2 (python interface of OpenCV)

## Preparation

Prepare files to load CNN

* net.caffemodel - binary proto file for weights of CNN. Obtain by downloading or training.
* deploy.prototxt - define the network structure. Set input layer dim = 1x3x227x227, and set the top layer name as "prob".
* labels.txt - simple text file to list the classes to be classified.
* Create a folder with network name and put these 3 files into that folder.
<<<<<<< HEAD
* Edit `classifier_simpleGUI.py` line 152. Set the argument of `UI()` to the created folder name.
=======
>>>>>>> c930d11768d38137f6246d8786724f68933d2cff

Folder `alexnet` is an example.

`alexnet/deploy.prototxt` is a modified file of [BVLC alexnet (github)](https://github.com/BVLC/caffe/tree/master/models/bvlc_alexnet).
 Corresponding caffemodel file can be downloaded from there.

 `alexnet/labels.txt` is a list of classes. This is extracted from synset_words.txt, which is downloaded from http://dl.caffe.berkeleyvision.org/caffe_ilsvrc12.tar.gz.


## Usage

1. Run `classifier_simpleGUI.py`. Running on terminal is better because some messages will be flushed on stdout/err.
2. After load the caffe model, an empty window whose title is the same as the network name will launch. Please wait for a while.
3. Select image files you want to classify. Drag them to the window and drop.
4. After forward calculations, a table which lists top 5 classes for each image will appear. Please wait for a while.
5. The actual probability values for each class can be confirmed by pushing "Details" button on the bottom of the window.
6. During detail view, you can return to the top 5 list table.
7. Dragging and drop other images, the previous results will be discarded an then calculate for new images and prepare a new table.
8. To terminate the program, simply close the window.

## Note

This program is written to learn how to use PyQt4.

## Author

Seiji Ueno

[ブログ(日本語)](http://sage-t.tumblr.com/)
