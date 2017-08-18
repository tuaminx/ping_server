# Ping server

This is a support for a sys-admin.

Sys-admin adds a list of servers which he/she wants to check status of the connection (failed ping or slow ping).

A linux cron-job will call the `ping_server` script frequesntly by the interval in its setting. When a ping to a server is failed, `ping_server` script will alert to Sys-admin.

`ping_server` script can recognize a gateway and ping it first. `ping_server` script just ping the rest after it know the gateway connection is good.

`ping_server` call a linux command to send an alert to Sys-admin, the command is well-prepared by ays-admin (his/her major). e.g: email sending, phone call, sms sending, im message sending, etc.

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
