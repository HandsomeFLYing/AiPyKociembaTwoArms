import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Button, Slider
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.colors as mcolors
import random
import os

# 设置中文字体
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

class RubiksCube3D:
    def __init__(self):
        # 定义魔方的颜色映射
        self.color_map = {
            'white': '#FFFFFF',  # 白色
            'yellow': '#FFFF00',  # 黄色
            'red': '#FF0000',    # 红色
            'blue': '#0000FF',   # 蓝色
            'orange': '#FF8C00', # 橙色
            'green': '#008000',  # 绿色
            'gray': '#808080',   # 灰色（用于实体内部）
        }
        
        # 定义面的缩写和对应的文件名
        self.face_names = {
            'U': ('up', 'u', 'w'),    # 上面 - 白色
            'D': ('down', 'd', 'y'),  # 下面 - 黄色
            'F': ('front', 'f', 'r'), # 前面 - 红色
            'B': ('back', 'b', 'b'),  # 后面 - 蓝色
            'L': ('left', 'l', 'o'),  # 左面 - 橙色
            'R': ('right', 'r', 'g')  # 右面 - 绿色
        }
        
        # 面的方向向量
        self.face_directions = {
            'U': (0, 1, 0),   # 上: Y+
            'D': (0, -1, 0),  # 下: Y-
            'F': (0, 0, 1),   # 前: Z+
            'B': (0, 0, -1),  # 后: Z-
            'L': (-1, 0, 0),  # 左: X-
            'R': (1, 0, 0)    # 右: X+
        }
        
        # 初始化魔方状态
        self.reset_cube()
        
        # 创建图形和两个3D轴
        self.fig = plt.figure(figsize=(15, 6))
        
        # 左侧视图 - 不透明实体魔方
        self.ax1 = self.fig.add_subplot(121, projection='3d')
        # 右侧视图 - 半透明面状魔方
        self.ax2 = self.fig.add_subplot(122, projection='3d')
        
        # 设置按钮和滑块的位置
        self.fig.subplots_adjust(bottom=0.2, wspace=0.1)
        
        # 创建控制按钮
        self.create_controls()
        
        # 绘制魔方
        self.draw_cube()
        
        # 设置初始视角
        self.ax1.view_init(elev=30, azim=45)  # 从左前上方观察
        self.ax2.view_init(elev=-30, azim=45)  # 从底部向上观察
        
        # 显示提示信息
        print("程序已启动，左侧为不透明实体魔方，右侧为半透明面状魔方。")
        print("请点击'加载文件'按钮从data目录导入颜色配置。")
        
        # 显示图形
        plt.show()
    
    def reset_cube(self):
        """重置魔方到初始状态（使用默认配色）"""
        self.cube = np.zeros((3, 3, 3), dtype=object)
        
        # 初始化每个小方块的颜色为面的缩写（U/D/F/B/L/R）
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    # 计算中心位置
                    center_x = x - 1
                    center_y = y - 1
                    center_z = z - 1
                    
                    # 确定每个块的面和朝向
                    faces = []
                    
                    # X方向
                    if center_x < 0:  # 左侧
                        faces.append( ('L', (-1, 0, 0)) )  # 左面朝左
                    elif center_x > 0:  # 右侧
                        faces.append( ('R', (1, 0, 0)) )   # 右面朝右
                    
                    # Y方向
                    if center_y < 0:  # 下侧
                        faces.append( ('D', (0, -1, 0)) )  # 下面朝右
                    elif center_y > 0:  # 上侧
                        faces.append( ('U', (0, 1, 0)) )   # 上侧朝上
                    
                    # Z方向
                    if center_z < 0:  # 后侧
                        faces.append( ('B', (0, 0, -1)) )  # 后朝后
                    elif center_z > 0:  # 前侧
                        faces.append( ('F', (0, 0, 1)) )   # 前朝前
                    
                    self.cube[x, y, z] = faces
    def reset_cube_r(self):
        """重置魔方到初始还原状态"""
        self.cube = np.zeros((3, 3, 3), dtype=object)
        
        # 初始化每个小方块的颜色为标准还原状态
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    # 计算中心位置
                    center_x = x - 1
                    center_y = y - 1
                    center_z = z - 1
                    
                    # 确定每个块的面和朝向
                    faces = []
                    
                    # X方向
                    if center_x < 0:  # 左侧
                        faces.append( ('orange', (-1, 0, 0)) )  # 左面朝左
                    elif center_x > 0:  # 右侧
                        faces.append( ('green', (1, 0, 0)) )   # 右面朝右
                    
                    # Y方向
                    if center_y < 0:  # 下侧
                        faces.append( ('yellow', (0, -1, 0)) )  # 下面朝下
                    elif center_y > 0:  # 上侧
                        faces.append( ('white', (0, 1, 0)) )   # 上侧朝上
                    
                    # Z方向
                    if center_z < 0:  # 后侧
                        faces.append( ('blue', (0, 0, -1)) )  # 后朝后
                    elif center_z > 0:  # 前侧
                        faces.append( ('red', (0, 0, 1)) )   # 前朝前
                    
                    self.cube[x, y, z] = faces
    
    def load_cube_from_files(self):
        """从文件加载魔方每个面的颜色配置"""
        # 创建一个临时的颜色映射字典
        face_color_map = {}
        
        for face, (long_name, short_name, file_prefix) in self.face_names.items():
            color_list = self.read_face_colors(file_prefix)
            if color_list:
                # 为这个面创建9个位置的颜色映射
                face_positions = self.get_face_positions(face)
                for i, (x, y, z) in enumerate(face_positions):
                    if i < len(color_list):
                        face_color_map[(x, y, z, face)] = color_list[i]
        
        # 应用颜色到每个块的面上
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    new_faces = []
                    for face, direction in self.cube[x, y, z]:
                        # 检查这个面是否有颜色配置
                        if (x, y, z, face) in face_color_map:
                            new_faces.append( (face_color_map[(x, y, z, face)], direction) )
                        else:
                            # 没有配置，使用默认颜色
                            default_colors = {
                                'U': 'white',
                                'D': 'yellow',
                                'F': 'red',
                                'B': 'blue',
                                'L': 'orange',
                                'R': 'green'
                            }
                            new_faces.append( (default_colors[face], direction) )
                    
                    self.cube[x, y, z] = new_faces
    
    def get_face_positions(self, face):
        """获取一个面的9个方块位置"""
        positions = []
        
        if face == 'U':  # 上面 (y=2)
            for x in range(3):
                for z in range(3):
                    positions.append( (x, 2, z) )
        elif face == 'D':  # 下面 (y=0)
            for x in range(3):
                for z in range(3):
                    positions.append( (x, 0, z) )
        elif face == 'F':  # 前面 (z=2)
            for x in range(3):
                for y in range(3):
                    positions.append( (x, y, 2) )
        elif face == 'B':  # 后面 (z=0)
            for x in range(3):
                for y in range(3):
                    positions.append( (x, y, 0) )
        elif face == 'L':  # 左面 (x=0)
            for y in range(3):
                for z in range(3):
                    positions.append( (0, y, z) )
        elif face == 'R':  # 右面 (x=2)
            for y in range(3):
                for z in range(3):
                    positions.append( (2, y, z) )
        
        return positions
    
    def read_face_colors(self, file_prefix):
        """读取单个面的颜色配置文件"""
        # 检查文件是否存在
        file_paths = [
            f'data/{file_prefix}.txt',
        ]
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        # 读取前9行并去除空白
                        lines = [line.strip().lower() for line in f.readlines()[:9]]
                        # 过滤掉空行
                        colors = [color for color in lines if color]
                        
                        # 验证颜色名称有效性
                        valid_colors = []
                        for color in colors:
                            if color in self.color_map:
                                valid_colors.append(color)
                            else:
                                print(f"警告: 文件 {file_path} 中的颜色 '{color}' 无效，使用默认灰色")
                                valid_colors.append('#808080')
                        
                        # 确保有9个有效颜色
                        if len(valid_colors) < 9:
                            print(f"警告: 文件 {file_path} 中的颜色不足，需要9个颜色")
                            valid_colors.extend(['#808080'] * (9 - len(valid_colors)))
                        
                        return valid_colors[:9]
                except Exception as e:
                    print(f"读取文件 {file_path} 时出错: {e}")
                    return None
        
        # 如果没有找到文件，返回None
        return None
    
    def draw_cube(self):
        """绘制魔方的两个视图"""
        self.ax1.clear()
        self.ax2.clear()
        
        # 设置坐标轴范围
        for ax in [self.ax1, self.ax2]:
            ax.set_xlim([0, 3])
            ax.set_ylim([0, 3])
            ax.set_zlim([0, 3])
            ax.axis('off')
        
        # 为两个视图添加标题
        self.ax1.set_title("不透明实体魔方视图", fontsize=12)
        self.ax2.set_title("半透明面状魔方视图", fontsize=12)
        
        # 绘制每个小方块
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    # 左侧视图绘制不透明实体魔方
                    self.draw_solid_cubie(x, y, z, self.ax1, alpha=1.0)
                    # 右侧视图绘制半透明面状魔方
                    self.draw_cubie(x, y, z, self.ax2, alpha=0.8)
    
    def draw_cubie(self, x, y, z, ax, alpha=0.8):
        """绘制单个小方块及其可见面（面状魔方）"""
        # 获取小方块的面
        faces = self.cube[x, y, z]
        
        # 绘制每个可见面
        for face_info in faces:
            color, direction = face_info
            # 将颜色名称转换为颜色代码
            color_code = self.get_color_from_face(color)
            self.draw_face(x, y, z, direction, color_code, ax, alpha)
    
    def draw_solid_cubie(self, x, y, z, ax, alpha=1.0):
        """绘制单个小方块（实体魔方）"""
        # 获取小方块的面
        faces = self.cube[x, y, z]
        
        # 创建面的字典，以便查找
        face_dict = {face: color for color, face in faces}
        
        # 绘制所有六个面，外部面使用指定颜色，内部面使用灰色
        directions = [
            (1, 0, 0),  # 右
            (-1, 0, 0), # 左
            (0, 1, 0),  # 上
            (0, -1, 0), # 下
            (0, 0, 1),  # 前
            (0, 0, -1)  # 后
        ]
        
        for direction in directions:
            # 检查这个方向是否有外部面
            if direction in [d for _, d in faces]:
                # 找到对应的颜色
                for color, dir in faces:
                    if dir == direction:
                        color_code = self.get_color_from_face(color)
                        break
            else:
                # 内部面，使用灰色
                color_code = self.get_color_from_face('gray')
            
            self.draw_face(x, y, z, direction, color_code, ax, alpha)
    
    def get_color_from_face(self, face):
        """将面的缩写或颜色名称转换为颜色代码"""
        # 如果是颜色名称，转换为颜色代码
        if face in self.color_map:
            return self.color_map[face]
        
        # 如果是颜色代码，直接返回
        if isinstance(face, str) and face.startswith('#'):
            return face
        
        # 未知情况，返回默认灰色
        print(f"警告: 未知颜色值 '{face}'，使用默认灰色")
        return '#808080'
    
    def draw_face(self, x, y, z, direction, color, ax, alpha=0.8):
        """绘制小方块的一个面，基于方向向量"""
        # 微调面的位置，确保所有面都正确对齐
        eps = 0.01  # 微调值，避免面重叠产生的渲染问题
        
        # 根据方向向量确定顶点
        dx, dy, dz = direction
        
        if dx > 0:  # 右面
            vertices = [
                [x+1-eps, y, z],
                [x+1-eps, y+1, z],
                [x+1-eps, y+1, z+1],
                [x+1-eps, y, z+1]
            ]
        elif dx < 0:  # 左面
            vertices = [
                [x+eps, y, z],
                [x+eps, y+1, z],
                [x+eps, y+1, z+1],
                [x+eps, y, z+1]
            ]
        elif dy > 0:  # 上面
            vertices = [
                [x, y+1-eps, z],
                [x+1, y+1-eps, z],
                [x+1, y+1-eps, z+1],
                [x, y+1-eps, z+1]
            ]
        elif dy < 0:  # 下面
            vertices = [
                [x, y+eps, z],
                [x+1, y+eps, z],
                [x+1, y+eps, z+1],
                [x, y+eps, z+1]
            ]
        elif dz > 0:  # 前面
            vertices = [
                [x, y, z+1-eps],
                [x+1, y, z+1-eps],
                [x+1, y+1, z+1-eps],
                [x, y+1, z+1-eps]
            ]
        elif dz < 0:  # 后面
            vertices = [
                [x, y, z+eps],
                [x+1, y, z+eps],
                [x+1, y+1, z+eps],
                [x, y+1, z+eps]
            ]
        else:
            # 未知方向，不绘制
            return
        
        # 创建多边形对象
        poly = Poly3DCollection([vertices], 
                                facecolors=color, 
                                edgecolors='black', 
                                linewidths=1.0, 
                                alpha=alpha)
        ax.add_collection3d(poly)
    
    def create_controls(self):
        """创建控制面板"""
        # 重置按钮
        reset_ax = self.fig.add_axes([0.1, 0.1, 0.1, 0.04])
        self.reset_button = Button(reset_ax, '重置魔方')
        self.reset_button.on_clicked(lambda event: self.on_reset())
        
        # 打乱按钮
        scramble_ax = self.fig.add_axes([0.25, 0.1, 0.1, 0.04])
        self.scramble_button = Button(scramble_ax, '打乱魔方')
        self.scramble_button.on_clicked(lambda event: self.on_scramble())
        
        # 加载文件按钮
        load_ax = self.fig.add_axes([0.4, 0.1, 0.1, 0.04])
        self.load_button = Button(load_ax, '加载文件')
        self.load_button.on_clicked(lambda event: self.on_load())
        
        # 透明度控制滑块
        alpha_ax = self.fig.add_axes([0.55, 0.1, 0.35, 0.03])
        self.alpha_slider = Slider(alpha_ax, '右侧透明度', 0.1, 1.0, valinit=0.8)
        self.alpha_slider.on_changed(self.update_alpha)
        
        # 视角控制滑块 - 左侧视图
        elev1_ax = self.fig.add_axes([0.55, 0.15, 0.15, 0.03])
        azim1_ax = self.fig.add_axes([0.55, 0.2, 0.15, 0.03])
        
        self.elev1_slider = Slider(elev1_ax, '左仰角', -90, 90, valinit=30)
        self.azim1_slider = Slider(azim1_ax, '左方位角', 0, 360, valinit=45)
        
        self.elev1_slider.on_changed(lambda val: self.update_view(self.ax1, val, self.elev1_slider, self.azim1_slider))
        self.azim1_slider.on_changed(lambda val: self.update_view(self.ax1, val, self.elev1_slider, self.azim1_slider))
        
        # 视角控制滑块 - 右侧视图
        elev2_ax = self.fig.add_axes([0.75, 0.15, 0.15, 0.03])
        azim2_ax = self.fig.add_axes([0.75, 0.2, 0.15, 0.03])
        
        self.elev2_slider = Slider(elev2_ax, '右仰角', -90, 90, valinit=-30)
        self.azim2_slider = Slider(azim2_ax, '右方位角', 0, 360, valinit=45)
        
        self.elev2_slider.on_changed(lambda val: self.update_view(self.ax2, val, self.elev2_slider, self.azim2_slider))
        self.azim2_slider.on_changed(lambda val: self.update_view(self.ax2, val, self.elev2_slider, self.azim2_slider))
    
    def update_view(self, ax, val, elev_slider, azim_slider):
        """更新视图的视角"""
        elev = elev_slider.val
        azim = azim_slider.val
        ax.view_init(elev=elev, azim=azim)
        self.fig.canvas.draw_idle()
    
    def update_alpha(self, val):
        """更新右侧视图的透明度"""
        # 重新绘制魔方，只更新右侧视图的透明度
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    self.draw_solid_cubie(x, y, z, self.ax1, alpha=1.0)
                    self.draw_cubie(x, y, z, self.ax2, alpha=val)
        
        self.fig.canvas.draw_idle()
    
    def on_reset(self):
        """重置魔方状态到默认配色"""
        self.reset_cube()
        self.draw_cube()
        self.fig.canvas.draw_idle()
        print("已重置魔方为默认配色")
    
    def on_scramble(self):
        """随机打乱魔方"""
        # 简单的打乱算法 - 随机改变一些面的颜色
        for _ in range(20):
            # 随机选择一个面
            face = random.choice(['U', 'D', 'F', 'B', 'L', 'R'])
            
            # 随机选择一个小方块位置
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            z = random.randint(0, 2)
            
            # 确保该位置有这个面
            for i, (f, dir) in enumerate(self.cube[x, y, z]):
                if f == face:
                    # 随机改变这个面的颜色
                    new_color = random.choice(list(self.color_map.keys()))
                    self.cube[x, y, z][i] = (new_color, dir)
                    break
        
        self.draw_cube()
        self.fig.canvas.draw_idle()
        print("已随机打乱魔方")
    
    def on_load(self):
        """从文件加载魔方配置"""
        print("正在从data目录加载颜色配置...")
        self.load_cube_from_files()
        self.draw_cube()
        self.fig.canvas.draw_idle()
        print("加载完成")

if __name__ == "__main__":
    # 确保data目录存在
    if not os.path.exists('data'):
        os.makedirs('data')
        print("已创建'data'目录，请在其中放置魔方面的颜色配置文件")
    
    RubiksCube3D()