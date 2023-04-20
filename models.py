from marshmallow_sqlalchemy import fields
from config import db, ma, bcrypt
from datetime import datetime




recipe_ingredients = db.Table('recipe_ingredients',
                    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
                    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
                    )

recipe_user = db.Table('recipe_user',
                    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
                    db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
                    )


class Ingredient(db.Model):

    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), unique=True)

   

    
    
    def __repr__(self):
        return '<Ingredient %s>' % self.name
  

class IngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Ingredient
        load_instance = True
        sqla_session = db.session
        include_relationships = True

class Recipe(db.Model):
    __tablename__ = 'recipe'

    
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), unique=True)

    ingredients = db.relationship('Ingredient', secondary = recipe_ingredients, backref='recipe')

    cookTime = db.Column(db.String(50))

    serving = db.Column(db.Integer)

    preparation = db.Column(db.Text)

    def __repr__(self):
        return '<Recipe %s>' % self.name
   


class RecipeSchema(ma.SQLAlchemyAutoSchema):

    
    class Meta: 
        model = Recipe
        load_instance = True
        sqla_session = db.session
        include_relationships = True
    ingredients = ma.Nested(IngredientSchema, many=True)

    


# User model

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    favoriteRecipes =  db.relationship('Recipe', secondary = recipe_user, backref='users')
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, name, password,favoriteRecipes=[], is_admin=False):
        self.name = name
        self.password = bcrypt.generate_password_hash(password)
        self.favoriteRecipes = favoriteRecipes
        self.is_admin = is_admin

    def __repr__(self):
        return f"<name {self.name}>"

class UserSchema(ma.SQLAlchemyAutoSchema):

    
    class Meta: 
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True
    favoriteRecipes = ma.Nested(RecipeSchema, many=True)
       

ingredient_schema = IngredientSchema()
recipe_schema = RecipeSchema()
ingredients_schema = IngredientSchema(many=True)
recipes_schema = RecipeSchema(many=True)   
user_schema = UserSchema()


    
    

