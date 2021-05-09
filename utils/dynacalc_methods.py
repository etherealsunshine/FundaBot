def add(nums):
    sum = 0
    for i in nums:
        sum += i
    return sum

def subtract(nums):
    diff_num = nums[0]
    for i in range(1, len(nums)):
        diff_num -= nums[i]
    return diff_num

def multiply(nums):
    product = 1
    for i in nums:
        product *= i
    return product

def divide(x, y):
    return x / y

def check_number(input):
    try:
        int(input)
        return True
    except ValueError:
        try:
            float(input)
            return True
        except ValueError:
            return False


def is_zero(input):
    return input == 0