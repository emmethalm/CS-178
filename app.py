from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Using the candidate concept of "routes"
@app.route("/")
def home():
    todo_list = Todo.query.all()
    # Here I use the "render_template()" function, which is part of the core concept of the "templates" folder & Jinja integration within Flask apps
    return render_template("base.html", todo_list=todo_list)

# Using the candidate concept of "routes" ; had to intentionally add the POST method to modify my database
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

# Using the candidate concept of "routes" ; GET (read value) is implied by default
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

# Using the candidate concept of "routes" ; GET (read value) is implied by default
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    # Added this line to temporarily create an "app context" as to avoid the error "Working outside of application context"
    with app.app_context():
        db.create_all()
    app.run(debug=True)
