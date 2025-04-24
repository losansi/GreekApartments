from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Newlife@localhost/GreekApartments'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models

class UnitsRegistration(db.Model):
    __tablename__ = 'Units'
    Unit_id = db.Column(db.Integer, primary_key=True)
    Build_num = db.Column(db.String, nullable=False)
    Unit_num = db.Column(db.String, nullable=False)
    Owner_name = db.Column(db.String, nullable=False)
    Occupant_by = db.Column(db.String, nullable=True)

class OwnerLogin(db.Model):
    __tablename__ = 'logins'
    login_id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String)
    password = db.Column(db.String)
    last_login = db.Column(db.DateTime)
    Owner_email = db.Column(db.String)
    Owner_phone = db.Column(db.String)

class OwnersRegistration(db.Model):
    __tablename__ = 'Owners'
    Owner_name = db.Column(db.String, primary_key=True)
    Owner_email = db.Column(db.String)
    Owner_phone = db.Column(db.String)
    Unit_id = db.Column(db.Integer, db.ForeignKey('Units.Unit_id'))

class UnitsOccupant(db.Model):
    __tablename__ = 'Occupante'
    Occupant_name = db.Column(db.String, primary_key=True)
    Occupant_in = db.Column(db.String)
    Occupant_out = db.Column(db.String)
    Occupant_phone = db.Column(db.String)
    Occupant_email = db.Column(db.String)
    Unit_id = db.Column(db.String)
    Occupant_by = db.Column(db.String)

class UnitsPayment(db.Model):
    __tablename__ = 'Payment_History'
    Payment_id = db.Column(db.String, primary_key=True)
    Payment_date = db.Column(db.DateTime)
    Payment_amount = db.Column(db.String)
    Payment_type = db.Column(db.String)


# Routes

@app.route('/')
def home():
    return redirect(url_for('manager'))  # Redirect to your main page
@app.route('/manager')
def manager():
    try:
        units = UnitsRegistration.query.all()
        return render_template('manager.html', units=units, message='')
    except Exception as e:
        return render_template('manager.html', units=[], message=f"Error: {e}")

@app.route('/unit', methods=['POST'])
def add_unit():
    try:
        build_num = request.form['Build_num']
        unit_num = request.form['Unit_num']
        owner_name = request.form['Owner_name']
        occupant_by = request.form['Occupant_by']
        unit = UnitsRegistration(Build_num=build_num, Unit_num=unit_num, Owner_name=owner_name, Occupant_by=occupant_by)
        db.session.add(unit)
        db.session.commit()
        return redirect(url_for('manager'))
    except Exception as e:
        return render_template('manager.html', message=f"Error: {e}")

@app.route('/unit/update/<int:unit_id>', methods=['POST'])
def update_unit(unit_id):
    try:
        unit = UnitsRegistration.query.get(unit_id)
        unit.Build_num = request.form['Build_num']
        unit.Unit_num = request.form['Unit_num']
        unit.Owner_name = request.form['Owner_name']
        unit.Occupant_by = request.form['Occupant_by']
        db.session.commit()
        return redirect(url_for('manager'))
    except Exception as e:
        return render_template('manager.html', message=f"Error: {e}")

@app.route('/unit/delete/<int:unit_id>', methods=['POST'])
def delete_unit(unit_id):
    try:
        unit = UnitsRegistration.query.get(unit_id)
        db.session.delete(unit)
        db.session.commit()
        return redirect(url_for('manager'))
    except Exception as e:
        return render_template('manager.html', message=f"Error: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)