import csv
import re
import os
from glob import glob

def is_english(line):
    # 检查是否主要是英文字符（包括标点符号和空格）
    line_stripped = line.strip()
    if not line_stripped:
        return False
    
    # 如果以 * 开头（如 *gasp*）或包含常见英文标点
    if line_stripped.startswith('*') or line_stripped.startswith('...'):
        return True
    
    # 计算英文字符占比
    letters = re.findall(r'[A-Za-z]', line_stripped)
    if not letters:
        return False
    
    # 如果英文字符占比超过30%，认为是英文
    total_chars = len([c for c in line_stripped if c != ' '])
    if total_chars == 0:
        return False
    
    ratio = len(letters) / total_chars
    return ratio > 0.3

def is_tag(line):
    return line.strip().startswith('<') and line.strip().endswith('>')

def is_punctuation_only(line):
    # 检查是否只有标点符号、空格、特殊符号
    line_stripped = line.strip()
    if not line_stripped:
        return True
    # 只允许的字符：标点符号、空格、...、‥‥、*等
    punctuation_pattern = r'^[‥\*\s\.\,\!\!\?\-\:\;\(\)\[\]\{\}\<\>\/\\|`~@#$%^&_+=]*$'
    return bool(re.match(punctuation_pattern, line_stripped))

def parse_text(text):
    lines = text.splitlines()
    
    # 先按空行分割成段落
    paragraphs = []
    current_para = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # 如果是空行，结束当前段落
        if not line_stripped:
            if current_para:
                paragraphs.append(current_para)
                current_para = []
            continue
        
        # 跳过纯标签行和纯标点行
        if is_tag(line_stripped) or is_punctuation_only(line_stripped):
            continue
        
        current_para.append(line_stripped)
    
    # 添加最后一个段落
    if current_para:
        paragraphs.append(current_para)
    
    # 处理每个段落
    results = []
    for para in paragraphs:
        # 分离日文和英文
        jp_lines = []
        en_lines = []
        
        for line in para:
            if is_english(line):
                en_lines.append(line)
            else:
                jp_lines.append(line)
        
        # 合并日文和英文
        jp_text = " ".join(jp_lines) if jp_lines else ""
        en_text = " ".join(en_lines) if en_lines else ""
        
        # 只有当段落有内容时才添加
        if jp_text or en_text:
            results.append([jp_text, en_text])
    
    return results


def convert_all_txt_to_csv():
    txt_files = glob("*.txt")
    
    for file in txt_files:
        print(f"处理文件: {file}")
        
        with open(file, "r", encoding="utf-16") as f:
            text = f.read()
        
        pairs = parse_text(text)
        
        # 生成同名的csv文件
        csv_filename = os.path.splitext(file)[0] + ".csv"
        
        # 为每个txt单独写入csv
        with open(csv_filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["Japanese", "English", "Note"])
            
            for jp, en in pairs:
                writer.writerow([jp, en, file])
        
        print(f"  生成: {csv_filename}, 共 {len(pairs)} 条")


if __name__ == "__main__":
    convert_all_txt_to_csv()