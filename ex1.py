age = int (input("votre Age : "))
if age <= 12:
    print("vous etes mineur -Enfant-")
elif age <= 17:
    print("vous etes mineur -Adolescent-")
elif age <= 64:
    print("vous etes majeur -Adult-")
else:
    print("vous etes Senior -Senior-")