DisBadge
========

Turns that EdgeBadge or PyBadge into a sweet Discord notification companion!


Hardware Dependencies
=====================

* [Adafruit EdgeBadge](https://www.adafruit.com/product/4400) OR [Adafruit PyBadge](https://www.adafruit.com/product/4200)
* [Adafruit AirLift FeatherWing](https://www.adafruit.com/product/4264)

:warning: This project will not work with the low cost version of the PyBadge!


Firmware Dependencies
=====================

This project runs on CircuitPython 7.1 or later!  Here are versions 7.2, depending on your device:

* [CircuitPython for Adafruit EdgeBadge](https://circuitpython.org/board/edgebadge/)
* [CircuitPython for Adafruit PyBadge](https://circuitpython.org/board/pybadge/)


CircuitPython Library Dependencies
==================================

These are the CircuitPython libraries you'll need to download:

* adafruit_bitmap_font
* adafruit_bus_device
* adafruit_display_shapes
* adafruit_display_text
* adafruit_esp32spi
* adafruit_imageload
* adafruit_led_animation
* adafruit_requests
* adafruit_wsgi
* neopixel

You can find them by downloading the latest version of the [CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases).  Make sure to download the ZIP file named something like  ``adafruit-circuitpython-bundle-7.x-mpy-XXXXXXXX.zip``.


Setup
=====

Hardware Setup
--------------

Solder the male header pins to the AirLift FeatherWing and connect it to the back of the EdgeBadge/Pybadge.

Upgrading CircuitPython
-----------------------

You can find instructions on installing or upgrading CircuitPython [here](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython).

Downloading Project Files
------------------------

You can download the latest release of this project on Github in the [Releases section](https://github.com/tekktrik/disbadge/releases). Download the ``disbadge_project.zip`` file and extract the files to a folder.

Install required libraries
--------------------------

In a command terminal, install the libraries in ``requirements.txt`` using ``pip``:

```
pip3 install -r requirements.txt
```

If that doesn't work, try the following:

```
python3 -m pip install -r requirements.txt
```

Setting Up Discord Bot
----------------------

You can find instructions on how to set up a Discord bot for Py-Cord [here](https://docs.pycord.dev/en/master/discord.html).
Take note of the bot token, you'll need it later.

You can also find instructions [here](https://poshbot.readthedocs.io/en/latest/guides/backends/setup-discord-backend/#find-your-guild-id-server-id) for determining the Guild ID of where your bot will live.  You will need this later as well!

Final Touches
-------------

One file that must be added to the project yourself is a file called ``secrets.py``.  This file will hold all the secret
information that you must supply yourself.  This file should be saved in the ``shared`` folder and will contain the
following information:

| Setting     |            Description            | Type |
| ----------- | --------------------------------- | ---- |
| SSID        | Wi-Fi network name                | str  |
| Password    | Wi-Fi password                    | str  |
| Guild ID    | The Discord channel the bot is in | int  |
| Login Token | The Bot token                     | str  |

Here's an example of what the file should look like:

```python
secrets = {
    "ssid": "NetworkName",
    "password": "YourPassword123",
    "guild-id": 123456789123456789,
    "login-token": "a1B2c3D4e5F6g7H8i9J0.k1L2m3N4o5P6q7R8_s9T0u1V2w3X4y5Z6"
}
```

:warning: The above information isn't real. **NEVER** share your network or Discord information with anyone!

Adding Files to the EdgeBadge/PyBadge
-------------------------------------

Simply plug in the EdgeBadge/PyBadge to your computer and copy/paste the files in the ``pybadge`` folder to it.
Additionally, you should copy/paste the ``shared`` folder to the device as well.  Finally, add all of the
CircuitPython libraries to a folder named ``lib``.


Starting Up the DisBadge
====================

To run the DisBadge (your new Discord Companion device!), connect the device to a power source (battery or USB cable) and turn it on.
The device will begin setting up things behind the scenes, like connecting to Wi-Fi. When it's ready, it will display your IP address.

Open up a command terminal in the project folder and run ``raspberrypi_bot_link.py`` and add the IP address displayed as a command
lin argument:

```
python3 raspberrypi_bot_link.py 123.45.6.789
```

This will start up the program on your computer that will actually managing communication with the bot.  It will automatically setup-discord-backend
connect to the DisBadge, as the screen will display "No messages!"


Using the DisBadge
==================

Using the DisBadge is easy!  From the channel containing the bot, anyone can just use any of the following slash commands,
along with an associated message:

| Slash Command |        Description        |
| ------------- | ------------------------- |
| ``/ping``     | Send a ping               |
| ``/cheer``    | Send some good vibes!     |
| ``/hype``     | LET'S GOOOOOOOOOOOOOOOOOO |

This will send the message attached with each slash command to the DisBadge, which will notify you and display the message
afterwards. Each has a slightly different sound, notification screen, and light sequence when it receives the message. Try
them all!

The message will stay on the screen until any of the following occur:

* 10 minutes pass after the message comes in
* You press the B button on the DisBadge
* A new message comes in to replace it

There is currently no timeout or wait associated with how fast messages can be sent.  Make sure to let your friends
know not to spam you!


Additional Features
===================

If you want to use the DisBadge without sound, you can use the ``--mute`` flag when starting up the computer script:

```
python3 raspberrypi_bot_link.py 123.45.6.789 --mute
```

This will let the DisBadge know that it shouldn't make any notification sounds.
