# used to configure the web page
from flask import Flask, render_template, url_for, request, redirect

# used to configure the database
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

# references this file
app = Flask(__name__)

# "///" is a relative path, "////" is an absolute path. Chose relative path this time so I don't have to provide exact location; just project location.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize databsae with seetings from app
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

    # default datetime is creation time (now, etc.)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# set up database at this point in interactive python terminal: 
    # >>> python
    # >>> from app import db
    # >>> db.create_all()
    # >>> exit()

# root directory of app
# POST allows me to update the database
@app.route('/', methods=['POST', 'GET'])
# displays text on the index.html page (localhost:5000)

def index():
    if request.method == 'POST':
                       #pass in the ID's value for the form
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            #adds newly added content to database and commits
            db.session.add(new_task)
            db.session.commit()

            #afterwards, go back to root page
            return redirect('/')

        except:
            return "There was an issue adding your task"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return "There was a problem deleting that task."


# try to figure out how to do an update without the tutorial. If I get stuck, then do it
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    task = Todo.query.get_or_404(id)

    if request.method == 'POST':

        # set current task's content to what's provided in input form
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return "There was a problem updating the task"

    else:
        return render_template('update.html', task=task)

    #return ''

    # replace the current value with the new value
    # save and commit the change to the database
    # redirect back to the root

# runs the app, shows debug messages on screen
if __name__ == "__main__":
    app.run(debug=True)
