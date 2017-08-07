import errno
import logging.handlers
import json
import os
import subprocess
import sys

import gevent

from datetime import datetime
from threading import Timer

WORKING_DIR = os.path.dirname(os.path.realpath(__file__))


class PingTimeout(Exception):
    pass


class Ping(object):

    def __init__(self, count, threshold, timeout, server=None):
        self.server = server
        self.count = count
        self.time_threshold = threshold
        self.timeout = timeout

    def ping_server(self, ip=None):
        ping_ip = None
        if ip:
            ping_ip = ip
        elif self.server:
            ping_ip = self.server

        if ping_ip:
            pping = subprocess.Popen(['/bin/ping', str(ping_ip),
                                      '-c', str(self.count)],
                                     stdout=subprocess.PIPE)
            time = Timer(self.timeout, pping.kill)
            time.start()
            out, code = pping.communicate()
            if time.is_alive():
                time.cancel()
            else:
                raise PingTimeout
            return out, code
        else:
            raise ValueError('IP was not defined')

    def is_result_ok(self, ping_output):
        for line in ping_output.split('\n'):
            log.debug('   line: %s' % line)
            # When not receiving all packet
            if '%s packets transmitted' % self.count in line \
                    and ', 0% packet loss' not in line:
                log.debug('Found lost package.')
                return False
            if 'icmp_seq=' in line and \
                    float(line.split()[6].split('=')[1]) > self.time_threshold:
                log.debug('Found over threshold ping.')
                return False
        return True


class Watcher(object):
    """Watcher object to watch for CI IP pingable"""

    def __init__(self, json_config):
        self.json_config = json_config

        self.pinger = Ping(
            get_config(self.json_config, 'ping_package_number', 3),
            get_config(self.json_config, 'ping_slow_threshold', 500),
            get_config(self.json_config, 'ping_timeout', 30)
        )

        self.fail_threshold = get_config(self.json_config,
                                         'looping_check_fail_threshold',
                                         10)
        self.ok_threshold = get_config(self.json_config,
                                       'looping_check_ok_threshold',
                                       3)
        self.looping_interval = get_config(self.json_config,
                                           'looping_check_interval',
                                           30)

        self.ok_list = []
        self.fail_list = []

    def check(self, ip):
        """Ping to server and check result"""
        try:
            out, _ = self.pinger.ping_server(ip)
            if not self.pinger.is_result_ok(out):
                return False
                # bot.respond(bot.get_admin_channel(), "res is not ok")
        except PingTimeout, _:
            log.warning('Ping result TIMEOUT')
            return False
        except ValueError, e:
            log.warning('Ping result ValueError: %s' % e.message)
            return False
        return True

    @staticmethod
    def cb_ok(self, ip):
        log.info('[%15.15s] looping check total: OK.' % ip)
        self.ok_list.append(ip)

    @staticmethod
    def cb_fail(self, ip):
        log.warning('[%15.15s] looping check total: FAIL.' % ip)
        self.fail_list.append(ip)

    def fail_alert(self):
        mess = 'Fail ping: %s' % \
               ', '.join(self.fail_list)
        log.error(mess)
        try:
            stop_alert_file = os.path.join(WORKING_DIR,
                                           'stop_alert_file')
            with open(stop_alert_file, 'r') as fp:
                first_line = fp.readline().rstrip('\n')
            if first_line:
                try:
                    log.debug('Got from %s: %s' % (stop_alert_file,
                                                   first_line))
                    if first_line == datetime.now().strftime('%Y%m%d'):
                        log.debug('Marked to stop announce for today')
                        return
                except Exception:
                    log.debug('Found %s but wrong content' % stop_alert_file)
                    pass
        except Exception:
            log.debug('Cannot open stop-alert-file')
            pass
        send_alert(mess)

    def looping_check(self, ip, cb_ok, cb_fail):
        """Do the looping check each 1 minute."""

        fail_count = 0
        pass_count = 0
        log.info('[%15.15s] Looping check started...' % ip)
        while True:
            gevent.sleep(self.looping_interval)
            res = self.check(ip)
            if res:
                pass_count += 1
                log.info('[%15.15s] ... passed (%s passed - %s failed)' %
                         (ip, pass_count, fail_count))
            else:
                fail_count += 1
                pass_count = 0
                log.info('[%15.15s] ... failed (%s passed - %s failed)' %
                         (ip, pass_count, fail_count))
            if pass_count == self.ok_threshold:
                cb_ok(self, ip)
                break
            if fail_count == self.fail_threshold:
                cb_fail(self, ip)
                break

    def first_check(self, ip):
        """Do the first check and issue a looping check if fail at the first"""
        if not self.check(ip):
            log.info('[%15.15s] First check failed.' % ip)
            self.looping_check(ip, self.cb_ok, self.cb_fail)
        else:
            log.info('[%15.15s] First check ok.' % ip)
            self.ok_list.append(ip)

    def parallel_check(self, ip):
        job_list = [gevent.spawn(self.first_check, ip)]
        if job_list:
            gevent.joinall(job_list)
        if len(self.fail_list):
            self.fail_alert()


def send_alert(message):
    print('ALERT ALERT ALERT: %s' % message)


def get_config(json_config, key, default_value=None):
    try:
        return json_config[key]
    except Exception:
        return default_value


if __name__ == "__main__":
    config_file = os.path.join(os.path.dirname(__file__), 'ping_server.conf')
    with open(config_file) as json_file:
        json_data = None
        try:
            json_data = json.load(json_file)
        except Exception:
            send_alert('Load %s failed' % config_file)
            exit(1)
        log_file = get_config(json_data, 'log_file', 'ping_server.log')
        if not log_file.startswith('/'):
            log_file = os.path.join(WORKING_DIR, log_file)
        log_level = {
            'debug': logging.DEBUG,
            'info': logging.INFO
        }[get_config(json_data, 'level', 'info')]

        logging.basicConfig()
        log = logging.getLogger("ping_server")
        try:
            os.makedirs(os.path.dirname(log_file))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        handler = logging.handlers.RotatingFileHandler(log_file,
                                                       maxBytes=1048576,
                                                       backupCount=1)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(process)6s] %(levelname)-7s [%(name)s] "
            "%(message)s"))
        log.addHandler(handler)
        logging.getLogger().setLevel(log_level)

        watcher = Watcher(json_data)
        watcher.parallel_check(sys.argv[1])
