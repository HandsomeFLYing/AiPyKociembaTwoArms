import tkinter as tk
import os
from tkinter import ttk, messagebox
import random

class RubiksCubeVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("魔方三面视图可视化")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")
        
        # 设置中文字体
        self.font_config()
        
        # 魔方颜色配置
        self.colors = ['green', 'red', 'orange', 'white', 'yellow', 'blue']
        self.color_codes = ['g', 'r', 'o', 'w', 'y', 'b']
        self.face_names = ['右面', '前面', '左面', '上面', '下面', '后面']
        
        # 创建界面
        self.create_widgets()
        
        # 初始化魔方状态
        self.initialize_cube_state()
        
        # 绘制魔方
        self.draw_cube()
    
    def font_config(self):
        """配置中文字体"""
        try:
            # 尝试设置常见中文字体
            self.default_font = ('SimHei', 10)
            self.title_font = ('SimHei', 16, 'bold')
            self.button_font = ('SimHei', 10, 'bold')
        except:
            # 如果无法设置中文字体，则使用默认字体
            self.default_font = ('Arial', 10)
            self.title_font = ('Arial', 16, 'bold')
            self.button_font = ('Arial', 10, 'bold')
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建顶部标题
        title_frame = tk.Frame(self.root, bg="#f0f0f0")
        title_frame.pack(pady=10)
        
        title_label = tk.Label(title_frame, text="魔方三面视图可视化", font=self.title_font, bg="#f0f0f0")
        title_label.pack()
        
        # 创建控制面板
        control_frame = tk.Frame(self.root, bg="#f0f0f0", relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 添加打乱按钮
        scramble_btn = tk.Button(control_frame, text="打乱魔方", command=self.scramble_cube,
                                font=self.button_font, bg="#4CAF50", fg="white", padx=10, pady=5)
        scramble_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        # 添加重置按钮
        reset_btn = tk.Button(control_frame, text="重置魔方", command=self.reset_cube,
                             font=self.button_font, bg="#2196F3", fg="white", padx=10, pady=5)
        reset_btn.pack(side=tk.LEFT, padx=10, pady=5)
        
        # 帮助按钮
        help_btn = tk.Button(control_frame, text="帮助", command=self.show_help,
                            font=self.button_font, bg="#FF9800", fg="white", padx=10, pady=5)
        help_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # 创建画布框架
        canvas_frame = tk.Frame(self.root, bg="#f0f0f0")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 第一个三面视图 - 右侧、前面、上面
        self.canvas1 = tk.Canvas(canvas_frame, width=480, height=360, bg="white")
        self.canvas1.pack(side=tk.LEFT, padx=10, pady=10)
        
        # 第二个三面视图 - 左侧、后面、下面
        self.canvas2 = tk.Canvas(canvas_frame, width=480, height=360, bg="white")
        self.canvas2.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # 创建底部信息栏
        info_frame = tk.Frame(self.root, bg="#e0e0e0", height=30)
        info_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        info_label = tk.Label(info_frame, text="拖动鼠标可旋转魔方 (功能开发中)", font=self.default_font, bg="#e0e0e0")
        info_label.pack(pady=5)
    
    def initialize_cube_state(self):
        """初始化魔方状态"""
        self.cube_state = {}
        for color, code in zip(self.colors, self.color_codes):
            # 每个面初始化为同一种颜色
            self.cube_state[code] = [color] * 9
    
    def draw_cube(self):
        """绘制魔方的两个三面视图"""
        # 清空画布
        self.canvas1.delete("all")
        self.canvas2.delete("all")
        
        # 绘制第一个三面视图 (右侧、前面、上面)
        self.draw_three_faces(self.canvas1, [0, 1, 3])  # 右侧、前面、上面
        
        # 绘制第二个三面视图 (左侧、后面、下面)
        self.draw_three_faces(self.canvas2, [2, 5, 4])  # 左侧、后面、下面
    
    def draw_three_faces(self, canvas, face_indices):
        """绘制三个魔方面"""
        # 定义三个面的位置
        positions = [
            (1, 1),  # 中间位置 (前面)
            (0, 1),  # 左边位置 (左面/右面)
            (1, 0)   # 上面位置 (上面/下面)
        ]
        
        # 绘制三个面
        for i, face_idx in enumerate(face_indices):
            color = self.colors[face_idx]
            color_code = self.color_codes[face_idx]
            col, row = positions[i]
            
            x = 10 + col * 160
            y = 10 + row * 160
            
            # 绘制面标题
            canvas.create_text(x + 80, y - 10, text=self.face_names[face_idx], 
                              font=self.default_font, fill="black")
            
            # 获取该面的颜色列表
            color_list = self.cube_state.get(color_code, [color] * 9)
            
            # 绘制9个小方块
            for i in range(3):
                for j in range(3):
                    # 计算小方块位置
                    x1 = x + 50 * i
                    y1 = y + 50 * j
                    x2 = x + 50 * (i + 1)
                    y2 = y + 50 * (j + 1)
                    
                    # 绘制小方块
                    fill_color = color_list[i + j * 3]
                    canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black", width=2)
                    
                    # 为了美观，在每个小方块中间添加一个小圆点
                    canvas.create_oval(x1 + 20, y1 + 20, x1 + 30, y1 + 30, fill="white", outline="")
    
    def scramble_cube(self):
        """打乱魔方"""
        # 简单打乱 - 随机改变每个面的几个方块颜色
        for color_code in self.color_codes:
            # 随机选择3-6个方块改变颜色
            num_changes = random.randint(3, 6)
            positions = random.sample(range(9), num_changes)
            
            # 为选中的方块随机选择颜色
            for pos in positions:
                # 选择一个不同的颜色
                new_color = random.choice([c for c in self.colors if c != self.colors[self.color_codes.index(color_code)]])
                self.cube_state[color_code][pos] = new_color
        
        # 重绘魔方
        self.draw_cube()
    
    def reset_cube(self):
        """重置魔方为初始状态"""
        self.initialize_cube_state()
        self.draw_cube()
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
        魔方三面视图可视化帮助
        
        1. 视图说明:
           - 左侧视图显示: 右面、前面、上面
           - 右侧视图显示: 左面、后面、下面
        
        2. 功能按钮:
           - 打乱魔方: 随机改变魔方的颜色状态
           - 重置魔方: 将魔方恢复到初始状态
        
        3. 后续功能开发中:
           - 鼠标拖动旋转魔方
           - 执行魔方转动算法
           - 显示魔方公式和步骤
        """
        messagebox.showinfo("帮助", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = RubiksCubeVisualizer(root)
    root.mainloop()    