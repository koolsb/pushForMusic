# pushForMusic

Push for Music is a python script that turns on a relay connected to an amplifier whenever a button is pressed for a specified period of time. This enhances a standard timer relay with the following features:

* Change the timer programmatically
* Log when a button is pressed to determine usage
* Turn the speaker on or off remotely via API call
* **Button LED must be activated in order for speakers to activate**
* Button LED turns off while speakers are on


## Configuration Parameters

* ```timeout``` - specifies number of seconds the amplifier relay is activated
* ```button_pin``` - GPIO pin number (NOT physical pin number) connected to the button normally open pin
* ```button_led_pin``` - GPIO pin number connected to the button's backlight
* ```relay_pin``` - GPIO pin connected to the amplifier relay
* ```log``` - True / False to enable logging of button presses
* ```log_file``` - text file to log button presses to

## API Endpoints

Flask is a micro http server for Python. This script creates an endpoint on port 5000 to access the calls below ```http://x.x.x.x:5000/<endpoint>```

* ```/music/on``` - turns the speakers on
* ```/music/off``` - turns the speakers off
* ```/music/status``` - returns 1 if speakers are on, 0 if off
* ```/led/on``` - turns the button LED on
* ```/led/off``` - turns the button LED off
* ```/led/status``` - returns 1 if the button LED is on, 0 if off
* ```/push``` - simulates a button press
* ```/shutdown``` - shuts down the host

## Systemd file

An example systemd file is included to run this script as a service. Update the button.service file line 7 to indicate where your script is stored ```ExecStart=/usr/bin/python3 /<path_to_file>/button.py```.

Store the file in ```/lib/systemd/system```

Run: ```systemctl daemon-reload```

Start the service: ```systemctl start button```

Enable the service to automatically start at boot: ```systemctl enable button```
