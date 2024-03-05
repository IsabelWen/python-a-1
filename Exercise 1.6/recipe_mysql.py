import mysql.connector
import sys

# Initialize connection object 
conn = mysql.connector.connect(
    host = "localhost",
    user = "cf-python",
    passwd = "password"
)

# Initialize cursor object 
cursor = conn.cursor()

# Create database task_database
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

# Access database
cursor.execute("USE task_database")

# Create table Recipes
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes (
               id           INT PRIMARY KEY AUTO_INCREMENT,
               name         VARCHAR(50),
               ingredients  VARCHAR(255),
               cooking_time INT,
               difficulty   VARCHAR(20)
)''')

# Loop to run the main menu
def main_menu(conn, cursor):
    choice = ""
    while(choice != 'quit'):
        print("Main Menu")
        print("----------")
        print("What would you like to do? Pick a choice!")
        print("1. Create a new recipe")
        print("2. Search for recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("Type 'quit' to exist the program.")
        choice = (input("\nYour choice (type in a number or 'quit'): "))

        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "quit":
            print("Exiting the program.\n")
            conn.close()
            break
        else:
            print("Please write the number of one of the choices.\n")
    

# Definition for operation: Create new recipe
def create_recipe(conn, cursor):
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time of the recipe in min: "))
    ingredients = input("Enter ingredients (separated by comma): ").split(", ")
    difficulty = calc_difficulty(cooking_time, ingredients)

    ingredients_string = ", ".join(ingredients)

    cursor.execute("INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)", (name, ingredients_string, cooking_time, difficulty))
    conn.commit()
    print("Recipe successfully added.\n")

# Calculate recipe difficulty
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
    else:
        print("Not able to calculate difficulty of this recipe.")

    return difficulty

# Definition for operation: Search for recipe
def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()
    all_ingredients = []
    if len(results) > 0:
        for result in results:
            ingredients = result[0].split(", ")
            for ingredient in ingredients:
                if ingredient not in all_ingredients:
                    all_ingredients.append(ingredient)
        for position, ingredient in enumerate(all_ingredients):
            print(f"Ingredient {position}: {ingredient}")
    else:
        print("There are no recipes yet.\n")
        return

    try:
        ingredient_index = input("Enter the the numbers of the ingredient you would like to search for (comma-separated): ").split(", ")
        search_ingredient = []
        for index in ingredient_index:
            ingredient_index = int(index.strip())
            if ingredient_index < len(all_ingredients):
                search_ingredient.append(all_ingredients[ingredient_index])
            else:
                print("The number you chose is not in the list.\n")
    except ValueError:
        print("One or more of your inputs aren't numbers.\n")
    except:
        print("An unexpected error occurred.\n")
        sys.exit(1)
    else:
        for ingredient in search_ingredient:
            cursor.execute("SELECT * FROM Recipes WHERE ingredients LIKE %s", ("%" + ingredient + "%",))
            result = cursor.fetchall()
            print("\nRecipe with ingredient", ingredient)
            print("=======================================")
            for row in result:
                print("\nRecipe:", row[1])
                print("----------------------------")
                print("Ingredients:", row[2])
                print("Cooking Time:", row[3])
                print("Diffculty:", row[4] + "\n")



# Definition for operation: Update existing recipe
def update_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()
    if len(results) > 0:
        for row in results:
            print("ID: ", row[0])
            print("Name: ", row[1])
            print("Ingredients: ", row[2])
            print("Cooking Time: ", row[3])
            print("Difficulty:", row[4] + "\n")
    else:
        print("There are no recipes yet.\n")
        return
    
    # Enter what to update
    try:
        recipe_id = int(input("Enter the the id of the recipe you would like to update: "))
        column = input("Enter the the name of the column you would like to update (name, cooking_time or ingredients): ")
        if column != "cooking_time" and column != "name" and column != "ingredients":
            print("You need to write 'cooking_time', 'name', or 'ingredients.\n")
            return
        update_value = input(f"Enter the new value for {column}: ")
    except ValueError:
        print("One or more of your inputs aren't in the right format.\n")
    except:
        print("An unexpected error occurred.\n")
        sys.exit(1)

    # Update accordingly
    try:
        cursor.execute(f"UPDATE Recipes SET {column} = %s WHERE id = %s", (update_value, recipe_id))
        if column == "cooking_time":
            cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id,))
            result = cursor.fetchone()
            ingredients = result[0]
            cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (calc_difficulty(int(update_value), ingredients.split(", ")), recipe_id))
        elif column == "ingredients":
            cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (recipe_id,))
            result = cursor.fetchone()
            cooking_time = result[0]
            cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (calc_difficulty(cooking_time, update_value.split(", ")), recipe_id))
        conn.commit()
        print("Recipe successfully updated.\n")
    except:
        print("Unexpected error\n")
        sys.exit(1)

# Definition for operation: Delete a recipe
def  delete_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()
    if len(results) > 0:
        for row in results:
            print("ID: ", row[0])
            print("Name: ", row[1])
            print("Ingredients: ", row[2])
            print("Cooking Time: ", row[3])
            print("Difficulty:", row[4] + "\n")
    else:
        print("There are no recipes yet.\n")
        return
    
    try:
        recipe_id = int(input("Enter the the id of the recipe you would like to delete: "))
    except ValueError:
        print("One or more of your inputs aren't numbers.\n")
    except:
        print("An unexpected error occurred.\n")
        sys.exit(1)
    else:
        cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))

        conn.commit()
        print("Recipe successfully deleted.\n")

main_menu(conn, cursor)