from app import app, db #, db
from models import Bird # db,

# db.init_app(app) # This is new import of db 
# Avoid creating a new SQLAlchemy() instance in seed.py.
# import the db and app from app.py

with app.app_context():

    print('Deleting existing birds...')
    Bird.query.delete()

    print('Creating bird objects...')
    chickadee = Bird(
        name='Black-Capped Chickadee',
        species='Poecile Atricapillus',
        image='/images/black-capped-chickadee.jpeg'
    )
    grackle = Bird(
        name='Grackle',
        species='Quiscalus Quiscula',
        image='/images/grackle.jpeg'
    )
    starling = Bird(
        name='Common Starling',
        species='Sturnus Vulgaris',
        image='/images/starling.jpeg'
    )
    dove = Bird(
        name='Mourning Dove',
        species='Zenaida Macroura',
        image='/images/dove.jpeg'
    )

    print('Adding bird objects to transaction...')
    db.session.add_all([chickadee, grackle, starling, dove])
    print('Committing transaction...')
    db.session.commit()
    print('Complete.')
