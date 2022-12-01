from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= user
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorite_people = db.relationship('FavoritePeople')
    favorite_planets = db.relationship('FavoritePlanet')
   

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    def serialize_with_favorites(self):
        favorite_people = [character.serialize() for character in self.favorite_people]
        favorite_planets = [planet.serialize() for planet in self.favorite_planets]
        
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "favorite_people": favorite_people,
            "favorite_planets": favorite_planets
        }

    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class People(db.Model):
    __tablename__ = people
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False)
    mass = db.Column(db.Integer, unique=False)
    hair_color = db.Column(db.String(120), unique=False)
    eye_color = db.Column(db.String(120), unique=False)

    def __repr__(self):
        return '<People %r>' % self.people

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,    
        }

class Planet(db.Model):
    __tablename__ = planet
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    diameter = db.Column(db.Integer)

    def __repr__(self):
        return '<Planet %r>' % self.planet

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
        }

class FavoritePeople(db.Model):
    __tablename__= favoritepeople
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), primary_key=True)
    people_rel = db.relationship('People')
    

    def __repr__(self):
        return '<FavoritePeople %r>' % self.favoritepeople

    def serialize(self):
        return {
            "users_id": self.users_id,
            "people_id": self.people_id,
    
        }

class FavoritePlanet(db.Model):
    __tablename__= favoriteplanet
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), primary_key=True)
    planet_rel = db.relationship('Planet')

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.favoriteplanets

    def serialize(self):
        return {
            "users_id": self.users_id,
            "planets_id": self.planets_id,
    
        }
