# Growth room monitoring project

This project composed of 3 main parts, the setup of Raspberry Pis, server data receiving API, and the dashboard. 

## Raspberry Pi setting

These Python applications are designed for Raspberry Pi management, facilitating tasks ranging from IP address tracking to storing sensor data such as temperature, humidity, thermal readings, brightness levels, and images directly into the local database housed on the lab's server.

### Features
- Dynamically track IP addresses due to their ever-changing nature and store them in Firebase.
- Store sensor data efficiently.

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

Clone the repository TrackIPAddress and RPI3 or RPI0 (based on the RPI type):
```bash
git clone []
cd TrackIPAddress
source venv/bin/activate
python3 pip3 install -r requirement.txt

cd RPI3 or cd RPI0
source venv/bin/activate
python3 pip3 install -r requirement.txt

```

### Usage

To use TrackIPAddress from the command line:
```
python3 getIP.py
```
To use RPI3 or RPI0 Data collector from the command line:
```
python3 app.py
```

## Data Receiver API
Using Flask, this API receives data from RPis and store it in a SQLite database for the dashboard.

### Installation

```bash
git clone []
cd SensorsData-App
source venv/bin/activate
python3 pip3 install -r requirement.txt
```


## RPI0-API
Constructed with Python's Flask package, this API is dedicated to storing data transmitted from RPI0 into a Firebase database. Due to the absence of Firebase package support in RPI0, this API serves as a workaround for data transmission. Hosted on lab's webserver.


## Getting Started

#### Local Installation
Clone the repository RPI0-API on lab's webserver
```bash
git clone []
cd RPI0-API
source venv/bin/activate
python3 pip3 install -r requirement.txt
```

## Data Dashboard
Using Streamlit, this dashboard displays temperature, humidity, and brightness through graphs, along with images arranged in a grid format.

### Installation
Clone the repository Dail Reporting on lab's webserver
```bash
git clone []
cd DailyReporting-App
source venv/bin/activate
python3 pip3 install -r requirement.txt
```

### Usage

```
streamlit run app.py
```



