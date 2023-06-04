from config import db
from flask import abort, session
from models import Recipe, Ingredient,recipes_schema,recipe_schema, RecipeSchema

#####
def create_recipe(recipe):

    name = recipe.get("name")
    ingredients = recipe.get("ingredients")
    ingredients_list = []

    # check if recipe with same name already exists
    existing_recipe = Recipe.query.filter_by(name=name).first()
    if existing_recipe is not None:
        abort(406, f"Recipe {name} already exists")
    
    # add ingredients to recipe
    for ingredient_data in ingredients:
        ingredient_name = ingredient_data.get("name")
        #check if the ingredient exist in the data base
        existing_ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if existing_ingredient is not None:
            ingredients_list.append(existing_ingredient)
        else:
            abort(404, f"Ingredient {ingredient_name} not found, you should created first !")
    
    # create new recipe
    new_recipe = Recipe(
        name=name,
        cookTime=recipe.get("cookTime"),
        serving=recipe.get("serving"),
        preparation=recipe.get("preparation"),
        ingredients = ingredients_list
    )
    

    # save recipe to database
    db.session.add(new_recipe)
    db.session.commit()
    
    return recipe_schema.dump(new_recipe), 201

#as user :list all recipes
def list_all_recipes():

    if 'name' in session:
        recipes = Recipe.query.all()
        return recipes_schema.dump(recipes)
    else:
        abort(401, f"User Unauthorized")

#list recipes with a particular ingredient
def filter_recipe(ingredient_name):

    if 'name' in session:
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if ingredient :
            
                recipes = ingredient.recipe
                recipe_schema = RecipeSchema(many=True)
                return recipe_schema .dump(recipes)
        else:

            abort (404, f"Ingredient {ingredient_name} not found")
    else:
        abort(401, f"User Unauthorized")