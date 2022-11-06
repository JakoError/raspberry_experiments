#!/usr/bin/env python   #告诉Linux本文件是一个Python程序
import RPi.GPIO as GPIO    #导入控制GPIO的模块，RPi.GPIO
import time     #导入时间模块，提供延时、时钟和其它时间函数
 
colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF] #颜色列表
R = 11        #定义物理针脚号
G = 12
B = 13
 
def setup(Rpin, Gpin, Bpin):
    global pins   #在函数内部声明被其修饰的变量是全局变量
    global p_R, p_G, p_B
    pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
    GPIO.setmode(GPIO.BOARD)      #设置引脚编号模式为板载模式，即树莓派上的物理位置编号
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)    # 设置针脚模式为输出（或者输入GPIO.IN）
        GPIO.output(pins[i], GPIO.LOW) # Set pins to low(0 V) to off led
 
    p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
    p_G = GPIO.PWM(pins['pin_G'], 1999)
    p_B = GPIO.PWM(pins['pin_B'], 5000)
 
    p_R.start(0)      # Initial duty Cycle = 0(leds off)
    p_G.start(0)
    p_B.start(0)
 
def map(x, in_min, in_max, out_min, out_max): #将颜色的刺激量转换为占空比对应的值。
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
def off():
    for i in pins:
        GPIO.output(pins[i], GPIO.LOW)    # Turn off all leds
 
def setColor(col):   # For example : col = 0x112233
    R_val = (col & 0xff0000) >> 16   #先“与”运算只保留自己颜色所在位的值有效
    G_val = (col & 0x00ff00) >> 8    #再“右移”运算将自己颜色所在位的值提取出来
    B_val = (col & 0x0000ff) >> 0
 
    R_val = map(R_val, 0, 255, 0, 100)  #将颜色的刺激量转换为占空比对应的值
    G_val = map(G_val, 0, 255, 0, 100)
    B_val = map(B_val, 0, 255, 0, 100)
 
    p_R.ChangeDutyCycle(R_val)     # 更改占空比，调整该颜色的亮度
    p_G.ChangeDutyCycle(G_val)
    p_B.ChangeDutyCycle(B_val)
 
def loop():
    while True:
        for col in colors:
            setColor(col)
            time.sleep(1)
 
def destroy():
    p_R.stop()      #Turn off PWM
    p_G.stop()
    p_B.stop()
    off()              # Turn off all leds
    GPIO.cleanup()     #重置GPIO状态
 
if __name__ == "__main__":
    try:                       #用try-except代码块来处理可能引发的异常
        setup(R, G, B)      #调用初始化设置LED灯的函数
        loop()                     #调用循环函数
    except KeyboardInterrupt:      #如果遇用户中断（control+C），则执行destroy()函数
        destroy()             #调用清除LED状态的函数