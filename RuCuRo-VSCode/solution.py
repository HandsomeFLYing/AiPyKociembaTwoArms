import kociemba as kc

# 颜色列表转魔方序列列表
def color2code(line_list):
    # U R F D L B
    # 白 红 绿 黄 橙 蓝
    if (line_list == 'white'):
        line_list = 'U'
    elif (line_list == 'yellow'):
        line_list = 'D'
    elif (line_list == 'green'):
        line_list = 'F'
    elif (line_list == 'orange'):
        line_list = 'L'
    elif (line_list == 'red'):
        line_list = 'R'
    elif (line_list == 'blue'):
        line_list = 'B'
    else:
        line_list = 'N'
    return line_list
# 魔方序列列表转字符串
def code2str():
    color_ = ['w','r','g','y','o','b']
    color_list = []
    for n in range(len(color_)):
        f = open('data/'+color_[n]+'.txt',mode='r',encoding='utf-8')
        for line in f.readlines(): #依次读取每行
            line_list = line.strip()
            color_list.append(color2code(line_list)) #去掉每行头尾空白
    code_str = ''
    for i in range(len(color_list)):
        code_str += color_list[i]
    # print(code_str)
    return code_str

# 魔方字符串转电机字符串
import kociemba as kc

def remove_adjacent_duplicates(code_str):
    """移除相邻重复字符"""
    result = list(code_str)
    i = 0
    while i < len(result) - 1:
        if result[i] == result[i+1]:
            del result[i]
        else:
            i += 1
    return ''.join(result)

def kociemba_solve(code_str):
    """使用kociemba求解魔方"""
    try:
        return kc.solve(code_str)
    except Exception as e:
        print(f"Kociemba求解错误: {e}")
        return ''

def process_kociemba_notation(kc_str):
    """处理Kociemba符号表示"""
    cube_str = ''
    for i, c in enumerate(kc_str):
        if c == ' ':
            continue
        if c == '2':
            cube_str += kc_str[i-1]  # 90度旋转两次等效于180度
        elif c == "'":
            cube_str = cube_str[:-1] + kc_str[i-1].lower()  # 逆旋表示
        else:
            cube_str += c
    return cube_str

def get_rotation_mapping(loop_num):
    """根据循环编号获取旋转映射"""
    u_mapping = 'ZRz' if loop_num >= 8 else 'xFX'
    u_prime_mapping = 'Zrz' if loop_num % 8 >= 4 else 'xfX'
    d_mapping = 'zRZ' if loop_num % 4 >= 2 else 'XFx'
    d_prime_mapping = 'zrZ' if loop_num % 2 else 'Xfx'
    
    return {
        'R': 'R', 'r': 'r',
        'L': 'ZZRZZ', 'l': 'ZZrZZ',
        'U': u_mapping, 'u': u_prime_mapping,
        'D': d_mapping, 'd': d_prime_mapping,
        'F': 'F', 'f': 'f',
        'B': 'XXFXX', 'b': 'XXfXX'
    }

def apply_initial_rotation(step_str, sort_str):
    """根据排序字符串应用初始旋转"""
    rotation_map = {
        'ob': ' ', 'ow': 'x', 'og': 'XX', 'oy': 'X',
        'rb': 'ZZ', 'rw': 'ZZx', 'rg': 'ZZXX', 'ry': 'xZZ',
        'yb': 'z', 'yo': 'xz', 'yg': 'XXz', 'yr': 'Xz',
        'wb': 'Z', 'wo': 'XZ', 'wg': 'XXZ', 'wr': 'xZ',
        'go': 'xzX', 'gy': 'zX', 'gr': 'xZx', 'gw': 'Zx',
        'br': 'xZX', 'bw': 'zx', 'bo': 'XZX', 'by': 'ZX'
    }
    return rotation_map.get(sort_str, '') + step_str

def optimize_step_sequence(step_str):
    """优化步骤序列，合并和简化操作"""
    # 优化X/x和Z/z旋转
    optimized = step_str
    
    # 处理X/x和Z/z的交换律
    for _ in range(6):
        new_str = ''
        i = 0
        while i < len(optimized):
            if i < len(optimized) - 1:
                if (optimized[i] in 'Xx') and (optimized[i+1] in 'Rr'):
                    new_str += optimized[i+1] + optimized[i]
                    i += 2
                elif (optimized[i] in 'Zz') and (optimized[i+1] in 'Ff'):
                    new_str += optimized[i+1] + optimized[i]
                    i += 2
                else:
                    new_str += optimized[i]
                    i += 1
            else:
                new_str += optimized[i]
                i += 1
        if new_str == optimized:
            break
        optimized = new_str
    
    # 消除四个连续相同的旋转
    for _ in range(6):
        new_str = ''
        i = 0
        while i < len(optimized):
            if i < len(optimized) - 3:
                if (optimized[i] == optimized[i+1] == optimized[i+2] == optimized[i+3] 
                    and optimized[i] in 'XZ'):
                    i += 4  # 四个相同旋转抵消
                else:
                    new_str += optimized[i]
                    i += 1
            else:
                new_str += optimized[i]
                i += 1
        if new_str == optimized:
            break
        optimized = new_str
    
    # 消除三个连续相同的旋转
    for _ in range(6):
        new_str = ''
        i = 0
        while i < len(optimized):
            if i < len(optimized) - 2:
                if (optimized[i] == optimized[i+1] == optimized[i+2] 
                    and optimized[i] in 'XZ'):
                    new_str += optimized[i].lower()  # 三个相同旋转等效于一个反向旋转
                    i += 3
                else:
                    new_str += optimized[i]
                    i += 1
            else:
                new_str += optimized[i]
                i += 1
        if new_str == optimized:
            break
        optimized = new_str
    
    # 消除相反的旋转对
    for _ in range(6):
        new_str = ''
        i = 0
        while i < len(optimized):
            if i < len(optimized) - 1:
                if ((optimized[i] == 'x' and optimized[i+1] == 'X') or
                    (optimized[i] == 'X' and optimized[i+1] == 'x') or
                    (optimized[i] == 'z' and optimized[i+1] == 'Z') or
                    (optimized[i] == 'Z' and optimized[i+1] == 'z')):
                    i += 2  # 抵消
                else:
                    new_str += optimized[i]
                    i += 1
            else:
                new_str += optimized[i]
                i += 1
        if new_str == optimized:
            break
        optimized = new_str
    
    # 再次处理X/x和Z/z的交换律
    for _ in range(6):
        new_str = ''
        i = 0
        while i < len(optimized):
            if i < len(optimized) - 1:
                if (optimized[i] in 'Xx') and (optimized[i+1] in 'Rr'):
                    new_str += optimized[i+1] + optimized[i]
                    i += 2
                elif (optimized[i] in 'Zz') and (optimized[i+1] in 'Ff'):
                    new_str += optimized[i+1] + optimized[i]
                    i += 2
                else:
                    new_str += optimized[i]
                    i += 1
            else:
                new_str += optimized[i]
                i += 1
        if new_str == optimized:
            break
        optimized = new_str
    
    # 截断到最后一个有效操作
    end_index = 0
    for i in range(len(optimized)-1, -1, -1):
        if optimized[i] in 'RrFf':
            end_index = i + 1
            break
    optimized = optimized[:end_index]
    
    return optimized

def verify_step_sequence(step_str):
    """验证步骤序列，转换为标准符号表示"""
    verification_map = {
        'r': "R'", 'f': "F'", 'z': "Z'", 'x': "X'"
    }
    return ''.join(verification_map.get(c, c) for c in step_str)

def str2step(code_str):
    """将魔方字符串转换为电机控制字符串"""
    # 移除相邻重复字符
    processed_code = remove_adjacent_duplicates(code_str)
    
    # 检查是否为六面状态
    if len(processed_code) != 6:
        print("(str2step):")
        print(code_str)
        print()
        try:
            kc_str = kociemba_solve(code_str)
            kc_flag = 0
        except:
            kc_str = ''
    else:
        kc_str = ''
    
    print('六面最佳解法： ' + kc_str)
    
    # 处理Kociemba符号
    cube_str = process_kociemba_notation(kc_str)
    
    # 读取排序信息
    try:
        with open('data/sort.txt', 'r', encoding='utf-8') as f:
            sort_str = f.read(2)
    except Exception as e:
        print(f"读取排序文件错误: {e}")
        sort_str = 'ob'  # 默认值
    
    # 生成12种可能的步骤序列
    step_list = []
    for loop_num in range(12):
        # 获取旋转映射
        rotation_map = get_rotation_mapping(loop_num)
        
        # 转换为电机步骤
        step_str = ''.join(rotation_map.get(c, '') for c in cube_str)
        
        # 应用初始旋转
        step_str = apply_initial_rotation(step_str, sort_str)
        
        # 优化步骤序列
        optimized_step_str = optimize_step_sequence(step_str)
        
        step_list.append(optimized_step_str)
    
    # 选择最短的步骤序列
    shortest_step_str = min(step_list, key=len)
    
    # 验证步骤序列
    verified_str = verify_step_sequence(shortest_step_str)
    print_str = (f'六面解法： {kc_str}\n两面解法:\n{verified_str}\n共{len(shortest_step_str)}步')
    
    print('step_str: ' + shortest_step_str)
    return shortest_step_str, print_str