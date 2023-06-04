import getpass
import unittest

from flask.cli import FlaskGroup
from app import db
import app
from models import User

#create command-line interfaces
cli = FlaskGroup(app)



@cli.command("test")
def test():
    """Runs the unit tests without coverage."""
    #searches for test modules and test cases in the "tests" directory.
    tests = unittest.TestLoader().discover("tests")
    
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@cli.command("create_admin")
def create_admin():
    #Create a admin user.
    name = input("Enter your name: ")
    password = getpass.getpass("Enter password: ")
    
           
    try:
       # check if admin with same name already exists
       existing_admin = User.query.filter_by(name=name).first()
       if existing_admin is  None:
           new_admin = User(name=name, password=password, is_admin=True)
           db.session.add(new_admin)
           db.session.commit()
           print(f"Admin with name {name} created successfully!")
      
       else:
            print(f"admin {name} already exists")
    except Exception:
        print("Couldn't create admin user.")
   
if __name__ == "__main__":
    cli()
