"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, FavoritePeople, FavoritePlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#GET ENDPOINTS
@app.route("/people", methods=["GET"])
def get_characters():
    people =People.query.all()
    people = list(map(lambda people: people.serialize(), people))
    return jsonify(people), 200

@app.route("/people/<int:people_id>", methods=["GET"])
def get_character_by_id(people_id):
    people = People.query.get(people_id)
    return jsonify(people.serialize()), 200

@app.route("/planets", methods=["GET"])
def get_planets():
    planets =Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200

@app.route("/planet/<int:planet_id>", methods=["GET"])
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id)
    return jsonify(planet.serialize()), 200

@app.route("/users", methods=["GET"])
def get_users():
    users =User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
     favorites = User.query.all()
     favorites= list(map(lambda favorite: favorite.serialize_with_favorites(), favorites))
     return jsonify(favorites), 200


#POST AND DELETE ENDPOINTS
@app.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])    
def add_delete_favorite_planet(planet_id):
    if request.method == 'POST':
        users_id = 1

        favoriteplanet = FavoritePlanet()
        favoriteplanet.users_id = users_id
        favoriteplanet.planet_id = planet_id

        favoriteplanet.save()

        return jsonify(favoriteplanet.serialize()), 200
    
    if request.method == 'DELETE':
        favoriteplanet = FavoritePlanet.query.filter_by(users_id=1,planet_id=planet_id).first()

        favoriteplanet.delete()

    return jsonify({"msg":"deleted"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST', 'DELETE'])    
def add_delete_favorite_people(people_id):
    if request.method == 'POST':
        user_id = 1

        favoritepeople = FavoritePeople()
        favoritepeople.user_id = user_id
        favoritepeople.people_id = people_id

        favoritepeople.save()

        return jsonify(favoritepeople.serialize()), 200 

    if request.method == 'DELETE':
        favoritepeople = FavoritePeople.query.filter_by(user_id=1,people_id=people_id).first()

        favoritepeople.delete()

    return jsonify({"msg":"deleted"}), 200







# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
