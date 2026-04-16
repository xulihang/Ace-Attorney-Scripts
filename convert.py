import csv
import re
import os
from glob import glob

def is_english(line):
    return bool(re.search(r'[A-Za-z]', line))

def is_tag(line):
    return line.strip().startswith('<') and line.strip().endswith('>')

def parse_text(text):
    lines = text.splitlines()

    results = []
    jp_buffer = []
    en_buffer = []
    mode = "jp"

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if is_tag(line):
            continue

        if is_english(line):
            en_buffer.append(line)
            mode = "en"
        else:
            if mode == "en" and jp_buffer:
                results.append([
                    "".join(jp_buffer),
                    " ".join(en_buffer)
                ])
                jp_buffer = []
                en_buffer = []

            jp_buffer.append(line)
            mode = "jp"

    if jp_buffer or en_buffer:
        results.append([
            "".join(jp_buffer),
            " ".join(en_buffer)
        ])

    return results


def convert_all_txt_to_csv(output_file="output.csv"):
    all_rows = []

    txt_files = glob("*.txt")

    for file in txt_files:
        with open(file, "r", encoding="utf-16") as f:
            text = f.read()

        pairs = parse_text(text)

        for jp, en in pairs:
            all_rows.append([jp, en, file])

    # 写入 CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Japanese", "English", "Note"])
        writer.writerows(all_rows)


if __name__ == "__main__":
    convert_all_txt_to_csv()
