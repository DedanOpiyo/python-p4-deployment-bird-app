import os

# Generate the environment variables (we have some in .env file)
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify, request, make_response, render_template
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Bird

# Following the production version of react # npm run build --prefix client # additional parameters apart from __name__
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build'
)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI') # Importing any of our .env variables with os.environ.get().
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# catch-all - for any route that doesn't match those already defined on the server. 
# when Flask receives a request,it will render the index.html that was generated to run the client application. 
# These follows the production version of react(see how we instantiate Flask above app = Flask ...)
@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")

api = Api(app)

@app.route('/')
def index():
    return "Welcome to the Bird API. Try /birds"

class Birds(Resource):

    def get(self):
        birds = [bird.to_dict() for bird in Bird.query.all()]
        return make_response(jsonify(birds), 200)

    def post(self):

        data = request.get_json()

        new_bird = Bird(
            name=data['name'],
            species=data['species'],
            image=data['image'],
        )

        db.session.add(new_bird)
        db.session.commit()

        return make_response(new_bird.to_dict(), 201)

api.add_resource(Birds, '/birds')

class BirdByID(Resource):
    
    def get(self, id):
        bird = Bird.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(bird), 200)

    def patch(self, id):

        data = request.get_json()

        bird = Bird.query.filter_by(id=id).first()

        for attr in data:
            setattr(bird, attr, data[attr])

        db.session.add(bird)
        db.session.commit()

        return make_response(bird.to_dict(), 200)

    def delete(self, id):

        bird = Bird.query.filter_by(id=id).first()
        db.session.delete(bird)
        db.session.commit()

        return make_response('', 204)

api.add_resource(BirdByID, '/birds/<int:id>')