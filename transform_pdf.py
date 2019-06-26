input_file = open('in.txt', 'r', encoding='utf-8')
output_file = open('out.txt', 'w', encoding='utf-8')

for line in input_file:
    if line.strip()[-1] == '-':
        output_file.write(line.strip()[:-1])
    else:
        output_file.write(line.strip() + ' ')

input_file.close()
output_file.close()
