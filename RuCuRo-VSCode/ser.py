import serial
import time


    #创建端口对象
try:
    #传入参数
    arduino_ser = serial.Serial('COM5', 115200)
except Exception as e:
    print('（s001）端口连接失败,错误原因：01)',e)

#arduino_ser = serial.Serial('COM5', 115200)



def ser_init():
    try:
        if arduino_ser.isOpen == False:
            arduino_ser.open()                # 打开串口
    except Exception as e:
        print('（s002）端口打开失败,错误原因：02)',e)

def ser_close():
    try:
        if arduino_ser != None:
            arduino_ser.close()
    except Exception as e:
        print('（s003）端口异常,错误原因：03)',e)

def ser_send(string):
    try:
        arduino_ser.write(string)
    except Exception as e:
        print('（s004）端口上传异常,错误原因：04)',e)


def ser_recv():
    try:
        while True:
            # 获得接收缓冲区字符
            count = arduino_ser.inWaiting()
            # 读取内容并显示
            if count == 0:
                break
            recv = arduino_ser.read(count)
            print(recv)
            # 清空接收缓冲区
            arduino_ser.flushInput()
            # 必要的软件延时
            time.sleep(0.1)
            return recv   
    except Exception as e:
        print('（s005）端口传输失败,错误原因：05)',e)


#def main():
#    while True:
#        # 获得接收缓冲区字符
#        count = ser.inWaiting()
#        if count != 0:
#            # 读取内容并显示
#            recv = ser.read(count)
#            print(recv)
#        # 清空接收缓冲区
#        ser.flushInput()
#        # 必要的软件延时
#        time.sleep(0.1)
#
#if __name__ == '__main__':
#    try:
#    # 打开串口
#        ser = serial.Serial('/dev/ttyAMA0', 115200)
#        if ser.isOpen == False:
#            ser.open()                # 打开串口
#        ser.write(b"rRZzXfxFRRXX")
#        #ser.write(b"rzrzRRzRzFZZrZZxfxFXXrZRzRzrZFFzRZRRFFxfxFFXXZZRRZrzRR")
#        main()
#    except KeyboardInterrupt:
#        if ser != None:
#            ser.close()