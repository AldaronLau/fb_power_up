# fb_power_up
First Power Up Video Game

## Arcade
You can run this on a raspberry pi.

### Step 1: Install OS
First install [raspbian minimal](https://downloads.raspberrypi.org/raspbian_lite_latest).  Then install it on an SD Card.

### Step 2: Connect to WiFi (or Ethernet)
For wifi, on your raspberry pi terminal, type `sudo vim.tiny /etc/wpa_supplicant/wpa_supplicant.conf`.

It should look something like this

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
```

add the following at the end of the file

```
network={
				ssid="WIFI_NAME_GOES_HERE"
				psk="WIFI_PASSWORD_GOES_HERE"
				scan_ssid=1
}
```

Of course, replacing WIFI_NAME_GOES_HERE and WIFI_PASSWORD_GOES_HERE with the actual wifi name and password.

Now press ESCAPE, and type `:wq` and press ENTER.

Now type `sudo reboot` to reboot the pi.

### Step 3: Install pygame
In the terminal type: `sudo apt-get update`.

When that is done, type: `sudo apt-get install python3-pygame`

### Step 4: Install git
In the terminal type: `sudo apt-get install git`.

### Step 5: Clone the repo
In the terminal type: `git clone https://github.com/OxyDeadbeef/fb_power_up.git`.

### Step 6: Run The Game
In the terminal type: `cd fb_power_up`.

Now, type: `python3 fpu.py`
