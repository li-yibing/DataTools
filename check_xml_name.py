#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@File   : check_xml_name.py
@Author : yb_li
@Date   : 2023/8/10
@Desc   : 检查VOC数据集标签中是否出现非法的标签
"""

import os
from loguru import logger
import xml.etree.ElementTree as ET


def check_xml(dataset_path):
    """
    检查VOC数据集标签中是否出现非法的标签
    :param dataset_path:
    :return:
    """
    # 遍历文件夹中的文件
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            # 检查文件扩展名是否为.xml
            if file.endswith(".xml"):
                # 解析XML文件
                xml_file = os.path.join(root, file)
                tree = ET.parse(xml_file)
                tree_root = tree.getroot()

                # 获取标签名
                label = tree_root.find("object/name").text

                # 判断标签是否为"coal"或"stone"
                if label != "coal" and label != "stone":
                    # 输出不正确的标签对应的文件名
                    logger.info(f"在{file} 找到非法标签{label}")

                    os.remove(xml_file)
                    logger.info(f"删除{file}")


def check_txt(dataset_path, nc=2):
    """
     检查YOLO数据集标签中是否出现非法的标签
    :param dataset_path: 数据集路径
    :param nc: 类别数
    :return: 
    """  # 遍历文件夹中的文件
    remove_flag = False
    for root, dirs, files in os.walk(dataset_path):
        for file in files:  # 检查文件扩展名是否为.txt
            if file.endswith(".txt"): # 读取txt文件
                txt_file = os.path.join(root, file)
                with open(txt_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        label = int(line.strip().split()[0])
                        if label > (nc - 1):
                            # 输出标签值大于1的文件名
                            logger.info(f"本数据集有{nc}个类别，在{file}中找到标签值大于{nc - 1}的行")
                            remove_flag = True

                # 删除txt文件
                if remove_flag:
                    os.remove(txt_file)
                    logger.info(f"删除{file}")
                    remove_flag = False

if __name__ == "__main__":
    # check_xml("C:/Users/ybli/Desktop/data-4/datasets/labels/test")
    check_txt("C:/Users/ybli/Desktop/data-4/datasets/labels/val")

