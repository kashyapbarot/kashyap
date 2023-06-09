def scooby_bite(food_items):
    for item in food_items:
        if food_items.count(item) < 3:
            return True
    return False


food_items_1 = ["Pedigree", "Kitkat", "Kitkat", "chocolate", "chocolate",
                "chocolate", "Carrot"]
food_items_2 = ["Pedigree", "Pedigree", "Pedigree", "Horlicks", "Horlicks",
                "Horlicks"]

result = scooby_bite(food_items_1)
if result:
    print("Scooby will bite")
else:
    print("Scooby will not byte")

####################################
num_food_items = int(input("Enter the number of food items: "))

if num_food_items >= 3:
    print("Scooby is happy and will not bite!")
else:
    print("Scooby is not happy and may bite. Give him at least 3 food items.")
