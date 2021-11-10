# TODO: Как загнать в схему db.relationship?

from app import app, db
from flask import jsonify, request
from app.models import Movie, MovieSchema
from app.errors import NotFoundError, ValidationError, BadRequestError
import time
# from marshmallow


@app.errorhandler(404)
@app.errorhandler(NotFoundError)
def on_not_found_error(error):
    return "Not found", 404


@app.errorhandler(ValidationError)
def on_not_validation_error(error):
    return "Validation error", 400


@app.errorhandler(BadRequestError)
def on_not_validation_error(error):
    return "Bad request error", 405


@app.route('/')
def index():
    return 'Movies API', 200


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
