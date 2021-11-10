# TODO: Как загнать в схему db.relationship?
# TODO: Если в PUT ID в URL не равен ID в теле запроса, какую ошибку возвращать?
# TODO: Delete при успехе возвращает 204?

from app import app, db
from flask import jsonify, request
from app.models import Movie, MovieSchema, Director, DirectorSchema, Genre, GenreSchema
from app.errors import NotFoundError, ValidationError, BadRequestError, NoContentError
import time


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


@app.route('/')
def index():
    return 'Movies API', 200


# movies endpoints
@app.route('/movies/')
def get_movies():
    # OPTION #1 - my preferable
    t0 = time.perf_counter()
    sql = "select * from movie"
    sql_where = []
    if director_id := request.args.get('director_id'):
        sql_where.append(f"director_id = '{director_id}'")
    if genre_id := request.args.get('genre_id'):
        sql_where.append(f"genre_id = '{genre_id}'")
    if sql_where:
        sql += " where " + ' and '.join(sql_where)
    if not (res := db.engine.execute(sql).fetchall()):
        raise NotFoundError
    elapsed = time.perf_counter() - t0
    print("[%0.8fs]" % elapsed)
    return jsonify([dict(i) for i in res])

    # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
    # director_id = request.args.get('director_id')
    # genre_id = request.args.get('genre_id')
    # if director_id and genre_id:
    #     res = Movie.query.where(Movie.director_id == director_id).where(Movie.genre_id == genre_id).all()
    # elif director_id:
    #     res = Movie.query.where(Movie.director_id == director_id).all()
    # elif genre_id:
    #     res = Movie.query.where(Movie.genre_id == genre_id).all()
    # else:
    #     res = Movie.query.all()
    # if not res:
    #     raise NotFoundError
    # return jsonify(MovieSchema(many=True).dump(res))


@app.route('/movies1/')
def get_movies1():
    # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
    t0 = time.perf_counter()
    director_id = request.args.get('director_id')
    genre_id = request.args.get('genre_id')
    if director_id and genre_id:
        res = Movie.query.where(Movie.director_id == director_id).where(Movie.genre_id == genre_id).all()
    elif director_id:
        res = Movie.query.where(Movie.director_id == director_id).all()
    elif genre_id:
        res = Movie.query.where(Movie.genre_id == genre_id).all()
    else:
        res = Movie.query.all()
    if not res:
        raise NotFoundError
    elapsed = time.perf_counter() - t0
    print("[%0.8fs]" % elapsed)
    return jsonify(MovieSchema(many=True).dump(res))


@app.route('/movies/<int:uid>')
def get_movie_by_id(uid: int):
    # OPTION #1 - my preferable
    # sql = f"select * from movie where id = {uid}"
    # if not (res := db.engine.execute(sql).first()):
    #     raise NotFoundError
    # return jsonify(dict(res))

    # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
    if not (res := Movie.query.get(uid)):
        raise NotFoundError
    return jsonify(MovieSchema().dump(res))


@app.route('/movies/count/')
def get_movies_count():
    return jsonify(Movie.query.count())


# directors endpoints
@app.route('/directors/')
def get_directors():
    # OPTION #1 - my preferable
    # sql = "select * from director"
    # if not (res := db.engine.execute(sql).fetchall()):
    #     raise NotFoundError
    # return jsonify([dict(i) for i in res])

    # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
    if not (res := Director.query.all()):
        raise NotFoundError
    return jsonify(DirectorSchema(many=True).dump(res))


@app.route('/directors/<int:uid>')
def get_director_by_id(uid: int):
    # OPTION #1 - my preferable
    # sql = f"select * from movie where id = {uid}"
    # if not (res := db.engine.execute(sql).first()):
    #     raise NotFoundError
    # return jsonify(dict(res))

    # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
    if not (res := Director.query.get(uid)):
        raise NotFoundError
    return jsonify(DirectorSchema().dump(res))


@app.route('/directors/', methods=['POST'])
def add_director():
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


@app.route('/directors/<int:uid>', methods=['PUT'])
def update_director(uid: int):
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


@app.route('/directors/<int:uid>', methods=['DELETE'])
def delete_director(uid: int):
    if not (director := Director.query.get(uid)):
        raise NotFoundError
    try:
        db.session.delete(director)
        db.session.commit()
    except Exception:
        raise BadRequestError
    return f"deleted /directors/{director.id}", 200  # исправить на 204?


# genres endpoints
@app.route('/genres/')
def get_genres():
    # OPTION #1 - my preferable
    # sql = "select * from genre"
    # if not (res := db.engine.execute(sql).fetchall()):
    #     raise NotFoundError
    # return jsonify([dict(i) for i in res])

    # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
    if not (res := Genre.query.all()):
        raise NotFoundError
    return jsonify(GenreSchema(many=True).dump(res))


@app.route('/genres/<int:uid>')
def get_genre_by_id(uid: int):
    # OPTION #1 - my preferable
    # sql = f"select * from movie where id = {uid}"
    # if not (res := db.engine.execute(sql).first()):
    #     raise NotFoundError
    # return jsonify(dict(res))

    # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
    if not (res := Genre.query.get(uid)):
        raise NotFoundError
    return jsonify(GenreSchema().dump(res))


@app.route('/genres/', methods=['POST'])
def add_genre():
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


@app.route('/genres/<int:uid>', methods=['PUT'])
def update_genre(uid: int):
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


@app.route('/genres/<int:uid>', methods=['DELETE'])
def delete_genre(uid: int):
    if not (genre := Genre.query.get(uid)):
        raise NotFoundError
    try:
        db.session.delete(genre)
        db.session.commit()
    except Exception:
        raise BadRequestError
    return f"deleted /genres/{genre.id}", 200  # исправить на 204?
