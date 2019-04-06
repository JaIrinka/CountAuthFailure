from time import time

from systemd.journal import Reader

def count_auth_failure():
    count = 0
    auth_log = Reader()
    start_time = time() - 60**2
    auth_log.add_match("SYSLOG_FACILITY=10", "PRIORITY=5")
    auth_log.seek_realtime(start_time)
    for entry in auth_log:
        if entry['MESSAGE'].find('authentication failure') >= 0 and \
           entry['MESSAGE'].find('sshd:auth') == -1:
            count+=1

    return count