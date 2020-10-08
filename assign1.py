age = int(input("Age: "))
name = input("Name: ")


def name_and_age(age=age, name=name):
    print(str(age)+name)


name_and_age()


def any_name_and_age(age, name):
    age = str(age)
    print(age+name)


def decades(a, n):
    a = int(age/10)
    print(f'{n} ,you have lived {a} decades')


# any_name_and_age(12, "Peter")
decades(age, name)
