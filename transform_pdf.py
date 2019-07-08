import webbrowser

input_file = open('in.txt', 'r', encoding='utf-8')

output = ""
for line in input_file:
    if len(line) > 1 and line.strip()[-1] == '-':
        output += line.strip()[:-1]
    else:
        output += line.strip() + ' '

url = 'https://translate.google.com/#view=home&op=translate&sl=auto&tl=zh-CN&text='
url += output.replace(' ', '%20')
print(output)
webbrowser.open(url)

input_file.close()
