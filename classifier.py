import caffe
import cv2
import numpy as np


class Classifier(object):
    def __init__(this, net="deploy.prototxt", weight="net.caffemodel",
                 class_label="labels.txt",
                 image_size=(227, 227), crop_size=(227, 227)):
        this.net = caffe.Classifier(net, weight,
                                    input_scale=1.0, image_dims=image_size)
        this.labels = []
        with open(class_label, 'r') as f:
            for line in f:
                this.labels.append(line)
        this.nclass = len(this.labels)
        this.img_size = image_size
        this.crop_size = crop_size

    def __call__(this, img):
        if img.ndim < 2 or img.ndim > 3:
            print "Input image should be a GrayScale or 3-bit image"
            raise ValueError
        c = 3
        resized = np.asarray(cv2.resize(img, this.img_size),
                             dtype=np.float32)
        if img.ndim == 2:
            c = 1
        if c == 1:
            input_vec = [cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)]
        else:
            input_vec = [resized]
        this.net.predict(input_vec, oversample=False)
        return np.copy(this.net.blobs['prob'].data[0])

    def get_class_top(this, i, score):
        if i < 0 or i >= this.nclass:
            return None
        order = np.argsort(score)[-1::-1]
        return [(ki + 1, this.labels[k], score[k])
                for ki, k in enumerate(order[:i])]

    def get_label_list(this):
        return this.labels
