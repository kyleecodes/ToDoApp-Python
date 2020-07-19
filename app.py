from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

# app.py is your server
# creates an application names app (name of file) & configures database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:Green@localhost:5432/postgres'

# db.object, creates flask app object
db = SQLAlchemy(app)

# initial migration
migrate = Migrate(app, db)


# MODEL class todoitem, inherits from db.model
# give each a integer primary key
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    # debugging statement, prints id and description
    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


# sync tables and models
db.create_all()


# request handler
# @app.route('/todos/create', methods=['POST'])
# def create_todo():
#     description = request.form.get('description', '')
#     todos = Todos(description=description)
#     db.session.add(todos)
#     db.session.commit()
#     return redirect(url_for('index'))

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


# sets up a route that listens for our index (render_template)
# processes templating using Jinja (allows non-html in html files)
@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())
