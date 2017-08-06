# Ping server

Use cron job to ping multiple servers and send alert

## Require:

* Python 2. If on Ubuntu `sudo apt-get install python2 python-pip`
* Python package gevent. `sudo pip install gevent`

## Usage:

Update `ping_server.conf`
Run `$ ./ping_server.sh`

To run automatically, please use cronjob `crontab -e`

## Example log file:

```
2017-08-07 00:02:07,669 [8222] INFO    [ping_server] [            server 1] First check ok.
2017-08-07 00:02:19,717 [8222] INFO    [ping_server] [            server 2] First check failed.
2017-08-07 00:02:19,718 [8222] INFO    [ping_server] [            server 2] Looping check started...
2017-08-07 00:02:21,751 [8222] INFO    [ping_server] [server 3 very long n] First check ok.
2017-08-07 00:02:33,796 [8222] INFO    [ping_server] [            server 4] First check failed.
2017-08-07 00:02:33,797 [8222] INFO    [ping_server] [            server 4] Looping check started...
2017-08-07 00:02:45,861 [8222] INFO    [ping_server] [            server 2] ... failed (0 passed - 1 failed)
2017-08-07 00:02:57,926 [8222] INFO    [ping_server] [            server 4] ... failed (0 passed - 1 failed)
2017-08-07 00:03:09,990 [8222] INFO    [ping_server] [            server 2] ... failed (0 passed - 2 failed)
2017-08-07 00:03:09,997 [8222] WARNING [ping_server] [            server 2] looping check total: FAIL.
2017-08-07 00:03:22,052 [8222] INFO    [ping_server] [            server 4] ... failed (0 passed - 2 failed)
2017-08-07 00:03:22,053 [8222] WARNING [ping_server] [            server 4] looping check total: FAIL.
2017-08-07 00:03:22,054 [8222] ERROR   [ping_server] Fail ping: server 2, server 4
```
