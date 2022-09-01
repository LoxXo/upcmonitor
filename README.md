![image](https://i.imgur.com/bcvzkwa.jpg)
# UPC Monitor

UPC Monitor is scraper for upstream and downstream status from Technicolor TC7200 router with UPC control panel. Intended to use with PostgreSQL and Grafana for data collection and visualization. It assumes use of the Linux's systemd service timer to run a code at regular intervals.

One month of data collected every 15 minutes takes ~67MB of disk space in PostgreSQL.

Script runs from `scrapper.py` file.

## Requirements
*This may or may not work on older versions.*

* Python 3.7 or higher
* PostgreSQL 11 or higher
* Grafana 9.1 or higher

## Configuration

1. Clone this repositorium to your Linux system:
```
$ git clone https://github.com/LoxXo/upcmonitor.git
```

2. Change `router_ip=` and `logoff_user=` in `scrapper.py` file:
```py
router_ip = '192.168.1.1'
```
```py
logoff_user = 0
```
When `logoff_user=` is set to 1, during script login it will force log off any current users in router's panel.

3. Also `SQLALCHEMY_DATABASE_URL=` and `schema_name=` in `database.py` files: 

```
SQLALCHEMY_DATABASE_URL = "dialect+driver://username:password@host:port/database"
```
```py
schema_name = "nameofschema"
```

## Python modules installation
Make sure you have Python3 installed on your system.

When in UPC Monitor directory type in terminal:
```bash
$ pip install -r requirements.txt
```
Or by specifying the path:
```bash
$ pip install -r path/to/requirements.txt
```

## PostgreSQL

[PostgreSQL installation](https://www.postgresql.org/download/)

Create database and schema you want to use. Tables will be created after running `scrapper.py` according to classes in `models.py` file.

Required users with privileges in schema:

1. upcmonitor:
   * INSERT
   * SELECT
   * REFERENCES
2. grafana:
   * SELECT


## Grafana

[Grafana installation docs](https://grafana.com/docs/grafana/latest/setup-grafana/installation/)

[Grafana add datasource](https://grafana.com/docs/grafana/latest/datasources/add-a-data-source/) and [more on PostgreSQL](https://grafana.com/docs/grafana/latest/datasources/postgres/)

To import dashboard from project's JSON file after logging in:

1. From left bar choose **Dashboards** and then **Import**.
2. Click **Upload JSON file** and select `Grafana-UPC-Monitor.json` file.
3. After loading it you should see a dashboard same as on screenshot above. Use it as is or modify to fit your needs.



## Creating a service
1. If you want to use it as timed service, create file named `/etc/systemd/system/upcmonitor.service`:
```
[Unit]
Description=UPC router stats scrapper with Postgres
Wants=upcmonitor.timer

[Service]
User=user
Type=oneshot
ExecStart=/usr/bin/python3 '/path/to/scrapper.py'

[Install]
WantedBy=multi-user.target
```
You'll have to:
* type your username after `User=`,
* set the current path to script after `ExecStart=`.

2. Next in same directory create timer for service `upcmonitor.timer`:
```
[Unit]
Description=run upcmonitor once per 15 minutes

[Timer]
Unit=upcmonitor.service
OnCalendar=*:0/15

[Install]
WantedBy=timers.target
```
In example `OnCalendar=` is set to every hour plus multiples of 15 minutes. Setting it to, e.g. `*0:0/1:00` would make it run every hour.

More on [systemd timers](https://wiki.archlinux.org/title/systemd/Timers).


3. To make it work, start timer:
```
$ systemctl start upcmonitor.timer
```
And to automatically start on boot:
```
$ systemctl enable upcmonitor.timer
```
