from app import app, db, movies_ns, directors_ns, genres_ns
from flask import jsonify, request
from app.models import Movie, MovieSchema, Director, DirectorSchema, Genre, GenreSchema
from app.errors import NotFoundError, ValidationError, BadRequestError, NoContentError
from flask_restx import Resource


# error handlers
@app.errorhandler(404)
@app.errorhandler(NotFoundError)
def on_not_found_error(error):
    return "Not found", 404


@app.errorhandler(ValidationError)
def on_not_validation_error(error):
    return "Validation error", 400


@app.errorhandler(BadRequestError)
def on_bad_request_error(error):
    return "Bad request error", 405


@app.errorhandler(NoContentError)
def on_no_content_error(error):
    return "No Content error", 204


# movies endpoints
# @app.route('/movies/')
@movies_ns.route('/')
class MoviesView(Resource):

    @staticmethod
    def get():
        """
        To get all movies from the database.
        Pagination available with 'page' and 'limit' + 'start' key words.
        Filter available with director_id and gere_id key words.
        """

        start = 0  # default screen - 1
        limit = None  # number of movies on one screen
        args = request.args
        if 'page' in args:
            limit = 5  # default number of movies on one screen
            try:
                page = int(args.get('page'))
            except Exception:
                raise BadRequestError
            start = (page - 1) * limit
        elif 'limit' in args and 'start' in args:
            try:
                limit = int(args.get('limit'))
                start = (int(args.get('start')) - 1) * limit
            except Exception:
                raise BadRequestError

        director_id = args.get('director_id')
        genre_id = args.get('genre_id')
        if director_id and genre_id:
            res = db.session.query(Movie).filter(Movie.director_id == director_id,
                                                 Movie.genre_id == genre_id).limit(limit).offset(start).all()
        elif director_id:
            res = db.session.query(Movie).filter(Movie.director_id == director_id).limit(limit).offset(start).all()
        elif genre_id:
            res = db.session.query(Movie).filter(Movie.genre_id == genre_id).limit(limit).offset(start).all()
        else:
            res = Movie.query.limit(limit).offset(start).all()
        if not res:
            raise NotFoundError
        return jsonify(MovieSchema(many=True).dump(res))


@movies_ns.route('/<int:uid>')
class MovieView(Resource):
    @staticmethod
    def get(uid: int):
        """
        To get a movie by its id.
        """

        # OPTION #1 - my preferable
        # sql = f"select * from movie where id = {uid}"
        # if not (res := db.engine.execute(sql).first()):
        #     raise NotFoundError
        # return jsonify(dict(res))

        # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
        if not (res := Movie.query.get(uid)):
            raise NotFoundError
        return jsonify(MovieSchema().dump(res))


@movies_ns.route('/count/')
class MoviesCountView(Resource):
    @staticmethod
    def get():
        """
        To get the number of movies in the database
        """

        return jsonify(Movie.query.count())


# directors endpoints
@directors_ns.route('/')
class DirectorsView(Resource):
    @staticmethod
    def get():
        """
        To get all directors from the database
        """

        # OPTION #1 - my preferable
        # sql = "select * from director"
        # if not (res := db.engine.execute(sql).fetchall()):
        #     raise NotFoundError
        # return jsonify([dict(i) for i in res])

        # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
        if not (res := Director.query.all()):
            raise NotFoundError
        return jsonify(DirectorSchema(many=True).dump(res))

    @staticmethod
    def post():
        """
        To add a director into the database.
        """

        director_json = request.get_json()
        if not director_json:
            raise BadRequestError
        director = Director(**director_json)
        try:
            db.session.add(director)
            db.session.commit()
        except Exception:
            raise BadRequestError
        return f"/directors/{director.id}", 201


@directors_ns.route('/<int:uid>')
class DirectorView(Resource):
    @staticmethod
    def get(uid: int):
        """
        To get a director with the given id.
        """

        # OPTION #1 - my preferable
        # sql = f"select * from movie where id = {uid}"
        # if not (res := db.engine.execute(sql).first()):
        #     raise NotFoundError
        # return jsonify(dict(res))

        # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
        if not (res := Director.query.get(uid)):
            raise NotFoundError
        return jsonify(DirectorSchema().dump(res))

    @staticmethod
    def put(uid: int):
        """
        Update a director with the given id in the database
        """

        if not (director_json := request.get_json()):
            raise NoContentError

        if not (director := Director.query.get(uid)):
            raise NotFoundError

        try:
            if director.id != director_json["id"]:
                raise BadRequestError
            director.name = director_json["name"]
            db.session.add(director)
            db.session.commit()
        except Exception:
            raise BadRequestError

        return f"updated /directors/{director.id}", 200

    @staticmethod
    def delete(uid: int):
        """
        To delete a director with the given id
        """

        if not (director := Director.query.get(uid)):
            raise NotFoundError
        try:
            db.session.delete(director)
            db.session.commit()
        except Exception:
            raise BadRequestError
        return "", 204


# genres endpoints
@genres_ns.route('/')
class GenresView(Resource):
    @staticmethod
    def get():
        """
        To get all genres from the database.
        """

        # OPTION #1 - my preferable
        # sql = "select * from genre"
        # if not (res := db.engine.execute(sql).fetchall()):
        #     raise NotFoundError
        # return jsonify([dict(i) for i in res])

        # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
        if not (res := Genre.query.all()):
            raise NotFoundError
        return jsonify(GenreSchema(many=True).dump(res))

    @staticmethod
    def post():
        """
        To add a new genre to the database.
        """

        genre_json = request.get_json()
        if not genre_json:
            raise BadRequestError
        genre = Genre(**genre_json)
        try:
            db.session.add(genre)
            db.session.commit()
        except Exception:
            raise BadRequestError
        return f"/genres/{genre.id}", 201


@genres_ns.route('/<int:uid>')
class GenreView(Resource):
    @staticmethod
    def get(uid: int):
        """
        To get a genre with the given id.
        """

        # OPTION #1 - my preferable
        # sql = f"select * from movie where id = {uid}"
        # if not (res := db.engine.execute(sql).first()):
        #     raise NotFoundError
        # return jsonify(dict(res))

        # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
        if not (res := Genre.query.get(uid)):
            raise NotFoundError
        return jsonify(GenreSchema().dump(res))

    @staticmethod
    def put(uid: int):
        """
        To update a genre with the given id.
        """

        if not (genre_json := request.get_json()):
            raise NoContentError

        if not (genre := Genre.query.get(uid)):
            raise NotFoundError

        try:
            if genre.id != genre_json["id"]:
                raise BadRequestError
            genre.name = genre_json["name"]
            db.session.add(genre)
            db.session.commit()
        except Exception:
            raise BadRequestError

        return f"updated /genres/{genre.id}", 200

    @staticmethod
    def delete(uid: int):
        """
        To delete a genre with the given id.
        """

        if not (genre := Genre.query.get(uid)):
            raise NotFoundError
        try:
            db.session.delete(genre)
            db.session.commit()
        except Exception:
            raise BadRequestError
        return "", 204
