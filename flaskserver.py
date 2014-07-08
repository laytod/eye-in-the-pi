from flask import Flask, url_for, render_template, jsonify, request
import datetime
import RPi.GPIO as GPIO
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
## GPIO.cleanup()
GPIO.setwarnings(False)

pins = { 17 : {'name': 'led01', 'state': GPIO.LOW} }
# pins = {}

for pin in pins:
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

@app.route('/get_content')
def get_content():
   buttonID = request.args.get('id', 'Button ID not found.')

   if buttonID == 'button1':
      content = 'Button 1 content area'
   elif buttonID == 'button2':
      content = 'You clicked on button 2.  Good for you!'
   elif buttonID == 'button3':
      content = "This is the content area for button 3.  Isn't it spiffy?"
   else:
      content = buttonID

   return jsonify(result=content)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/changePin")
def action():
   action = request.args.get('action', None)
   pin = request.args.get('pin', None)
   pin = int(pin)

   try:
      if action == 'off':
         GPIO.output(pin, GPIO.HIGH)
      elif action == 'on':
         GPIO.output(pin, GPIO.LOW)

      result = True
   except:
      result = False

   return jsonify(result=result)

   # # Convert the pin from the URL into an integer:
   # changePin = int(changePin)
   # # Get the device name for the pin being changed:
   # deviceName = pins[changePin]['name']
   # # If the action part of the URL is "on," execute the code indented below:
   # if action == "on":
   #    # Set the pin high:
   #    GPIO.output(changePin, GPIO.HIGH)
   #    # Save the status message to be passed into the template:
   #    message = "Turned " + deviceName + " on."
   # if action == "off":
   #    GPIO.output(changePin, GPIO.LOW)
   #    message = "Turned " + deviceName + " off."
   # if action == "toggle":
   #    # Read the pin and set it to whatever it isn't (that is, toggle it):
   #    GPIO.output(changePin, not GPIO.input(changePin))
   #    message = "Toggled " + deviceName + "."

   # # For each pin, read the pin state and store it in the pins dictionary:
   # for pin in pins:
   #    pins[pin]['state'] = GPIO.input(pin)

   # # Along with the pin dictionary, put the message into the template data dictionary:
   # templateData = {
   #    'message' : message,
   #    'pins' : pins,
   # }

   # # return jsonify(result=content)
   # return render_template('main.html', **templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8088, debug=True)