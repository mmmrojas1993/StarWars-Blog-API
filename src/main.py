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
from models import db, User
from models import Person, Ship, Planet


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

#User

@app.route("/users", methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda ship: ship.to_dict(), users))
    return jsonify(users), 200

@app.route("/users/<int:user_id>/favorites", methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    people = user.get_people()
    planets = user.get_planets()
    ships = user.get_ships()

    return jsonify({
        "people": people,
        "planets": planets,
        "ships": ships
    }), 200

@app.route("/users", methods=['POST'])
def create_user():
    user = User()
    user.email = request.json.get('email')
    user.password = request.json.get('password')
    user.save()
    
    return jsonify(user.to_dict()), 201

@app.route("/users/<int:user_id>/favorites_planets", methods=['POST'])
def create_favorite_planet(user_id):
    favorite_planet = FavoritePlanet()
    favorite_planet.user_id = user_id
    favorite_planet.planet_id = request.json.get('planet_id')
    favorite_planet.save()
    
    return jsonify(favorite_planet.to_dict()), 201

@app.route("/users/<int:user_id>/favorites_ships", methods=['POST'])
def create_favorite_ship(user_id):
    favorite_ship = FavoriteShip()
    favorite_ship.user_id = user_id
    favorite_ship.ship_id = request.json.get('ship_id')
    favorite_ship.save()
    
    return jsonify(favorite_ship.to_dict()), 201

@app.route("/users/<int:user_id>/favorites_people/<int:favorite_person_id>", methods=['DELETE'])
def delete_favorite_person(user_id, favorite_person_id):
    favorite_person = FavoritePerson.query.get(favorite_person_id)
    favorite_person.delete()

    return jsonify(favorite_person.to_dict()), 201

@app.route("/users/<int:user_id>/favorites_planets/<int:favorite_planet_id>", methods=['DELETE'])
def delete_favorite_planet(user_id, favorite_planet_id):
    favorite_planet = FavoritePlanet.query.get(favorite_planet_id)
    favorite_planet.delete()

    return jsonify(favorite_planet.to_dict()), 201

@app.route("/users/<int:user_id>/favorites_ships/<int:favorite_ship_id>", methods=['DELETE'])
def delete_favorite_ship(user_id, favorite_ship_id):
    favorite_ship = FavoriteShip.query.get(favorite_ship_id)
    favorite_ship.delete()

    return jsonify(favorite_ship.to_dict()), 201

#People

@app.route("/people", methods=['GET'])
def getPeople():
    people = Person.query.all()
    people = list(map(lambda person: person.to_dict(), people))
    return jsonify(people), 200

@app.route("/people/<int:person_id>", methods = ["GET"])
def getPerson(person_id):
    person = Person.query.get(person_id)
    
    if person:
        return jsonify(person.to_dict())

    return jsonify({"message": "Person not found"})

@app.route("/users/<int:user_id>/favorites_people", methods=['POST'])
def create_favorite_person(user_id):
    favorite_person = FavoritePerson()
    favorite_person.user_id = user_id
    favorite_person.person_id = request.json.get('person_id')
    favorite_person.save()
    
    return jsonify(favorite_person.to_dict()), 201

@app.route("/people", methods=['POST'])
def createPerson():
    person = Person()
    person.name = request.json.get('name')
    person.height = request.json.get('height')
    person.mass = request.json.get('mass')
    person.hair_color = request.json.get('hair_color')
    person.skin_color = request.json.get('skin_color')
    person.eye_color = request.json.get('eye_color')
    person.birth_year = request.json.get('birth_year')
    person.gender = request.json.get('gender')
    person.save()
    
    return jsonify(person.to_dict()), 201

#Planets

@app.route("/planets", methods=['GET'])
def getPlanets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.to_dict(), planets))
    return jsonify(planets), 200

@app.route("/planets/<int:planet_id>", methods = ["GET"])
def getPlanet(planet_id):
    planet = Planet.query.get(planet_id)
    
    if planet:
        return jsonify(planet.to_dict())

    return jsonify({"message": "Planet not found"})

@app.route("/planets", methods=['POST'])
def createPlanet():
    planet = Planet()
    planet.name = request.json.get('name')
    planet.rotation_period = request.json.get('rotation_period')
    planet.orbital_period = request.json.get('orbital_period')
    planet.diameter = request.json.get('diameter')
    planet.climate = request.json.get('climate')
    planet.gravity = request.json.get('gravity')
    planet.terrain = request.json.get('terrain')
    planet.surface_water = request.json.get('surface_water')
    planet.population = request.json.get('population')
    planet.save()
    
    return jsonify(planet.to_dict()), 201

# Ships

@app.route("/ships", methods=['GET'])
def getShips():
    ships = Ship.query.all()
    ships = list(map(lambda ship: ship.to_dict(), ships))
    return jsonify(ships), 200

@app.route("/ships/<int:ship_id>", methods = ["GET"])
def getShip(ship_id):
    ship = Ship.query.get(ship_id)
    
    if ship:
        return jsonify(ship.to_dict())

    return jsonify({"message": "Ship not found"})

@app.route("/ships", methods=['POST'])
def createShip():
    ship = Ship()
    ship.name = request.json.get('name')
    ship.model = request.json.get('model')
    ship.manufacturer = request.json.get('manufacturer')
    ship.cost_in_credits = request.json.get('cost_in_credits')
    ship.length = request.json.get('length')
    ship.max_atmosphering_speed = request.json.get('max_atmosphering_speed')
    ship.crew = request.json.get('crew')
    ship.passengers = request.json.get('passengers')
    ship.cargo_capacity = request.json.get('cargo_capacity')
    ship.consumables = request.json.get('consumables')
    ship.hyperdrive_rating = request.json.get('hyperdrive_rating')
    ship.MGLT = request.json.get('MGLT')
    ship.starship_class = request.json.get('starship_class')
    ship.save()
    
    return jsonify(ship.to_dict()), 201
    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)