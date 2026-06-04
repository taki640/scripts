import sys

if len(sys.argv) < 2:
    print("Error: No strings provided")
    exit(1)

replace_text = ''
if len(sys.argv) >= 3 and (sys.argv[1] == "-r" or sys.argv[1] == "--replace"):
    replace_text = sys.argv[2]

disallowed_chars = [ '<', '>', ':', '"', '/', '\\', '|', '?', '*' ]

start_index = 1
if replace_text != '':
    start_index = 3

for str in sys.argv[start_index:]:
    for c in disallowed_chars:
        str = str.replace(c, replace_text)
    print(str)
