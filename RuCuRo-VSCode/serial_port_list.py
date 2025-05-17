import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import ttk


def list_com_ports():
    """列出电脑上所有可用的 COM 端口"""
    ports = serial.tools.list_ports.comports()
    com_ports = []
    for port, desc, hwid in sorted(ports):
        com_ports.append(port)
    return com_ports


arduino_ser = None


def ser_init(port, baudrate=115200):
    global arduino_ser
    try:
        arduino_ser = serial.Serial(port, baudrate)
        if not arduino_ser.is_open:
            arduino_ser.open()
        print(f"成功打开串口 {port}，波特率 {baudrate}")
    except serial.SerialException as e:
        print(f"无法打开串口 {port}: {e}")


def ser_close():
    if arduino_ser and arduino_ser.is_open:
        arduino_ser.close()


def ser_send(string):
    if arduino_ser and arduino_ser.is_open:
        arduino_ser.write(string)


def ser_recv():
    if arduino_ser and arduino_ser.is_open:
        while True:
            # 获得接收缓冲区字符
            count = arduino_ser.in_waiting
            # 读取内容并显示
            if count == 0:
                break
            recv = arduino_ser.read(count)
            print(recv)
            # 清空接收缓冲区
            arduino_ser.reset_input_buffer()
            # 必要的软件延时
            time.sleep(0.1)
            return recv
    return None


def on_confirm():
    selected_port = port_combobox.get()
    selected_baudrate = int(baudrate_combobox.get())
    ser_init(selected_port, selected_baudrate)
    root.destroy()


def refresh_ports():
    available_ports = list_com_ports()
    port_combobox['values'] = available_ports
    if available_ports:
        port_combobox.set(available_ports[0])
    root.after(2000, refresh_ports)


# 创建主窗口
root = tk.Tk()
root.title("选择串口和波特率")

# 设置窗口大小
root.geometry("400x160")

# 获取可用串口
available_ports = list_com_ports()

# 串口选择下拉框
port_label = tk.Label(root, text="选择串口:")
port_label.pack(pady=10)
port_combobox = ttk.Combobox(root, values=available_ports)
if available_ports:
    port_combobox.set(available_ports[0])
port_combobox.pack(pady=5)

# 波特率选择下拉框
baudrates = [9600, 115200, 230400]
baudrate_label = tk.Label(root, text="选择波特率:")
baudrate_label.pack(pady=10)
baudrate_combobox = ttk.Combobox(root, values=baudrates)
baudrate_combobox.set(115200)
baudrate_combobox.pack(pady=5)

# 确认按钮
confirm_button = tk.Button(root, text="确认", command=on_confirm)
confirm_button.pack(pady=20)

# 启动刷新任务
refresh_ports()

# 运行主循环
root.mainloop()

if arduino_ser and arduino_ser.is_open:
    ser_send(b"rRZzXfxFRRXX")
    received_data = ser_recv()
    if received_data:
        print(f"接收到的数据: {received_data}")
    ser_close()
    