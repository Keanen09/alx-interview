#!/usr/bin/python3
"""
module: script that reads stdin line by line and computes metrics
"""
import sys
import re
import signal
import os
from typing import Any


sig_num = signal.Signals.SIGINT
file_size = []
status_codes = []
possible_status_codes = [200, 301, 400, 401, 403, 404, 405, 500]


def control_loop() -> Any:
    """The function that loops and finds a match from stdin"""
    loop_count = 0

    for line in sys.stdin:
        if loop_count == 10:
            os.kill(os.getpid(), signal.SIGINT)
            return
        pattern = r'\w+'
        matched_group = re.findall(pattern, line)

        loop_count += 1
        last_status_code = matched_group[-2]
        last_file_size = matched_group[-1]
        file_size.append(int(last_file_size))
        status_codes.append(last_status_code)


def signal_handler(pid, signal) -> Any:
    """a function to handle the sigint signal from the user
    """
    printer()
    file_size.clear()
    status_codes.clear()


def int_values(list_strings):
    """a function to make a list of integers
    """
    list_ints = []
    for string in list_strings:
        list_ints.append(int(string))

    return list_ints


def printer():
    """A function that computes metrics
    """
    template = f'File size: {sum(file_size)}'
    print(template)
    visited = []
    current_values = sorted(int_values(status_codes))
    for code in current_values:
        if code in visited:
            continue
        else:
            visited.append(code)
            count = status_codes.count(code)
            loop_template = f'{code}: {count}'
            print(loop_template)


signal.signal(sig_num, signal_handler)

if __name__ == '__main__':
    while True:
        control_loop()
