from app import app, db
from app.models import Movie, Director, Genre


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Movie': Movie, 'Director': Director, 'Genre': Genre}


if __name__ == '__main__':
    app.run(debug=True)
