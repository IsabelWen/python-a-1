import pickle

# Define a function to take recipes.
def take_recipe():
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time of the recipe in min: "))
    ingredients = input("Enter ingredients (separated by comma): ").split(', ')
    difficulty = calc_difficulty(cooking_time, ingredients)
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty
    }
    return recipe

# Define a function to calculate recipe difficulty.
def calc_difficulty(cooking_time, ingredients):
    ingredients_len = len(ingredients)

    if cooking_time < 10 and ingredients_len < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and ingredients_len >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and ingredients_len < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and ingredients_len >= 4:
        difficulty = "Hard"

    return difficulty

# Main Code
filename = input("Enter the filename for your recipe: ")
try:
    file = open(filename, "rb")
    data = pickle.load(file)
except FileNotFoundError:
    print("File doesn't exist")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
except:
    print("An unexpected error occurred.")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
else:
    file.close()
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

# User input how many recipes they would like to enter
n = int(input("Enter how many recipes you would like to enter: "))

# For-loop that calls the take_recipe() function
for i in range(n):
    recipe = take_recipe()
    recipes_list.append(recipe)
    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

# Gather recipe list and ingredients list in dictionary
data = {
    "recipes_list": recipes_list,
    "all_ingredients": all_ingredients
}
    
# Save data in binary file
with open(filename, "wb") as file:
    pickle.dump(data, file)