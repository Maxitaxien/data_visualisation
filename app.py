from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from visualizations import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    filesize = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Data %r>' % self.id

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
                    existing_file = Data.query.filter_by(filename=filename).first()
                    if existing_file:
                        error_message = "File already exists."
                    else:
                        # Calculate file size in bytes
                        file.seek(0, 2)  # Move cursor to the end of the file
                        filesize = file.tell()  # Get current position, which is file size
                        file.seek(0)  # Reset cursor to the beginning of the file

                        new_data = Data(filename=filename, filesize=filesize)
                        try:
                            db.session.add(new_data)
                            db.session.commit()
                        except:
                            error_message = "There was an unknown issue adding your file."

    # Fetch all uploaded files
    files = Data.query.order_by(Data.filesize.desc()).all()
    for file in files:
        file.filesize = format_filesize(file.filesize)

    return render_template('index.html', files=files, error_message=error_message)


@app.route('/plot_file/<filename>', methods=['GET'])
def plot_file(filename):
    return render_template('plot.html', filename=filename)

@app.route('/plot_option', methods=['POST'])
def plot_option():
    option = request.form['option']
    filename = request.args.get('filename')
    if not filename:
        return 'Invalid filename'
    if option == 'plot1':
        # Call function to generate plot 1 data
        plot_data = test_plot()
    elif option == 'plot2':
        # Call function to generate plot 2 data
        plot_data = test_plot()
    else:
        return 'Invalid option'
    return render_template('plot.html', plot_data=plot_data)


@app.route('/remove_file/<filename>', methods=['GET', 'POST'])
def remove_file(filename):
    if request.method == 'GET':
        file_to_remove = Data.query.filter_by(filename=filename).first()
        if file_to_remove:
            db.session.delete(file_to_remove)
            db.session.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
