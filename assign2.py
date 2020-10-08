names = ["nick", "jason", "nathanel", "pete", "natasha", "Ty", "Russell",
         "Victoria", "Samuel", "Romell", "Nicholas"]

for name in names:
    name_len = len(name)
    if name_len > 5 and name[0].lower() == "n":
        print(name)
    else:
        print(name_len)

while len(names) > 0:
    popped = names.pop()
    if len(popped) < 6:
        print(f'{popped} is less than 6 letters 😩')

print(names)
