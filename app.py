from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
import os


# Create an instance of the Flask application after the imports.
app = Flask(__name__)

# Set a secret key for sessions (needed for flash messages)
app.config['SECRET_KEY'] = '6b809f7762e4a672f4d57d951d87c67bff1991ee9eea687d'

# URI (= Uniform Resource Identifier)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data', 'library.db')}"
db.init_app(app)

# Create Tables:
# with app.app_context():
#     db.create_all()



@app.route('/')
def index():

    # Get the sort option from the query parameters
    sort_by = request.args.get('sort_by', 'title')  # Default to sorting by title
    search_query = request.args.get('search', '')  # Get the search query


    # Fetch books based on the sorting option and search query
    if search_query:
        books = Book.query.filter(Book.title.ilike(f'%{search_query}%')).all()
    else:
        if sort_by == 'author':
            books = Book.query.join(Author).order_by(Author.name).all()
        else:  # Default to sorting by title
            books = Book.query.order_by(Book.title).all()

    authors = Author.query.all()
    return render_template('home.html', authors=authors, books=books, sort_by=sort_by)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():

    if request.method == 'GET':
        return render_template('add_author.html')

    elif request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birthdate']
        date_of_death = request.form['date_of_death']

        author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        print(author.__repr__())
        db.session.add(author)
        db.session.commit()
        return render_template('add_author.html', message=f'Author {name} added successfully!')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():

    authors = Author.query.all()

    if request.method == 'GET':
        return render_template('add_book.html', authors=authors)

    elif request.method == 'POST':
        title = request.form['title']
        publication_year = request.form['publication_year']
        isbn = request.form['isbn']
        author_id = request.form['author']

        book = Book(title=title, publication_year=publication_year, isbn=isbn, author_id=author_id)
        db.session.add(book)
        db.session.commit()
        return render_template('add_book.html', message=f'Book {title} added successfully!', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    author = book.author

    # Delete the book
    db.session.delete(book)
    db.session.commit()

    # Check if the author has other books
    if not Author.query.filter_by(id=author.id).first().books:
        db.session.delete(author)  # Delete the author if they have no other books
        db.session.commit()

    flash(f'Book "{book.title}" deleted successfully!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
