# -*- coding: utf-8 -*-
import pyltp 
import os
LTP_DATA_DIR = './ltp-models/ltp_data_v3.4.0'  # ltp模型目录的路径
# 这里注意，模型的路径里是'/'不是'\'

def cut_words(words):
    # words是输入的问句
    segmentor = pyltp.Segmentor()
    seg_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
    segmentor.load(seg_model_path)
    words = segmentor.segment(words)
    array_str="|".join(words)
    array=array_str.split("|")
    segmentor.release()
    return array


def words_mark(array):
    # array是分完词后用于储存的数组
    # 词性标注模型路径，模型名称为`pos.model`
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    postagger = pyltp.Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    postags = postagger.postag(array)  # 词性标注
    pos_str=' '.join(postags)
    pos_array=pos_str.split(" ")
    postagger.release()  # 释放模型
    return pos_array

def get_target_array(words):
    # word是输入的问句
    target_pos=['nh','n','nz']
    target_array=[]
    # cut_words是分词函数
    seg_array=cut_words(words)
    print(seg_array)
    # words_mark用于给词语打上词性标签
    pos_array = words_mark(seg_array)
    print(pos_array)
    exception=['分类','包含']
    for i in range(len(pos_array)):
        if pos_array[i] in target_pos or seg_array[i] in exception:
            target_array.append(seg_array[i])
    target_array.append(seg_array[0])
    print(target_array)
    # target_array.append(seg_array[1])
    return target_array





