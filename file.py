# Creates 'demo.txt' file and in mode=(w) writes to it.
# f = open('demo.txt', mode='x')
# f.write('hello from python\n')
# close() closes and saves file immediately
# f.close()

# f = open('demo.txt', mode='r')
# file_content = f.read()
# f.close()
# print(file_content)

# f = open('demo.txt', mode='a')
# f.write("cool,whats going on?\n")
# f.close()

# r = open('demo.txt', mode='r')
# read_content = r.read()
# print(read_content)

# f = open('demo.txt', mode='r')
# content_file = f.readlines()
# f.close()

# print(content_file[-1])
# f = open('demo.txt', mode='w')

# f.write('Hello from Python!')


# f.close()

# f = open('demo.txt', mode='a')
# f.write('How are you liking Python?\n')
# f.close()

# f = open('demo.txt', mode='r')
# file_content = f.read()
# f.close()
# print(file_content)
# f = open('demo.txt', mode='a')
# f.write("i'm pretty good Sir\n")

# f.close()
# f = open('demo.txt', mode='r')

# the_lines = f.readlines()

# for line in the_lines:
#     print(line)

# the_line = f.readline()
# while the_line:
#     print(the_line)
#     the_line = f.readline()
# f.close()


with open('demo.txt', mode='r') as f:
    for line in f.readlines():
        print(line)
