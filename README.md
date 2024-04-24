# RaspberryPis
These Python applications are designed for Raspberry Pi management, facilitating tasks ranging from IP address tracking to storing sensor data such as temperature, humidity, thermal readings, brightness levels, and images directly into the local database housed on the lab's server.

## Features
- Dynamically track IP addresses due to their ever-changing nature and store them in Firebase.
- Store sensor data efficiently.

## Getting Started

### Prerequisites 
- Retrieve the RPI's IP address by executing the "ifconfig" command in the command prompt.
- Enable SSH configuration to allow SSH access to the RPI: Navigate to Preferences -> Raspberry Pi Configuration -> Interfaces -> SSH, then enable it.
- Set up the camera module in the RPI by following these steps:
  - Consult the installation instructions provided at https://elinux.org/RPi-Cam-Web-Interface to configure the camera.
  - Verify the camera functionality by browsing the server's IP address.
  - Prepare the camera for Python script usage by disabling the HTTP option:
    - Use the command "sudo nano /etc/rc.local"
    - Remove the "#" from the line "#START RASPIMJPEG SECTION"
    - Restart the RPI for the changes to take effect.
   
  #### Firebase and Local Database preparation
  - Establish a database table within the Data-Store.db file located on the lab's server to accommodate the specific RPI's data.
  - Maintain updated RPI details on Firebase to ensure accurate tracking of IP addresses.
 

### Installation

#### Local Installation
Clone the repository TrackIPAddress and RPI3 or RPI0 (based on the RPI type):
```bash
git clone https://github.com/TsailabBioinformatics/RaspberryPis.git
cd TrackIPAddress
source venv/bin/activate
python3 pip3 install -r requirement.txt

cd RPI3 or cd RPI0
source venv/bin/activate
python3 pip3 install -r requirement.txt

```

### Usage
#### Command-Line Interface
To use TrackIPAddress from the command line:
```
python3 getIP.py
```
To use RPI3 or RPI0 Data collector from the command line:
```
python3 app.py
```

#### Service file
Can be done for RPI datacollector and tracking IP address 
`sudo nano /lib/systemd/system/datacollector.service` \
Paste below lines inside the file by making necessary changes 

```
  [Unit] 
  Description=rpi3 
  After=multi-user.target 

  [Service] 
  WorkingDirectory=/path_to_user_directory 
  User=sonya-cummings 
  Type=idle 
  ExecStart=/path_to_user_directory/DataCollector/venv/bin/python3 /path_to_user_directory/DataCollector/app.py 
  Restart=on-failure 
  KillMode=process 
  LimitMEMLOCK=infinity 
  LimitNOFILE=65535 
  Type=simple 

  [Install] 
  WantedBy=multi-user.target
```

`sudo chmod 644 /lib/systemd/system/datacollector.service` \
`sudo systemctl enable datacollector.service` \
`sudo systemctl daemon-reload` \
`sudo systemctl start datacollector.service` \
`sudo systemctl status datacollector.service` 


# Daily Reporting App
Constructed using Python's Streamlit package, this application displays daily observations collected by RPIs. It presents data regarding temperature, humidity, and brightness through graphs, along with images arranged in a grid format. The time range covered is segmented into 12AM-6AM, 6AM-12PM, 12PM-6PM, and 6PM-12AM. If the above RPI is setup correctly you should be able to see the data.

## Getting Started

#### Local Installation
Clone the repository Dail Reporting on lab's webserver
```bash
git clone []
cd DailyReporting-App
source venv/bin/activate
python3 pip3 install -r requirement.txt
```

### Usage
#### Command-Line Interface

```
streamlit run app.py
```

#### Service file
Can be done for RPI datacollector and tracking IP address 
`sudo nano /lib/systemd/system/dailyreport.service` \
Paste below lines inside the file by making necessary changes 

```
  [Unit]

Description=Daily Report Service
After=multi-user.target


[Service]
WorkingDirectory=/data/Reporting-Project
User=tsai-apps
Type=idle
ExecStart=/data/Reporting-Project/venv/bin/streamlit run /data/Reporting-Project/app.py --server.port 8089 --server.enableCORS=false --server.sslKeyFile /data/private-keys/private.key --server.sslCertFile /data/private-keys/localhost.crt
Restart=on-failure
KillMode=process
LimitMEMLOCK=infinity
LimitNOFILE=65535
Type=simple


[Install]
WantedBy=multi-user.target

```

`sudo chmod 644 /lib/systemd/system/dailyreport.service` \
`sudo systemctl enable dailyreport.service` \
`sudo systemctl daemon-reload` \
`sudo systemctl start dailyreport.service` \
`sudo systemctl status dailyreport.service` 

