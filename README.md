# final-project

## Setup

```
vagrant up
vagrant ssh
sudo service mongod start
bash run_flask_dev.sh
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