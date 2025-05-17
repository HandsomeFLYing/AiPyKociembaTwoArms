import tkinter as tk
import threading
import serial
import serial.tools.list_ports
import cv2 as cv
from PIL import Image,ImageTk
import os
import shutil
import time
from tkinter import ttk
from tkinter import messagebox

import datetime
import cube
from cube import points_list
import solution
#import kmeans
#备份数据
import DataBackup
DataBackup.Backuo()


def list_com_ports():
    """列出电脑上所有可用的 COM 端口"""
    ports = serial.tools.list_ports.comports()
    com_ports = []
    for port, desc, hwid in sorted(ports):
        com_ports.append(port)
    return com_ports

arduino_ser = None

#串口开关（0关1开）//这里关闭将停止大部分功能
CAMARA = 1
#模型摄像头开关 //传递依然继续
CAMARA_1 = 1
if CAMARA:
    import ser


# 获取可用串口
available_ports = list_com_ports()

exposure = -5
delay_time = 5
camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_AUTO_EXPOSURE, 1)
camera.set(cv.CAP_PROP_EXPOSURE, exposure)


# 显示图像更新
def video_loop():
    ret, img = camera.read()  # 从摄像头读取照片
    img = cv.flip(img, 1)
    if ret:
        img = cv.resize(img, (480,360), interpolation=cv.INTER_CUBIC)

        # 画魔方轮廓线
        cv.line(img,points_list[0],points_list[1],(0,255,0),3),cv.line(img,points_list[1],points_list[2],(0,255,0),3)
        cv.line(img,points_list[2],points_list[3],(0,255,0),3),cv.line(img,points_list[3],points_list[4],(0,255,0),3)
        cv.line(img,points_list[4],points_list[5],(0,255,0),3),cv.line(img,points_list[5],points_list[0],(0,255,0),3)
        cv.line(img,points_list[1],points_list[4],(0,255,0),3)
        cv.line(img,(40,300),(440,300),(100,255,0),3)
        cv2image = cv.cvtColor(img, cv.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
        current_image = Image.fromarray(cv2image)#将图像转换成Image对象
        imgtk = ImageTk.PhotoImage(image=current_image)
        cube_panel.imgtk = imgtk
        cube_panel.config(image=imgtk)

        window.after(50, video_loop)

# 绘画六面颜色
def draw_cube_ja():
    color = ['green','red','orange','white','yellow','blue']
    color_ = ['g','r','o','w','y','b']
    # 创建画布
    canvas = tk.Canvas(window,width=480,height=360,bg="pink")
    for n in range(len(color)):
        col = row = 0
        if (color[n] == 'white'):
            col = 1
            row = 0
        elif (color[n] == 'orange'):
            col = 0
            row = 1
        elif (color[n] == 'green'):
            col = 1
            row = 1
        elif (color[n] == 'red'):
            col = 2
            row = 1
        elif (color[n] == 'blue'):
            col = 3
            row = 1
        elif (color[n] == 'yellow'):
            col = 1
            row = 2
    

        x=10+col*120;y=10+row*120
        if(os.path.exists('data/'+color_[n]+'.txt')):
            if(os.path.exists('data/'+color_[n]+'.txt')):
                f = open('data/'+color_[n]+'.txt',mode='r',encoding='utf-8')
            else:
                f = open('data/'+color_[n]+'.txt')
            color_list = []
            for line in f.readlines(): #依次读取每行
                color_list.append(line.strip()) #去掉每行头尾空白
            f.close()

            if (len(color_list)==9):
                for i in range(3):
                    for j in range(3):
                        #绘制矩形(x1,y1,x2,y2),填充颜色：blue，边框颜色：white
                        canvas.create_rectangle(x+35*i,y+35*j,x+35*(i+1),y+35*(j+1),fill=str(color_list[i+j*3]),outline='black')
        else:
            for i in range(3):
                for j in range(3):
                    #绘制矩形(x1,y1,x2,y2),填充颜色：blue，边框颜色：white
                    canvas.create_rectangle(x+35*i,y+35*j,x+35*(i+1),y+35*(j+1),fill='pink',outline='black')
    canvas.pack()#包装画布
    #魔方面位置
    canvas.place(relx=0.01, rely=0.5)
    print("（G ja0）已经生成扫描后的魔方状态？")


def draw_cube():
    color = ['green','red','orange','white','yellow','blue']
    color_ = ['g','r','o','w','y','b']
    
    # 创建画布
    canvas = tk.Canvas(window,width=480,height=360,bg="pink")
    for n in range(len(color)):
        col = row = 0
        if (color[n] == 'white'):
            col = 1
            row = 0
        elif (color[n] == 'orange'):
            col = 0
            row = 1
        elif (color[n] == 'green'):
            col = 1
            row = 1
        elif (color[n] == 'red'):
            col = 2
            row = 1
        elif (color[n] == 'blue'):
            col = 3
            row = 1
        elif (color[n] == 'yellow'):
            col = 1
            row = 2

        x=10+col*120;y=10+row*120
        if(os.path.exists('data/'+color[n]+'.txt')):
            if(os.path.exists('data/'+color_[n]+'.txt')):
                f = open('data/'+color_[n]+'.txt',mode='r',encoding='utf-8')
            else:
                f = open('data/'+color[n]+'.txt')
            color_list = []
            for line in f.readlines(): #依次读取每行
                color_list.append(line.strip()) #去掉每行头尾空白
            f.close()

            if (len(color_list)==9):
                for i in range(3):
                    for j in range(3):
                        #绘制矩形(x1,y1,x2,y2),填充颜色：blue，边框颜色：white
                        canvas.create_rectangle(x+35*i,y+35*j,x+35*(i+1),y+35*(j+1),fill=str(color_list[i+j*3]),outline='black')
        else:
            for i in range(3):
                for j in range(3):
                    #绘制矩形(x1,y1,x2,y2),填充颜色：blue，边框颜色：white
                    canvas.create_rectangle(x+35*i,y+35*j,x+35*(i+1),y+35*(j+1),fill='pink',outline='black')
    canvas.pack()#包装画布
    #魔方面位置
    canvas.place(relx=0.01, rely=0.5)
    print("六面图发生一次变化")


# 处理结果并输出
def check_data_su():
    for n in range(30):
        print('（1-推算？）')
        #time.sleep(0.1)
        if(n%2==0):
            gamut_type = 'hsv'
        else:
            gamut_type = 'lab'
        points,label,center,color_dict = cube.kmeans(gamut_type)
        if(cube.check_data() == 1):
            cube.cube_list_sort()
            code_str = solution.code2str()
            step_str,print_str = solution.str2step(code_str)
            send_string = step_str.encode('utf-8')
            if not(len(step_str) == 0):
                print(n)
                #cube.plot(points,label,center,color_dict)
                draw_cube()
                messagebox.showinfo("成功推算","已有结果(检查机器状态是否良好)")
                if CAMARA:
                    ser.ser_send(send_string[0:64])
                    print(send_string[0:64])
                    t1 = time.process_time()
                    while(time.process_time()<t1+2):pass
                    ser.ser_send(send_string[64:])
                    ser.ser_send(b'c')
                    
                result_lb = tk.Label(window,
                    text=print_str,justify='left',
                    width=88, height=10,
                    font=('Arial', 12),bg = 'White',)
                result_lb.place(relx = 0.35,rely = 0.1)
                print("发生结果？")
                break
            else:
                color = ['white','red','green','yellow','orange','blue']
                for i in range(6):
                    if os.path.exists('data/sort.txt'):
                        os.remove('data/sort.txt')
                    if os.path.exists('data/'+color[i]+'.txt'):
                        os.remove('data/'+color[i]+'.txt')
                print("异常的无结？")
    print("CC-处理结束")

def draw_result():
    print(time.process_time())
    if CAMARA:
        global camera
        if camera.isOpened():
            camera.release()
        global speed_spin
        print(speed_spin.get())

        speed_str = 'S'
        speed_str += str(speed_spin.get())
        speed_byte  =  speed_str.encode('utf-8')
        ser.ser_send(speed_byte)
        print(speed_byte)
        #上传
        ser.ser_send(b'l')
    
    save_picture()
    if not camera.isOpened():
        camera = cv.VideoCapture(0)
    check_data_su()


def speed_sc():
    if CAMARA:
        global speed_spin
        print(speed_spin.get())
        speed_str = 'S'
        speed_str += str(speed_spin.get())
        speed_byte  =  speed_str.encode('utf-8')
        ser.ser_send(speed_byte)
        ser.ser_send(b'l')
        print("（速度）:"+ str(speed_spin))

                
#开合机械爪
def zhua_result_on():#k
   if CAMARA:
        ser.ser_send(b'e')
        print("（zhua）尝试状态：on")

def zhua_result_off():#g
   if CAMARA:
        ser.ser_send(b'l')
        print("（zhua）尝试状态：off")
    

# 截图保存图片并处理成数据
def save_picture():
    print("（图像处理 ：）启动")
    if not CAMARA_1:
        print("（图像处理 ：）模拟1")
        img = cv.imread('test/20250516_192334/1.203125.png')
        cube.img2points(img,"1")
        print("（图像处理 ：）模拟2")
        img = cv.imread('test/20250516_192334/6.90625.png')
        cube.img2points(img,"2")
        print("（图像处理 ：）模拟3")
        img = cv.imread('test/20250516_192334/12.1875.png')
        cube.img2points(img,"3")

    if CAMARA_1:   
        for i in range(3):
            print("（图像处理 ：）Pi"+str(i)+"\t"+str(time.process_time()))
            camera = cv.VideoCapture(0)
            ret, img = camera.read()
            img = cv.flip(img, 1)
            img = cv.resize(img, (480,360), interpolation=cv.INTER_CUBIC)
            camera.release()
            # 增加曝光（亮度调整）
            #alpha = 2.0  # 对比度
            #beta = 0    # 亮度增加值
            #brightened_img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
            cube.img2points(img,str(i))
            cv.imwrite('./picture/'+str(time.process_time())+'.png',img)
            if(i!=2):
                ser.ser_send(b'XzC')
            else:
                ser.ser_send(b'XzC')
            if(i<2):
                t0 = time.process_time()
                while(time.process_time()<t0+delay_time):
                    pass
        if(False):
            camera.set(cv.CAP_PROP_AUTO_EXPOSURE, 1)
            camera.set(cv.CAP_PROP_EXPOSURE, exposure)
            camera.set(cv.CAP_PROP_EXPOSURE, exposure)
    #time.sleep(4)
        
def cube_cv_img():
    global camera
    if camera.isOpened():
        camera.release()
    global img_su
    print("（图像处理 ：）Pi"+str(img_su.get())+"\t"+str(time.process_time()))
    camera = cv.VideoCapture(0)
    ret, img = camera.read()
    img = cv.flip(img, 1)
    img = cv.resize(img, (480,360), interpolation=cv.INTER_CUBIC)
    camera.release()
    # 增加曝光（亮度调整）
            #alpha = 2.0  # 对比度
            #beta = 0    # 亮度增加值
            #brightened_img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
    cube.img2points(img,str(img_su.get()))
    cv.imwrite('./picture/'+str(time.process_time())+'.png',img)
    t0 = time.process_time()
    while(time.process_time()<t0+delay_time):
        pass
    if not camera.isOpened():
        camera = cv.VideoCapture(0)
    
        
#切换连接设备
def on_confirm():
    on_combobox,on_baudrate = port_combobox.get(),int(baudrate_combobox.get())
    try:
        #串口重连  
        ser.arduino_ser = serial.Serial(on_combobox,on_baudrate)
        print("（GUI 212）设备发生了一次变动？")
        ser.ser_init()
    except serial.SerialException as e:
        print(f"（GUI 212）尝试切换异常 ,错误原因on_confirm)  {e}")
def refresh_ports():
    available_ports = list_com_ports()
    port_combobox['values'] = available_ports
    if available_ports:
        port_combobox.set(available_ports[0])
    window.after(2000, refresh_ports)        
        
        
#重置程序
def reset():
    if CAMARA:
        ser.ser_send(b'c')
        global camera
        if not camera.isOpened():
            camera = cv.VideoCapture(0)
    DataBackup.Backuo()
    shutil.rmtree('./data')
    os.mkdir('./data')
    shutil.rmtree('./picture')
    os.mkdir('./picture')
    draw_cube()
    result_lb = tk.Label(window,
        text='',
        width=88, height=10,
        font=('Arial', 12),bg = 'white',)
    result_lb.place(relx = 0.35,rely = 0.1)

    result_lb = tk.Label(window,
    text='重置成功等待。。。',
    width=88, height=10,
    font=('Arial', 12),bg = 'White',)
    result_lb.place(relx = 0.35,rely = 0.1)
    print("（reset）重置成功")

if(True):
    if (os.path.exists('./data')):
        shutil.rmtree('./data')
    os.mkdir('./data')
    if (os.path.exists('./picture')):
        shutil.rmtree('./picture')
    os.mkdir('./picture')


#创建窗口对象
window = tk.Tk()
window.title("湖州职业技术学院")
window.geometry("1440x960")

#调用摄像头
if CAMARA:
    ser.ser_init()
    cube_panel = tk.Label(window)
    cube_panel.place(relx = 0.01,rely = 0.1)
    video_loop()

draw_cube()

x1_x = 0.42
#工作按钮
run_btn = tk.Button(window,
    text='全自动还原',      
    width=12, height=2,
    font=('Arial', 12),bg = 'Yellow',
    command=draw_result) 
run_btn.place(relx = x1_x,rely = 0.78)
#开关爪
zhua_no_btn = tk.Button(window,text='开爪',
                        width=12, height=2,font=('Arial', 12),bg = 'Yellow',
                        command=zhua_result_on) 
zhua_no_btn.place(relx = x1_x,rely = 0.72)    
zhua_off_btn = tk.Button(window,text='合爪',
                        width=12, height=2,font=('Arial', 12),bg = 'Yellow',
                        command=zhua_result_off)   
zhua_off_btn.place(relx = x1_x,rely = 0.66)    

x2_x =0.52
draw_cube_btn = tk.Button(window,
    text='绘图',      
    width=12, height=2,
    font=('Arial', 12),bg = 'Yellow',
    command=draw_cube) 
draw_cube_btn.place(relx = x2_x,rely = 0.72)

check_data_su_btn = tk.Button(window,
    text='处理现成数据',      
    width=12, height=2,
    font=('Arial', 12),bg = 'Yellow',
    command=check_data_su) 
check_data_su_btn.place(relx = x2_x,rely = 0.66)

picture_btn = tk.Button(window,
    text='重置程序',      
    width=12, height=2,
    font=('Arial', 12),bg = 'Yellow',
    command=reset) 
picture_btn.place(relx = x2_x,rely = 0.78)

x3_x =0.62
draw_cube_jb_btn = tk.Button(window,
    text='识别绘图',      
    width=12, height=2,
    font=('Arial', 12),bg = 'Yellow',
    command=draw_cube_ja) 
draw_cube_jb_btn.place(relx = x3_x,rely = 0.72) 

cube_cv_btn = tk.Button(window,
    text='手动拍摄处理',      
    width=12, height=2,
    font=('Arial', 12),bg = 'Yellow',
    command=cube_cv_img) 
cube_cv_btn.place(relx = x3_x,rely = 0.66) 

speed_btn = tk.Button(window,
    text='上传速度',      
    width=12, height=2,
    font=('Arial', 12),bg = 'Yellow',
    command=speed_sc) 
speed_btn.place(relx = x3_x,rely = 0.78) 

#状态显示框
result_lb = tk.Label(window,
    text='等待就绪。。。',
    width=88, height=10,justify='left',
    font=('Arial', 12),bg = 'White',)
result_lb.place(relx = 0.35,rely = 0.1)
#调整拦
speed_lb = tk.Label(window,
    text='速度：',
    width=6,
    font=('Arial', 14))
speed_lb.place(relx = 0.42,rely = 0.6)
var = tk.IntVar()
var.set(24)
speed_spin = tk.Spinbox(window,
    from_=0, to=99,
    width=4, increment=2,
    font=('Arial', 16),
    textvariable=var)
speed_spin.place(relx = 0.46,rely = 0.6)

var1 = tk.IntVar()
var1.set(1)
img_su = tk.Spinbox(window,
    from_=0, to=99,
    width=4, increment=2,
    font=('Arial', 16),
    textvariable=var1)
img_su.place(relx = x3_x,rely = 0.6)



#串口修改器窗口
serial_port_x = 0.8
    # 串口选择下拉框
port_label = tk.Label(window, text="选择串口:")
port_label.place(relx = serial_port_x,rely = 0.6)
port_combobox = ttk.Combobox(window, values=available_ports)
if available_ports:
    port_combobox.set(available_ports[0])
port_combobox.place(relx = serial_port_x,rely = 0.62)
    # 波特率选择下拉框
baudrates = [5200, 9600, 115200, 230400]
baudrate_label = tk.Label(window, text="选择波特率:")
baudrate_label.place(relx = serial_port_x,rely = 0.68)
baudrate_combobox = ttk.Combobox(window, values=baudrates)
baudrate_combobox.set(115200)
baudrate_combobox.place(relx = serial_port_x,rely = 0.70)
    # 切换设备按钮
confirm_button = tk.Button(window, 
    text="尝试切换链接",
    width=16, height=2,
    font=('Arial', 12),bg = 'Pink',
    command=on_confirm
)
confirm_button.place(relx = serial_port_x,rely = 0.78)


window.mainloop()

# 当一切都完成后，关闭摄像头并释放所占资源
if CAMARA:
    camera.release()
    ser.ser_close()
cv.destroyAllWindows()