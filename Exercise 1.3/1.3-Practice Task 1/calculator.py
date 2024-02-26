a = int(input("Enter a number: "))
b = int(input("Enter another number: "))
operator = input("Enter + or -: ")

if operator == "+":
    print("The sum of these numbers is", str(a+b))
elif operator == "-":
    print("The difference of these numbers is", str(a-b))
else:
    print("Unknown operator")

