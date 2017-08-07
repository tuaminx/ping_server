# Ping server

Use cron job to ping multiple servers and send alert

## Require:

* Python 2. If on Ubuntu `sudo apt-get install python2 python-pip`
* Python package gevent. `sudo pip install gevent`

## Usage:

Update `ping_server.conf`
Add server *IP* to `server.list`
Run `$ ./ping_server.sh`

To run automatically, please use cronjob `crontab -e`

## Example log file:

```
2017-08-07 17:30:20,733 [ 13774] INFO    [ping_server] [        1.1.1.1] First check ok.
2017-08-07 17:30:20,781 [ 13786] INFO    [ping_server] [        8.8.4.4] First check ok.
2017-08-07 17:30:20,849 [ 13788] INFO    [ping_server] [        8.8.8.8] First check ok.
2017-08-07 17:30:30,750 [ 13783] INFO    [ping_server] [        4.5.6.7] First check failed.
2017-08-07 17:30:30,750 [ 13782] INFO    [ping_server] [        3.3.3.3] First check failed.
2017-08-07 17:30:30,750 [ 13782] INFO    [ping_server] [        3.3.3.3] Looping check started...
2017-08-07 17:30:30,750 [ 13783] INFO    [ping_server] [        4.5.6.7] Looping check started...
2017-08-07 17:30:45,790 [ 13783] INFO    [ping_server] [        4.5.6.7] ... failed (0 passed - 1 failed)
2017-08-07 17:30:45,790 [ 13782] INFO    [ping_server] [        3.3.3.3] ... failed (0 passed - 1 failed)
2017-08-07 17:31:00,831 [ 13783] INFO    [ping_server] [        4.5.6.7] ... failed (0 passed - 2 failed)
2017-08-07 17:31:00,831 [ 13782] INFO    [ping_server] [        3.3.3.3] ... failed (0 passed - 2 failed)
2017-08-07 17:31:00,832 [ 13782] WARNING [ping_server] [        3.3.3.3] looping check total: FAIL.
2017-08-07 17:31:00,832 [ 13783] WARNING [ping_server] [        4.5.6.7] looping check total: FAIL.
2017-08-07 17:31:00,834 [ 13782] ERROR   [ping_server] Fail ping: 3.3.3.3
2017-08-07 17:31:00,835 [ 13783] ERROR   [ping_server] Fail ping: 4.5.6.7
```
