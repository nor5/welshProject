from flask import abort,session
from config import db
from models import  Ingredient, ingredient_schema,ingredients_schema 

## create ingredient 
def create_ingredient(ingredient):

    name = ingredient.get("name")
    existing_ingredient = Ingredient.query.filter(Ingredient.name == name).one_or_none()
    #check if the ingredient exist in the data base
    if existing_ingredient is None:
        new_ingredient = ingredient_schema.load(ingredient, session=db.session)
        db.session.add(new_ingredient)
        db.session.commit()
        return ingredient_schema.dump(new_ingredient), 201
    else:
        abort(406, f"The ingredient {name} already exists")


# as user :list ingredients 
def list_all_ingredients():

    if 'name' in session:
        ingredients = Ingredient.query.all()
        return ingredients_schema.dump(ingredients)
    else:
        abort(401, f"User Unauthorized")
 