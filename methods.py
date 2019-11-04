from datetime import datetime

def Average(nums):
    print("average func")
    print("List length: {}".format(len(nums)))
    print("List type: {}".format(type(nums)))
    if len(nums) > 0:
       return sum(nums) / len(nums)
    else:
        print("empty")



