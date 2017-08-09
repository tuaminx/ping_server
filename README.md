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
2017-08-09 19:20:18,134 [ 25777] INFO    [ping_server] [             Gateway] First check ok.
2017-08-09 19:20:20,287 [ 25989] INFO    [ping_server] [Server 3 is swaped n] First check ok.
2017-08-09 19:20:20,315 [ 25972] INFO    [ping_server] [Server 1 checked whe] First check ok.
2017-08-09 19:20:30,279 [ 25982] INFO    [ping_server] [Server 2 checked whe] First check failed.
2017-08-09 19:20:30,279 [ 25982] INFO    [ping_server] [Server 2 checked whe] Looping check started...
2017-08-09 19:20:45,319 [ 25982] INFO    [ping_server] [Server 2 checked whe] ... failed (0 passed - 1 failed)
2017-08-09 19:21:00,359 [ 25982] INFO    [ping_server] [Server 2 checked whe] ... failed (0 passed - 2 failed)
2017-08-09 19:21:00,359 [ 25982] WARNING [ping_server] [Server 2 checked whe] looping check total: FAIL.
2017-08-09 19:21:00,360 [ 25982] ERROR   [ping_server] Fail ping: Server 2 checked when above passed but failed and more 20 chars
2017-08-09 19:21:00,360 [ 25982] ERROR   [ping_server] ALERT ALERT ALERT: Fail ping: Server 2 checked when above passed but failed and more 20 chars
```
