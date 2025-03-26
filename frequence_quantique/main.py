# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

 # String
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print("Hello World")


def input_birthday():
    birth_year = input("What is your birth year ? ")
    age = 2025 - int(birth_year)


def input_name():
    name = input("WHat is your name ? ")
    print("Hello" + name)


def sum_two_numbers():
    first_number = float(input("First number : "))
    second_number = float(input("second number : "))
    numbers_sum = first_number + second_number
    res = "The sum is : " + str(numbers_sum)
    print(res)
    print("sum" in res)  # Check if keyword "sum"  appears in res.

# ARITHMETICS


def arithmetic_operations():
    print(10 / 3)
    print(10 // 3)
    print(10 % 3)
    print(10 ** 3)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sum_two_numbers()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
