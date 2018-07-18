import subprocess

from threading import Timer


def send_alert(message, log=None):
    """ This function is used by ping_server.py to send alert
    Do NOT change this function name.

    :param message: Mess to be sent out
    :param log: logger object passed from ping_server.py
    :return: None
    """
    try:
        log.error('ALERT ALERT ALERT: %s' % message)
    except Exception:
        print('ALERT ALERT ALERT: %s' % message)
        pass
    palert = subprocess.Popen(["echo %s" % message],
                              stdout=subprocess.PIPE,
                              shell=True)
    time = Timer(30, palert.kill)
    time.start()
    _, _ = palert.communicate()
    if time.is_alive():
        time.cancel()
