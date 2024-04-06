from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import pyautogui as pg
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'Bablu@12345'

###############################
##### Contact Us Database #####
###############################


class Contactus(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  message = db.Column(db.String(200))

  def __init__(self, name, email, message):
    self.name = name
    self.email = email
    self.message = message


with app.app_context():
  db.create_all()

###############################
##### Here all End points #####
###############################


# Load Home Page
@app.route('/')
def index():
  return render_template('home.html', title='Home')


# Load Auto Message Page
@app.route('/auto_msg', methods=['GET', 'POST'])
def msg():
  # Variable to track whether the message sending process is ongoing
  sending_messages = False

  if request.method == 'POST':
    # Check if the stop button is pressed
    if 'stop' in request.form:
      # Set sending_messages to False to exit the loop
      sending_messages = False
      flash('Message sending stopped.', 'info')
      return redirect('/auto_msg')  # Redirect to clear the form

    try:
      num_msg = int(request.form['num_msg'])  # Convert input to integer
      message = request.form['message']
      time.sleep(5)
      sending_messages = True  # Start sending messages

      # Loop to send messages
      for _ in range(num_msg):
        if not sending_messages:
          # If sending_messages is set to False, exit the loop
          break
        pg.write(message)
        pg.press("enter")
      flash(f'Message Sent {num_msg} times Successfully.', 'success')
      return redirect('/auto_msg')  # Redirect to clear the form
    except ValueError:
      flash('Please enter a valid integer for the number of messages.',
            'error')

  # If sending_messages is True, it means the message sending process is ongoing
  # Render the template with the "Stop Sending" button
  return render_template('auto_msg.html',
                         title='Auto-Msg',
                         sending_messages=sending_messages)


# Load Contact Us Page
@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
  if request.method == 'POST':
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    new_contact = Contactus(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()
    flash('Message Sent Successfully.', 'success')
    return redirect('/contactus')

  return render_template('contactus.html', title='Contact Us')


# Load About Page
@app.route('/about')
def about():
  return render_template('about.html', title='About')


if __name__ == '__main__':
  app.run(debug=True)
