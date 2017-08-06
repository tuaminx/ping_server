# Ping server

Use cron job to ping multiple servers and send alert

## Require:

* Python 2. If on Ubuntu `sudo apt-get install python2 python-pip`
* Python package gevent. `sudo pip install gevent`

## Usage:

Update `ping_server.conf`
Run `$ ./ping_server.sh`

To run automatically, please use cronjob `crontab -e`
