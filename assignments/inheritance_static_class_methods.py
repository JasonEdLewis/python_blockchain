
# #Class food with attributes 'name' and 'kind' with method describe
# class Food:
#     def __init__(self, name, kind):
#         self.name = name
#         self.kind = kind

#     def describe(self):
#         print("My name is {} and I am a {}".format(self.name, self.kind))


# apple = Food('apple', 'fruit')
# apple.describe()
# lamb = Food('lamb', 'meat')
# lamb.describe()

# Class method

# class Food:
#     name = 'x'
#     kind = 'y'

#     @classmethod
#     def describe(cls):
#         print('My name is {} an Im a {}'.format(cls.name, cls.kind))


# Food.name = "oxtail"
# Food.kind = "meat"

# Food.describe()

# # Static method
# class Food:

#     @staticmethod
#     def describe(name, kind):
#         print("Hi I'm a {} and I am a {}".format(name, kind))


# Food.describe('fig', 'veggie')


class Food:
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

    def __repr__(self):
        return f"Name:{self.name}, kind: {self.kind}"

    def describe(self):
        print("My name is {} and I am a {}".format(self.name, self.kind))


# class Meat(Food):

#     def cook(self):
#         print(f"I like my {self.name} cooked well done")


# class Fruit(Food):

#     def wash(self):
#          print(f"Hi im {self.name}.Please wash {self.kind} off throughly before eating.")


# apple = Fruit('apple', 'fruit')
# print(apple.wash())

# chicken = Meat('chicken', 'pultry')
# print(chicken.cook())


class Meat(Food):
    def __init__(self, name):
        super().__init__(name, "meat")

    def cook(self):
        print(f"I like my {self.name}, type of {self.kind} cooked well done")


class Fruit(Food):
    def __init__(self, name):
        super().__init__(name, "fruit")

    def wash(self):
        print(
            f"Hi im {self.name}.Please wash {self.kind} off throughly before eating.")


apple = Fruit('apple')
# apple.wash()
print(apple)

chicken = Meat('chicken')
# chicken.cook()
print(chicken)
