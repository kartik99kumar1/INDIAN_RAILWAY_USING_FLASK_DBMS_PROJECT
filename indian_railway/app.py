#to run:  python app.py
# DataBase: MySQL(indian_railway->table:passenger).
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.String(255), nullable=False)
    passenger_name = db.Column(db.String(255), nullable=False)
    train_number = db.Column(db.String(255), nullable=False)
    pnr_id = db.Column(db.String(255), nullable=False)
    ticket_price = db.Column(db.Numeric(10, 2), nullable=False)

@app.route('/')
def index():
    passengers = Passenger.query.all()
    return render_template('index.html', passengers=passengers)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        passenger_id = request.form['passenger_id']
        passenger_name = request.form['passenger_name']
        train_number = request.form['train_number']
        pnr_id = request.form['pnr_id']
        ticket_price = request.form['ticket_price']

        new_passenger = Passenger(
            passenger_id=passenger_id,
            passenger_name=passenger_name,
            train_number=train_number,
            pnr_id=pnr_id,
            ticket_price=ticket_price
        )

        db.session.add(new_passenger)
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            print(f"Error inserting record: {e}")
            return "There was an issue adding the passenger."

    return render_template('insert.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    passenger = Passenger.query.get_or_404(id)

    if request.method == 'POST':
        passenger.passenger_id = request.form['passenger_id']
        passenger.passenger_name = request.form['passenger_name']
        train_number = request.form['train_number']
        pnr_id = request.form['pnr_id']
        ticket_price = request.form['ticket_price']

        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            print(f"Error updating record: {e}")
            return "There was an issue updating the passenger."

    return render_template('update.html', passenger=passenger)

@app.route('/delete/<int:id>')
def delete(id):
    passenger = Passenger.query.get_or_404(id)
    try:
        db.session.delete(passenger)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting record: {e}")
        return "There was an issue deleting the passenger."

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
