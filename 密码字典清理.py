import string
import time
import os

# 定义一个包含所有有效字符的集合
valid_characters = string.ascii_letters + string.digits + string.punctuation + " "

def is_valid_password(password):
    """检查密码是否仅包含有效字符"""
    return all(char in valid_characters for char in password)

def process_file(input_file, valid_output_file, invalid_output_file, chunk_size=10000):
    """逐行读取文件并筛选有效密码，分批写入输出文件"""
    total_lines = sum(1 for _ in open(input_file, 'r', encoding='utf-8'))  # 获取文件的总行数
    print(f"文件总行数：{total_lines}")

    start_time = time.time()  # 记录开始时间
    processed_lines = 0  # 已处理行数
    valid_count = 0  # 有效密码行数
    invalid_count = 0  # 无效密码行数
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(valid_output_file, 'w', encoding='utf-8') as valid_file, \
         open(invalid_output_file, 'w', encoding='utf-8') as invalid_file:
        batch_valid = []
        batch_invalid = []
        for line_number, password in enumerate(infile, 1):
            password = password.strip()  # 去除两端空白字符
            if is_valid_password(password):
                batch_valid.append(password)
                valid_count += 1
            else:
                batch_invalid.append(password)
                invalid_count += 1
            
            # 如果达到了批处理大小，写入到文件并清空批次
            if len(batch_valid) >= chunk_size:
                valid_file.write("\n".join(batch_valid) + "\n")
                batch_valid.clear()

            if len(batch_invalid) >= chunk_size:
                invalid_file.write("\n".join(batch_invalid) + "\n")
                batch_invalid.clear()

            # 每处理一定行数，计算进度并显示
            processed_lines += 1
            if processed_lines % 100000 == 0 or processed_lines == total_lines:
                elapsed_time = time.time() - start_time  # 计算已用时间
                remaining_lines = total_lines - processed_lines
                estimated_time = (elapsed_time / processed_lines) * remaining_lines if processed_lines > 0 else 0
                print(f"已处理 {processed_lines}/{total_lines} 行 | 预计剩余时间: {format_time(estimated_time)}")
        
        # 写入最后一批（如果有剩余）
        if batch_valid:
            valid_file.write("\n".join(batch_valid) + "\n")
        if batch_invalid:
            invalid_file.write("\n".join(batch_invalid) + "\n")

    elapsed_time = time.time() - start_time  # 总耗时
    print(f"原文件一共有 {total_lines} 行，有效密码行数 {valid_count} 行，无效密码行数 {invalid_count} 行，总耗时 {format_time(elapsed_time)}")

def format_time(seconds):
    """格式化时间为小时:分钟:秒"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

# 获取用户输入的文件路径，并去除多余的空格和引号
input_file = input("请输入密码文件路径: ").strip().strip("'\"")
# 创建有效和无效密码输出文件路径
valid_output_file = input_file.rsplit('.', 1)[0] + "_OK.txt"
invalid_output_file = input_file.rsplit('.', 1)[0] + "_NG.txt"
# 调用函数，处理文件
process_file(input_file, valid_output_file, invalid_output_file)
