simple_list = [1, 2, 3, 4]
# del simple_list[0]
# print(simple_list)

simple_list.extend([5, 6, 7])

# print(simple_list)

d = {'name': 'jason'}
print(d.items())
for k, v in d.items():
    print(k, v)
del d['name']
# print(d)

s = {'jason', 'jamon', 'joyce'}
del s['jason']
# print(s)

t = ('jason', 'jamon', 'joyce')
del t[0]
# print(t)

greater = [el for el in simple_list if el > 0]  # greater = [1, 2, 3, 4]


bools_for_sim_list = [el > 0 for el in simple_list]
# [True, True, True, True, False]
all(bools_for_sim_list)  # False
any(bools_for_sim_list)  # True
