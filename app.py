# Collecting height, weight and age. Will email the user their BMI statistics relative to all users.
# Will also tell user how their BMI compares with stats for their age group.
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
# Below we are importing our send_email function from the other py-script.
from send_email import send_email
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Obsidian1989!@localhost/BMI_collection'
db=SQLAlchemy(app)

# After creating the class, we need to instantiate it in the terminal. We could call the class in the script but
# to do so would entail automatically executing the flask app each time.
class Data(db.Model):
    __tablename__='data'
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)
    weight_=db.Column(db.Integer)
    age=db.Column(db.Integer)

    def __init__(self, email_, height_, weight_, age_):
        self.email_ = email_
        self.height_ = height_
        self.weight_ = weight_
        self.age_ = age_

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/success', methods=['GET', 'POST'])
def success():
    # Below we ensure that we are obtaining a post request as the visitor may be approaching the URL via other means. If
    # said-condition holds, then we seize the form element of the http request. Corresponds to form element in our index.
    # html file.
    if request.method == 'POST':
        email = request.form['email_name']
        height = request.form['height_name']
        weight = request.form['weight_name']
        age = request.form['age_name']
        # We need some means of neatly alerting the user to the fact that their email is already logged in the system using a conditional.
        # The below indicates that if the count of preexistent email input is 0, then the information will be uploaded to the database.
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email, height, weight, age)
            db.session.add(data)
            db.session.commit()

            float_BMI = int(height) / int(weight)
            BMI = round(float_BMI, 2)

            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_weight = db.session.query(func.avg(Data.weight_)).scalar()
            # The scalar method converts the output to an integer and the round method tells it to round to a certain number of dec
            # places.
            average_height = round(average_height, 1)
            average_weight = round(average_weight, 1)
            # In addition to sending the average height, we also want to let the user know how statistically significant their
            # data is by sending them the count of total users of our app thus far.
            count = db.session.query(Data.height_).count()

            # We need to save an integer form of our age variable in order to enact the below conditionals.
            integer_age = int(age)

            if integer_age < 16:
                BMI_message = 'As for how your BMI compares with UK averages, you\'re too young to worry about that!'
            elif 16 <= integer_age <= 24:
                BMI_message = 'The average BMI for a UK male aged 16-24 is 24.7 kg/m^2 whereas for females it is 24.5 kg/m^2'
            elif 25 <= integer_age <= 34:
                BMI_message = 'The average BMI for a UK male aged 25-34 is 26.8 kg/m^2 whereas for females it is 27.2 kg/m^2'
            elif 35 <= integer_age <= 44:
                BMI_message = 'The average BMI for a UK male aged 35-44 is 27.6 kg/m^2 whereas for females it is 28 kg/m^2'
            elif 45 <= integer_age <= 54:
                BMI_message = 'The average BMI for both UK males and females aged 45-54 is 28.6 kg/m^2.'
            elif 55 <= integer_age <= 64:
                BMI_message = 'The average BMI for a UK male aged 55-64 is 28.9 kg/m^2 whereas for females it is 28.3 kg/m^2'
            elif 65 <= integer_age <= 74:
                BMI_message = 'The average BMI for a UK male aged 65-74 is 29.3 kg/m^2 whereas for females it is 28.1 kg/m^2'
            else:
                BMI_message = 'The average BMI for a UK male aged 75 or more is 27.6 kg/m^2 whereas for females it is 27.7 kg/m^2'

            send_email(email, height, weight, age, BMI, average_height, average_weight, count, BMI_message)

            return render_template('success.html')
    return render_template('index.html', text='We already have information from that email address.')



if __name__ == '__main__':
    app.debug=True
    app.run()