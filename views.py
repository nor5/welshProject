from models import Recipe, Ingredient, User, IngredientSchema, RecipeSchema,user_schema, ingredient_schema,ingredients_schema , recipes_schema,recipe_schema
from config import db, bcrypt
from flask import abort, make_response, session, request


##Ingredient 
def read_all_ingredients():

    ingredients = Ingredient.query.all()
    return ingredients_schema.dump(ingredients)


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

    
##Recipe
def read_all_recipes():

    recipes = Recipe.query.all()
    return recipes_schema.dump(recipes)

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


###Create User
def create_user(user):

    if 'name' in session:
        username = session['name']
        admin = User.query.filter_by(name=username).first()
        if admin.is_admin:
            name = user.get("name")
            password = user.get("password")

     # check if admin with same name already exists
            existing_user = User.query.filter_by(name=name).first()
            if existing_user is  None:
                 new_user = User(name=name, password=password, is_admin=False)
                 db.session.add(new_user)
                 db.session.commit()
                 return user_schema.dump(new_user), 201
      
            else:
                abort(409, f"user {name} already exists")
        else:
            abort(406, f"user {username} must be an admin to create a user")

        
    else:
        abort(401, f"User Unauthorized")
        

###login
def login(user):

    name = user.get("name")
    password = user.get("password")
    user_exist = User.query.filter_by(name=name).first()
    if user_exist and bcrypt.check_password_hash( user_exist.password ,password ):
            session['name'] = user_exist.name
            return user_schema.dump(user_exist), 201
    else:
        abort(403, "Invalid name and/or password.")
            

##logout User
def logout():

    if 'name' in session:
        session.pop('name', None)
    
# as user :list ingredients 
def list_all_ingredients():

    if 'name' in session:
        return read_all_ingredients()
    else:
        abort(401, f"User Unauthorized")
 

#list all recipes
def list_all_recipes():

    if 'name' in session:
        return read_all_recipes()
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

    