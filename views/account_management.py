from models import  User,user_schema
from config import db, bcrypt
from flask import abort,session



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