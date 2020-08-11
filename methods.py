from datetime import datetime

def Average(nums):
    print("average func")
    print("List length: {}".format(len(nums)))
    print("List type: {}".format(type(nums)))
    if len(nums) > 0:
       return sum(nums) / len(nums)
    else:
        print("empty")



# covert phone number from +1########## to ###-###-####
def phone12to10(num):
  print("Execute: num12to10()")
  print("Inputted Ph Number: ", num)

  # reduce number from 12 to 1 10 digits +16265551212 > 6265551212
  editNum = num[2:]
  print("Edited Number: ", editNum)
  
  # format phone ###-###-####
  numDash = editNum[:3] + "-" + editNum[3:6] + "-" + editNum[6:]
  #print(editNum[:3] + "-" + editNum[3:6] + "-" + editNum[6:])
  print("Number with dashes: ", numDash)

  return numDash