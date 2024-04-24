 # IPAddress Tracker
                                                            
This application is built using Python to store most recent IP address of the RPI as it tends to change arbitrarily and it also sends an email when the RPI starts or restarts. If the current IP address changes it stores the updated IP in Firebase in case of RPI3 and in case of RPI0 it sends the info to an API hosted on webserver which updates the info in firebase.

---

### Firebase preparation
- Add the entry of the rpidescription in the Firebase Database -> RPI-details -> add new instance of the RPI and add field parameters with required information. Example: IPAddress: 172.21.197.141
         collection: blackbox
         location: growth room #1 (Middle)
         password: gafst1234
         type: rpi3
         username: wendy-king
- RPI details can be updated in Firebase using https://console.firebase.google.com/u/1/project/rpi-dataset/firestore/data/~2FRPI-details

---

### Flow of the application:
<img src="https://github.com/TsailabBioinformatics/TrackIPAddress/blob/main/RPI3-IPStatus.jpg" alt="Alt text" title="Optional title">
<img src="https://github.com/TsailabBioinformatics/TrackIPAddress/blob/main/RPI0-IPStatus.jpg" alt="Alt text" title="Optional title">

### Instructions
1. Clone this repository. \
`git clone https://github.com/sakshi-seth-17/TrackIPAddress.git`

2. Make neccessary changes required in the getIP.py wrt specific RPI. 

3. Travel to the parent project directory and install the required python packages. \
Create virtual environment – `python3 -m venv venv` \
`source venv/bin/activate` \
`pip3 install -r requirement.txt` \
To check if application is working fine run – `python3 getIP.py` 

### Create service file to make the app run indefinitely
`sudo nano /lib/systemd/system/ipstatus.service` \
Paste below lines inside the file by making necessary changes 


	[Unit] 
	Description=IP address 
	After=multi-user.target 


	[Service] 
	WorkingDirectory=/home/sonya-cummings 
	User=sonya-cummings 
	ExecStart=/home/sonya-cummings/trackIPadress/venv/bin/python3 /home/sonya-cummings/trackIPadress/getIP.py
	Restart=on-failure 


	[Install] 
	WantedBy=multi-user.target 

`sudo chmod 644 /lib/systemd/system/ipstatus.service` \
`sudo systemctl enable ipstatus.service` \
`sudo systemctl daemon-reload` \
`sudo systemctl start ipstatus.service` \
`sudo systemctl status ipstatus.service` 

---
### Folder Structure
	- venv/
	- getIP.py
	- getIP-rpi0.py
	- config.json (Not on github, need to ask for this file from lab members)
	- sendEmail.py
	- userdefined.py
	- db-key.json (Not on github, need to ask for this file from lab members)
	- requirement.txt
	
---
### Note
If RPI3 -> use getIP.py \
If RPI0 -> save content of getIP-rpi0.py to getIP.py (config.json and db-key.json won't be required)
