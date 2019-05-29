## flask run
```py
## go to /home/stu/project-01/PUG/webapp/WebApp
python app.py
```
## deploy with uWSGI

start and enable uWSGI service
```sh
sudo systemctl start app
sudo systemctl enable app
```

check the status and debug:
```sh
sudo systemctl status app
```

stop the service

```sh
sudo systemctl stop app
```
