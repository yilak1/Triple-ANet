# -*- coding:utf-8 -*-
import tensorflow as tf
import os
import random
import math
import numpy as np
import cv2

def get_tfdata_path(tfrecords_path, split_name):
    if not os.path.exists(tfrecords_path):
        os.mkdir(tfrecords_path)
    tfrecords_filename = tfrecords_path + split_name
    return tfrecords_filename

# Helper functions for defining tf types
def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _image_to_tfexample(image_data, height, width, depth, label):
    return tf.train.Example(features=tf.train.Features(feature={
        'image/encoded': _bytes_feature(image_data),
        # 'image/format': _bytes_feature(image_format),
        'image/height': _int64_feature(height),
        'image/width': _int64_feature(width),
        'image/depth': _int64_feature(depth),
        'image/class/label': _int64_feature(label)}))

# def to_tfrecords(txt_path, tf_path,train_ratio, split_name):#
#     with open(txt_path, 'r') as f:
#         txt_list = f.readlines()
#         #txt_list = txt_list[0:len(txt_list)]
#         random.shuffle(txt_list)
#         num =len(txt_list)
#         num_train = int(math.floor(train_ratio * num))
#         num_test = num - num_train
#         print('num_train and num_test is %d, %d'% (num_train, num_test))
#         write_tf_data(num_train, num_test, txt_list, tf_path, split_name)


# def write_tf_data(num_train, num_test, txt_list, tfrecords_path, split_name):
#     tfrecords_filename = get_tfdata_path(tfrecords_path, split_name)
#     with tf.python_io.TFRecordWriter(tfrecords_filename) as tfrecords_writer:
#         for i in range(0, num_train):
#             rpath = txt_list[i].split(' ')[0]
#             label = int(txt_list[i].split(' ')[1])-1
#
#             data = cv2.imread(rpath)
#
#             data = cv2.resize(data,(128,128))
#             data1 = np.zeros([128,128,3],dtype = np.uint8)
#
#             data1[:,:,0] = data[:,:,2]
#             data1[:,:,1] = data[:,:,1]
#             data1[:,:,2] = data[:,:,0]
#
#             rows, cols, depth = data1.shape
#             data_str = data1.tostring()
#             example = _image_to_tfexample(data_str, rows, cols, depth, label)
#             tfrecords_writer.write(example.SerializeToString())
#
#             print(split_name, txt_list[i])
#         print(i+1)


def read_txt(txt_path):
    with open(txt_path) as f:
        lines = f.readlines()
    txt_data = [line.strip() for line in lines]
    return txt_data


# 构造训练和测试数据集
def to_tfrecords(root_dir, txt_COVID, txt_NonCOVID, tfrecords_path, split_name):
    # txt_path = [txt_COVID, txt_NonCOVID]
    # classes = ['COVID', 'non-COVID'] #[1, 0]
    txt_list_COVID = read_txt(txt_COVID)
    txt_list_NonCOVID = read_txt(txt_NonCOVID)
    write_tf_data(root_dir, txt_list_COVID, txt_list_NonCOVID, tfrecords_path, split_name)


def write_tf_data(root_dir, txt_list_COVID, txt_list_NonCOVID, tfrecords_path, split_name):
    classes = ['COVID', 'non-COVID'] #[1, 0]
    tfrecords_filename = get_tfdata_path(tfrecords_path, split_name)
    with tf.python_io.TFRecordWriter(tfrecords_filename) as tfrecords_writer:
        for i in range(0, len(txt_list_COVID)):
            rpath = os.path.join(root_dir, classes[0], txt_list_COVID[i])
            label = 1
            data = cv2.imread(rpath)
            print(data.shape)
            data = cv2.resize(data, (128, 128))
            data1 = np.zeros([128, 128, 3], dtype=np.uint8)

            data1[:, :, 0] = data[:, :, 2]
            data1[:, :, 1] = data[:, :, 1]
            data1[:, :, 2] = data[:, :, 0]
            rows, cols, depth = data1.shape
            data_str = data1.tostring()
            example = _image_to_tfexample(data_str, rows, cols, depth, label)
            tfrecords_writer.write(example.SerializeToString())
            print(split_name, txt_list_COVID[i])
        print(i + 1)

        for i in range(0, len(txt_list_NonCOVID)):
            rpath = os.path.join(root_dir, classes[1], txt_list_NonCOVID[i])
            label = 0
            data = cv2.imread(rpath)
            data = cv2.resize(data, (128, 128))
            data1 = np.zeros([128, 128, 3], dtype=np.uint8)

            data1[:, :, 0] = data[:, :, 2]
            data1[:, :, 1] = data[:, :, 1]
            data1[:, :, 2] = data[:, :, 0]
            rows, cols, depth = data1.shape
            data_str = data1.tostring()
            example = _image_to_tfexample(data_str, rows, cols, depth, label)
            tfrecords_writer.write(example.SerializeToString())
            print(split_name, txt_list_COVID[i])
        print(i + 1)


root_dir = '/home/lds/code/machine-learning/lung/archive'
# txt_COVID = '/home/lds/code/machine-learning/lung/archive/data-split/COVID/train_covid.txt'
# txt_NonCOVID= '/home/lds/code/machine-learning/lung/archive/data-split/non-COVID/train_non_covid.txt'
# split_name = 'train'
txt_COVID = '/home/lds/code/machine-learning/lung/archive/data-split/COVID/test_covid.txt'
txt_NonCOVID= '/home/lds/code/machine-learning/lung/archive/data-split/non-COVID/test_non_covid.txt'
tfrecords_path = './tfrecord/'
split_name = 'test'
to_tfrecords(root_dir, txt_COVID, txt_NonCOVID, tfrecords_path, split_name)
# txt_path = './txt/train.txt'
# tf_path = './tfrecord/'
# split_name = 'train'
# train_ratio = 1
# to_tfrecords(txt_path, tf_path, train_ratio, split_name)
        
