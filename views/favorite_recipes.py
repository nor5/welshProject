from config import db
from flask import abort, session, request
from models import Recipe,  User,user_schema, recipes_schema

# flag favorite recipe  
def favorite_recipes(recipes):
    if 'name' in session:
        username = session['name']
        recipes = recipes.get("recipes")
        current_User = User.query.filter_by(name=username).first()
        
        for recipe in recipes:
            name = recipe.get("name")
            existing_recipe = Recipe.query.filter_by(name=name).first()
            if existing_recipe:
                current_User.favoriteRecipes.append(existing_recipe)
           
            else:
                abort(404, f"Recipe {name} not found")
    
    # save favorite recipe to database
        db.session.commit()
    
        return user_schema.dump(current_User), 201
    else:
        abort(401, f"User Unauthorized")


# Unflag favorite recipe  
def delete_favorite():

    if 'name' in session:
        username = session['name']
        recipes = request.json["recipes"]
        current_User = User.query.filter_by(name=username).first()
        
        for recipe in recipes:
            name = recipe.get("name")
            existing_recipe = Recipe.query.filter_by(name=name).first()
            if existing_recipe and existing_recipe in current_User.favoriteRecipes:
                current_User.favoriteRecipes.remove(existing_recipe)
           
            else:
                abort(404, f"Recipe {name} not found")
    
    # save the updated list of favorite recipe to database
        db.session.commit()
        return user_schema.dump(current_User), 201
    else:
        abort(401, f"User Unauthorized")

#list favorites recipes
def list_favorite_recipes():

    if 'name' in session:
        username = session['name']
        current_User = User.query.filter_by(name=username).first() 
        favorite_recipes = current_User.favoriteRecipes
        if favorite_recipes:
            return recipes_schema.dump(favorite_recipes)
        else:
            return {'message': 'No favorite recipes found'}

    else:
        abort(401, "User Unauthorized")

    