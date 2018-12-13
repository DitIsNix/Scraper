## Specs
Pi 2B rev 1.1  
1 GB RAM  
ARMv7 CPU  

## Resources
buttons.py  
scrape.py  
splash.png  

Chromium: 65.0  
Needs [chromedriver: 2.38](https://launchpad.net/ubuntu/trusty/+package/chromium-chromedriver)  
double-click .deb to install  
_Selenium only works after install_  

## SSH
`sudo raspi-config`  
Interfaces -> enable SSH  

## make py script executable
`sudo chmod +x /home/pi/example.py`  

## run it after boot
`sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart`  
add to bottom: `@/usr/bin/python /home/pi/scraper.py`  

## no mouse
`sudo apt-get install unclutter`  
`sudo nano /etc/default/unclutter`  
change `EXTRA_OPTS="-idle 1 -root"` to `EXTRA_OPTS="-idle 2 -root"`  

## no screensaver
`sudo apt-get install xscreensaver`  
`disable screen sleep`  
OR  
`sudo nano /etc/lightdm/lightdm.conf`  
change `#xserver-command=X` to `xserver-command=X -s 0 -dpms`  

## screen rotate and disable rainbow
`sudo nano /boot/config.txt` -> add to bottom  
screen rotate  
* (for 90 degrees): `display_rotate=2`  
* (for 270 degrees): `display_rotate=3`  
no rainbow image: `disable_splash=1`  

## i forgot what this does; some more clean start up?
`sudo nano /boot/cmdline.txt`  
change: `console=tty1`  to  `console=tty3`  
check if present: `splash quiet plymouth.ignore-serial-consoles`  
add at end of the line: `logo.nologo vt.global_cursor_default=0`  

## replace old splash image
`sudo cp /new/splash.png /usr/share/plymouth/themes/pix/splash.png`  

# To do:
- [ ] Split py-script into scraper and buttons
- [ ] Write bash script to run part of setup
