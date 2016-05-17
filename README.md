# final-project

## Setup

Add the following line to the host machine's '/etc/hosts' file
```
192.168.255.255 project-budget-tracker
```

```
vagrant up
vagrant ssh
pip install -r requirements.txt
sudo service mongod start
bash run_flask_dev.sh
```

To populate the database:
```
python3 /vagrant/scripts/setup-db.py
```

# Database Commands

To start the service:
```
sudo service mongod start
```

To stop the service:
```
sudo service mongod stop
```

To restart the service:
```
sudo service mongod restart
```

To enter Mongo shell commands:
```
mongo
```

Access application using http://192.168.33.10:8080/