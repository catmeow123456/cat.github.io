import os

path = './outputs'
files = os.listdir(path)
file_size_list = []
total = 0
totalchars = 0
for file in files:
    if not file.endswith('.txt') or not file.startswith('message'):
        continue
    with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
        # read all lines
        lines = f.readlines()
        # count the number of lines
        num_lines = len(lines)
        total += num_lines
        for line in lines:
            # count the number of words in each line
            num_chars = len(line)
            totalchars += num_chars
print(total, totalchars)
