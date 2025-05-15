import os

print(os.getcwd())
label_folder = 'C:/Users/user/Desktop/sinkhole dataset.v1i.yolov8/valid/labels'  # 라벨 폴더 경로

for filename in os.listdir(label_folder):
    if filename.endswith('.txt'):
        filepath = os.path.join(label_folder,filename)
        with open(filepath, 'r') as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if parts:
                # 클래스 0을 3으로 변경
                if parts[0] == '0':
                    parts[0] = '3'
                new_lines.append(' '.join(parts))
        with open(filepath, 'w') as f:
            f.write('\n'.join(new_lines))
