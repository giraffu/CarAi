'''
Author: chuzeyu 3343447088@qq.com
Date: 2023-07-04 09:55:38
LastEditors: chuzeyu 3343447088@qq.com
LastEditTime: 2023-07-20 09:07:16
FilePath: \CesiumAi\DataHandle.py
Description: 主要功能是查看原始数据集，并将原始数据转为h5格式保存下来,在AiDrive环境下运行
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import Cooking

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# << 配置下载的数据集目录 >>
RAW_DATA_DIR = './data/data_raw/'

# << 配置预处理后(*.h5)的输出目录 >>
COOKED_DATA_DIR = './data/data_handle/'

DATA_FOLDERS = ['normal_1', 'normal_2', 'normal_3', 'normal_4', 'normal_5', 'normal_6', 'swerve_1', 'swerve_2', 'swerve_3']

train_eval_test_split = [0.7, 0.2, 0.1]
full_path_raw_folders = [os.path.join(RAW_DATA_DIR, f) for f in DATA_FOLDERS]
Cooking.cook(full_path_raw_folders, COOKED_DATA_DIR, train_eval_test_split)