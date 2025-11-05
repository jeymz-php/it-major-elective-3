hf = int(input("Enter height in feet: "))
hi = int(input("Enter height in inches: "))
wkg = int(input("Enter weight in kilogram: "))

hm = ((hf*30.48) + (hi*2.54))/100
bmi = wkg/(hm*hm)

print(f"The body mass index is {round(bmi,2)}")