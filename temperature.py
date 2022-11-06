# 总控制程序。
# 当实际温度值在下限和上限值之间时，LED灯显绿色，蜂鸣器无响声；
# 当实际温度值超下限时，LED灯显蓝色，蜂鸣器蜂鸣3次，每次0.5秒；
# 当实际温度值超上限时，LED灯显红色，蜂鸣器蜂鸣3次，每次0.1秒。

# !/usr/bin/env python
import RPi.GPIO as GPIO
import importlib  # 动态加载某个模块
import time
import sys

# 重新定义部分针脚位置
LedR = 11  # 17
LedG = 12  # 18
LedB = 13  # 27
Buzz = 15  # 22

# ds18b20 = '28-031467805fff'
# location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'

# 导入模块
joystick = importlib.import_module('03_joystick_PS2')
ds18b20 = importlib.import_module('04_ds18b20')
beep = importlib.import_module('02_active_buzzer')
rgb = importlib.import_module('01_rgb_led')

# 调用各个模块中的初始化函数
joystick.setup()
ds18b20.setup()
beep.setup(Buzz)
rgb.setup(LedR, LedG, LedB)

color = {'Red': 0xFF0000, 'Green': 0x00FF00, 'Blue': 0x0000FF}


def setup():
    # """初始化下限和上限值"""
    global lowl, highl
    lowl = 9
    highl = 15


def edge():
    # """根据摇杆方向的值设置上下限的值及退出"""
    global lowl, highl
    temp = joystick.direction()
    if temp == 'Button pressed':  # 当按下摇杆时，程序退出
        destroy()
        quit()
    if temp == 'up' and highl <= 125:  # 上限值不超过125
        highl += 1
    if temp == 'down' and lowl < highl - 1:  # 保证上限值不能<=下限值
        highl -= 1
    if temp == 'right' and lowl < highl - 1:  # 保证上限值不能<=下限值
        lowl += 1
    if temp == 'left' and lowl >= -5:  # 下限值不低于-5
        lowl -= 1


def loop():
    while True:
        edge()
        temp = ds18b20.read()
        print('The lower limit of temperature : ', lowl)
        print('The upper limit of temperature : ', highl)
        print('Current temperature : ', temp)
        print('')
        if float(temp) < float(lowl):
            rgb.setColor(color['Blue'])  # 温度超下限时LED灯显蓝色
            for i in range(0, 3):
                beep.beep(0.5)  # 蜂鸣3次，每次0.5秒
        if temp >= float(lowl) and temp < float(highl):
            rgb.setColor(color['Green'])  # 温度不超限时LED灯显绿色
        if temp >= float(highl):
            rgb.setColor(color['Red'])  # 温度超上限时LED灯显红色
            for i in range(0, 3):
                beep.beep(0.1)  # 蜂鸣3次，每次0.1秒


def destroy():
    beep.destroy()
    joystick.destroy()
    ds18b20.destroy()
    rgb.destroy()
    GPIO.cleanup()


if __name__ == "__main__":
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
