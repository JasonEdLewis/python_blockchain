import random as ran
import datetime as dt


def get_ran_num_1_10():
    return ran.randrange(10)


def get_ran_num_range(a, b):
    return ran.randint(a, b)


def current_date_time():
    return dt.datetime.now().time()


def random_num_time():
    print(str(get_ran_num_range(1, 7))+str(current_date_time()))


# random_num_time()

print(get_ran_num_1_10())
