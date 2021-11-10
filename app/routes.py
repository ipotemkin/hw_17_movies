# TODO: Как загнать в схему db.relationship?

from app import app, db
from flask import jsonify
from app.models import Movie, MovieSchema
# from marshmallow


@app.route('/')
def index():
    return 'Movies API', 200


@app.route('/movies/')
def get_movies():
    # OPTION #1 - my preferable
    # res = [dict(i) for i in db.session.execute("select * from movie")]
    # db.session.close()
    # return jsonify(res)

    # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
    res = Movie.query.all()
    movies_lst = MovieSchema(many=True).dump(res)
    return jsonify(movies_lst)


@app.route('/movies/<int:uid>')
def get_movie_by_id(uid: int):
    # OPTION #1 - my preferable
    # sql = f"select * from movie where id = {uid}"
    # res = dict(db.session.execute(sql).first())
    # db.session.close()
    # return jsonify(res)

    # OPTION #2 - I don't like ORM queries, so it's just to meet the lesson topic
    res = Movie.query.get(uid)
    movies_dict = MovieSchema().dump(res)
    return jsonify(movies_dict)
