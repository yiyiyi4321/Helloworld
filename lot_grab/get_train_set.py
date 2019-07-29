import pandas as pd

ssq_data = pd.read_csv('lot_500_ssq.txt')
line_rec = []
train_set_file = open("train_set.csv", "w")
head_line = ""
for t in range(7, -1, -1):
    for f in range(33+16):
        head_line += "t" + str(t) + "_f" + str(f) + ","
train_set_file.write(head_line[:-1]+'\n')
for idx in range(len(ssq_data)):
    row = ssq_data.iloc[idx, :]
    red_list = []
    red_list.append(int(row['r1']))
    red_list.append(int(row['r2']))
    red_list.append(int(row['r3']))
    red_list.append(int(row['r4']))
    red_list.append(int(row['r5']))
    red_list.append(int(row['r6']))
    blue = int(row['b'])
    line = ""
    for r in range(1, 34):
        if r in red_list:
            line += "1,"
        else:
            line += "0,"
    for b in range(1, 17):
        if b == blue:
            line += "1,"
        else:
            line += "0,"
    if len(line_rec) > 200:
        output_line = ""
        for i in range(-7, 0):
            output_line += line_rec[i]
        output_line += line[:-1]
        train_set_file.write(output_line+'\n')
    line_rec.append(line)
train_set_file.close()

