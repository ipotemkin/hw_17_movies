# TODO: Как загнать в схему db.relationship?

from app import app, db
from flask import jsonify, request
from app.models import Movie, MovieSchema
from app.errors import NotFoundError, ValidationError, BadRequestError
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
    # sql = "select * from movie"
    # if director_id := request.args.get('director_id'):
    #     sql += f" where director_id = {director_id}"
    # return jsonify([dict(i) for i in db.engine.execute(sql)])

    # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
    if director_id := request.args.get('director_id'):
        res = Movie.query.where(Movie.director_id == director_id).all()
    else:
        res = Movie.query.all()
    if not res:
        raise NotFoundError
    return jsonify(MovieSchema(many=True).dump(res))


@app.route('/movies/<int:uid>')
def get_movie_by_id(uid: int):
    # OPTION #1 - my preferable
    # sql = f"select * from movie where id = {uid}"
    # return jsonify(dict(db.engine.execute(sql).first()))

    # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
    if not (res := Movie.query.get(uid)):
        raise NotFoundError
    return jsonify(MovieSchema().dump(res))


@app.route('/movies/count/')
def get_movies_count():
    return jsonify(Movie.query.count())
