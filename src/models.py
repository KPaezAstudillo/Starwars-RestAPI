from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
   

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

class Character(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False)
    mass = db.Column(db.Integer, unique=False)
    hair_color = db.Column(db.String(120), unique=False)
    eye_color = db.Column(db.String(120), unique=False)

    def __repr__(self):
        return '<Character %r>' % self.character

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

class FavoriteCharacter(db.Model):
    
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'), primary_key=True)

    def __repr__(self):
        return '<FavoriteCharacter %r>' % self.favoritecharacters

    def serialize(self):
        return {
            "users_id": self.users_id,
            "characters_id": self.characters_id,
    
        }

class FavoritePlanet(db.Model):
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), primary_key=True)

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.favoriteplanets

    def serialize(self):
        return {
            "users_id": self.users_id,
            "planets_id": self.planets_id,
    
        }
