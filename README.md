# Raspi-Robot-Snapshot
Raspberry Pi application for uploading images from camera on robot.

# Python (2.7.3) Libraries
twython  
picamera  

# Using the Raspberry Pi's Camera
Simply use raspi_pic() with the camera plugged in  

# Using a USB Camera
Requires fswebcam and calls directly via subprocess call  
Simply use raspi_usb_camera_pic()  

# To run
python snapshot.py  
	-Note: will request authorization information  

python snapshot.py auth.txt  
	-Note: auth.txt should have the following information (each on a separate line)  
		Consumer Key  
		Consumer Secret  
		Access Token Key  
		Access Token Secret  