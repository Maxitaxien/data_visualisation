from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    filesize = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Task %r>' % self.id

def format_filesize(filesize):
    if filesize >= 1024 * 1024:  # If greater than or equal to 1 MB
        return '{:.2f} MB'.format(filesize / (1024 * 1024))
    elif filesize >= 1024:  # If greater than or equal to 1 KB
        return '{:.2f} KB'.format(filesize / 1024)
    else:
        return '{:.2f} bytes'.format(filesize)

@app.route('/', methods=['POST', 'GET'])
def index():
    error_message = None
    if request.method == 'POST':
        if "input_file" in request.files:
            file = request.files['input_file']
            if file.filename != '':
                filename = file.filename
                if not filename.endswith('.csv'):
                    error_message = "Please select a CSV file."
                else:
                    # Calculate file size in bytes
                    file.seek(0, 2)  # Move cursor to the end of the file
                    filesize = file.tell()  # Get current position, which is file size
                    file.seek(0)  # Reset cursor to the beginning of the file

                    # Remove all existing tasks before adding the new one
                    Todo.query.delete()
                    new_task = Todo(filename=filename, filesize=filesize)
                    try:
                        db.session.add(new_task)
                        db.session.commit()
                    except:
                        error_message = "There was an unknown issue adding your task."

    # Fetch the most recent task
    latest_file = Todo.query.order_by(Todo.filesize.desc()).first()
    if latest_file:
        latest_file.filesize = format_filesize(latest_file.filesize)

    return render_template('index.html', file=latest_file, error_message=error_message)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
