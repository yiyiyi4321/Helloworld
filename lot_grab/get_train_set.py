import pandas as pd

def get_code(year, turn):
        str_code = "{0:02d}{1:03d}".format(year, turn)
        return str_code

pos_data = pd.read_csv('lot_500_ssq.txt')
pos_set = set()

for idx in range(len(pos_data)):
        row = pos_data.iloc[idx, :]
        year = row['year']
        turn = row['turn']
        code = get_code(year, turn)
        pos_set.add(code)

ssq_data = pd.read_csv('lot_500_ssq_all.txt')
train_set_file = open("train_set.csv", "w")
head_line = ""
for t in range(0, -1, -1):
        for f in range(33+16):
                head_line += "t" + str(t) + "_f" + str(f) + ","
head_line += "y"
train_set_file.write(head_line+'\n')

for idx in range(len(ssq_data)):
        row = ssq_data.iloc[idx, :]
        red_list = []
        year = row['year']
        turn = row['turn']
        code = get_code(year, turn)
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
        if code in pos_set:
                line += "1"
        else:
                line += "0"
        train_set_file.write(line+'\n')
train_set_file.close()

