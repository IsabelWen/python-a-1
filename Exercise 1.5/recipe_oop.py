class Recipe:
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = int(0)
        self.difficulty = ""

    # Calculating the difficulty level of the recipe
    def calculate_difficulty(self, cooking_time, ingredients):
        ingredients_len = len(ingredients)

        if cooking_time < 10 and ingredients_len < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and ingredients_len > 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and ingredients_len < 4:
            difficulty = "Intermediate"
        elif cooking_time >= 10 and ingredients_len > 4:
            difficulty = "Hard"
        else:
            print("Not able to calculate difficulty")
        
        return difficulty

    # Getter method for name
    def get_name(self):
        return self.name

    # Getter method for cooking time
    def get_cooking_time(self):
        return self.cooking_time
    
    # Getter method for ingredients
    def get_ingredients(self):
        return self.ingredients
    
    # Getter method for difficulty
    def get_difficulty(self):
        if not self.difficulty:
            self.difficulty = self.calculate_difficulty(self.cooking_time, self.ingredients)
        return self.difficulty
    
    # Setter method for name
    def set_name(self, name):
        self.name = name 
    
    # Setter method for cooking_time
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    # Method to add ingredients
    def add_ingredients(self, items):
        self.ingredients.extend(items)
        self.update_all_ingredients()

    # Method for updating the all ingreidents list
    def update_all_ingredients(self):
        all_ingredients = []
        for ingredient in self.ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    # Method to check if an ingredient is in the recipe
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients
        
    # Method to print recipe
    def view_recipe(self):
        print("\n Recipe:", self.name)
        print("------------------------")
        print("Cooking time (min): " + str(self.cooking_time) + "\n" +  "Diffulty: " + self.get_difficulty() + "\n" + "Ingredients:")
        for ingredient in self.ingredients:
            print(ingredient)
    
# Method to find recipes that contain a specific ingredient
def recipe_search(data, search_term):
    found = False
    print("\nRecipes found with the ingredient:", search_term)
    print("---------------------------------------------")
    for recipe in data:
        if recipe.search_ingredient(search_term):
            recipe.view_recipe()
            found = True
    if not found:
        print("Coundn't find", search_term)
        
# Main Code
# Tea Recipe
tea = Recipe("Tea")
tea.add_ingredients(["Tea Leaves", "Sugar", "Water"])
tea.set_cooking_time(5)

# Coffee Recipe
coffee = Recipe("Coffee")
coffee.add_ingredients(["Coffee Powder", "Sugar", "Water"])
coffee.set_cooking_time(5)

# Cake Recipe
cake = Recipe("Cake")
cake.add_ingredients(["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"])
cake.set_cooking_time(50)

# Banana Smoothie
banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients(["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"])
banana_smoothie.set_cooking_time(5)

# Recipe List
recipes_list = [tea, coffee, cake, banana_smoothie]

# Print all recipes
for recipe in recipes_list:
    recipe.view_recipe()

# Search recipes ingredients
recipe_search(recipes_list, "Water")
recipe_search(recipes_list, "Sugar")
recipe_search(recipes_list, "Bananas")
        
