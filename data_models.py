from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String, nullable=False)
    date_of_death = db.Column(db.String)

    def __repr__(self):
        return f"Author: {self.name} (*{self.birth_date})"


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    isbn = db.Column(db.String(13))
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    # Define a relationship to Author
    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return f"Book: {self.title} ({self.publication_year})"
