# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    trailer = fields.Str()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class DirectorSchema(Schema):
    id =fields.Int()
    name = fields.Str()

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class GenreSchema(Schema):
    id =fields.Int()
    name = fields.Str()

movie_schema=MovieSchema()
movies_schema=MovieSchema(many=True)

genre_schema=GenreSchema()

director_schema=DirectorSchema()


api = Api(app)

movie_ns = api.namespace('movies')
director_ns=api.namespace('director')
genre_ns=api.namespace('genre')

@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        res = Movie.query
        if director_id is not None:
            res = res.filter(Movie.director_id == director_id)
        if genre_id is not None:
            res = res.filter(Movie.genre_id == genre_id)
        if genre_id is not None and director_id is not None:
            res = res.filter(Movie.genre_id == genre_id, Movie.director_id == director_id)

        result = res.all()
        return movies_schema.dump(result)

    def post(self):
        r_json = request.json
        add_movie = Movie(**r_json)
        with db.session.begin():
            db.session.add(add_movie)
        return  "", 201

@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid):
        movie=Movie.query.get(uid)
        if not movie:
            return "но ничего страшного", 404
        return movie_schema.dump(movie)

    def delete(self, uid):
        movie = Movie.query.get(uid)
        if not movie:
            return "но ничего страшного", 404
        else:
            db.session.delete(movie)
            db.session.commit()
            return "", 204

################# директор
@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors=Director.query.all()

        return director_schema.dump(all_directors, many=True), 200

    def post(self):
        r_director_json = request.json
        new_director = Movie(**r_director_json)
        with db.session.begin():
            db.session.add(new_director)
        return  "", 201

@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    def get(self, uid):
        director=Director.query.get(uid)
        if not director:
            return "но ничего страшного", 404
        return director_schema.dump(director), 200

    def delete(self, uid):
        director = Director.query.get(uid)
        if not director:
            return "но ничего страшного", 404
        else:
            db.session.delete(director)
            db.session.commit()
            return "", 204
    def put(self, uid):
        director = Director.query.get(uid)
        reg_new_json=request.json
        director.name = reg_new_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "новый директор зареген", 204

    def patch(self, uid):
        director = Director.query.get(uid)
        reg_new_json=request.json
        if "name" in reg_new_json:
            director.name = reg_new_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "частичное изм. директора", 204

################# жанры
@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genre=Genre.query.all()

        return genre_schema.dump(all_genre, many=True), 200

    def post(self):
        r_genre_json = request.json
        new_genre = Movie(**r_genre_json)
        with db.session.begin():
            db.session.add(new_genre)
        return  "", 201

@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    def get(self, uid):
        genre=Genre.query.get(uid)
        if not genre:
            return "но ничего страшного", 404
        return genre_schema.dump(genre), 200

    def delete(self, uid):
        genre = Genre.query.get(uid)
        if not genre:
            return "но ничего страшного", 404
        else:
            db.session.delete(genre)
            db.session.commit()
            return "", 204
    def put(self, uid):
        genre = Genre.query.get(uid)
        reg_new_json=request.json
        genre.name = reg_new_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "новый жанр зареген", 204

    def patch(self, uid):
        genre = Director.query.get(uid)
        reg_new_json=request.json
        if "name" in reg_new_json:
            genre.name = reg_new_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "частичное изм. жанра", 204

if __name__ == '__main__':
    app.run(debug=True)
