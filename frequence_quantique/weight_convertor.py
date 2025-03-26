weight_input = input("Weight? ")
weight_units = input("In (K)gs or (L)bs ? ").lower()

if weight_units == "l":
    print("Your weight is " + str(float(weight_input) * 0.45) + " Kgs")
elif weight_units =="k":
    print("Your weight is " + str(float(weight_input) / 0.45) + " Lbs")
else:
    print("Invalid answer")  #error management


class Rectangle:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def __str__(self):
        return f'Rectangle({self.height}, {self.width})'

    def __eq__(self, other):
        """ Vérification de l'égalité"""
        return self.height * self.width == other.height * other.width

    def __lt__(self, other):
        """ Vérifie si le rectangle est plus petit que l'autre """
        return self.height * self.width < other.height * other.width

    def __gt__(self, other):
        """ Vérifie si le rectangle est plus grand que l'autre """
        return self.height * self.width > other.height * other.width

    def __del__(self):
        self.height = 0
        self.width = 0

rectangle = Rectangle(10, 20)
rectangle2 = Rectangle(20,30)
print(rectangle < rectangle2)
