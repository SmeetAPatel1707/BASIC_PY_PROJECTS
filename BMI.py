# Create a command-line BMI Calculator in python. Prompt users for their weight(kg) and height(m), Calculate the BMI and classify it into caategories (underweight, normal, overweight) based on predefined ranges. Display the BMI result and category to the user.

W = float(input("Enter your weight in Kilograms :"))
H = float(input("Enter your height in Foot :"))

Hm = (H*0.3048)
BMI = W/(Hm**2)
print("Your Body Mass Index(BMI) is :",BMI)

if BMI>0:
    if BMI<18.5:
        print("You are Underweight")
    if BMI>=18.5 and BMI<=24.9:
        print("You are Normal")
    if BMI>=25.0 and BMI<=29.9:
        print("You are Overweight")
    if BMI>=30.0 and BMI<=34.9:
        print("You are Obese")
    if BMI>35.0:
        print("You are Extremly Obese")
