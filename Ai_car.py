'''
Author: chuzeyu 3343447088@qq.com
Date: 2023-07-04 09:47:11
LastEditors: chuzeyu 3343447088@qq.com
LastEditTime: 2023-07-18 08:57:16
FilePath: \CesiumAi\Ai_car.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import tensorflow as tf
import sys
import numpy as np
import airsim
import time
if ('../../PythonClient/' not in sys.path):
    sys.path.insert(0, '../../PythonClient/')
from AirSimClient import *

#设置模型路径
MODEL_PATH = './model/models/model_model.02-0.0230253.h5'

model = tf.keras.models.load_model(MODEL_PATH)

#建立与airsim的通信
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
print("开启API控制: %s" % client.isApiControlEnabled())
car_controls = airsim.CarControls()

#初始化车辆控制参数
car_controls.steering = 0
car_controls.throttle = 0
car_controls.brake = 0

#定义缓存区
image_buf = np.zeros((1, 59, 255, 3))
state_buf = np.zeros((1,4))

#从airsim获取摄像头图片
def get_image():
    image_response = client.simGetImages([ImageRequest(0, AirSimImageType.Scene, False, False)])[0]
    image1d = np.fromstring(image_response.image_data_uint8, dtype=np.uint8)
    image_rgba = image1d.reshape(image_response.height, image_response.width, 3)

    return image_rgba[76:135,0:255,0:3].astype(float)

start_time = time.time()
while  (time.time() - start_time) < 50:
    car_state = client.getCarState()
    
    if (car_state.speed < 4):
        car_controls.throttle = 1.0
    else:
        car_controls.throttle = 0.0
    
    image_buf[0] = get_image()
    state_buf[0] = np.array([car_controls.steering, car_controls.throttle, car_controls.brake, car_state.speed])
    model_output = model.predict([image_buf, state_buf])
    car_controls.steering = round(0.5 * float(model_output[0][0]), 2)
    
    print('发送信号：方向盘 = {0}, 油门 = {1}'.format(car_controls.steering, car_controls.throttle))
    
    client.setCarControls(car_controls)
    
client.reset()

client.enableApiControl(False)