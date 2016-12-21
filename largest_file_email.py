"""
Get the top 10 largest files in the current directory and send it by email.

Bash command:
    find . -printf '%s %p\n'|sort -nr|head -10

    This script adds support to show filesizes in a human-readable format.

Usage:
    ./largest_file_email.py -h
"""

import locale
import shlex
import subprocess as sp

import smtplib
from email.mime.text import MIMEText

encoding = locale.getdefaultlocale()[1]


def sizeof_fmt(num):
    """
    Convert file size to human readable format.
    """

    for x in ['b', 'K', 'M', 'G', 'T']:
        if num < 1024.0:
            return "{0:.2f}{1}".format(num, x)
        num /= 1024.0


def human_readable(lines):
    file_list = []
    for line in lines:
        num, fname = line.split(maxsplit=1)
        num = sizeof_fmt(int(num))
        file_list.append('{n} {f}'.format(n=num, f=fname))

    return file_list


def create_top_file_list():
    find = sp.Popen(shlex.split("find . -printf '%s %p\n'"), stdout=sp.PIPE)
    sort = sp.Popen(shlex.split("sort -nr"),
                    stdin=find.stdout, stdout=sp.PIPE, stderr=sp.PIPE)
    out = sort.communicate()[0].decode(encoding).split('\n')
    if len(out) > 10:
        out = out[:10]
    else:
        out = out[:-1]

    return human_readable(out)


def send_email(file_list):
    print('\n'.join(file_list))
    msg = MIMEText('\n'.join(file_list))
    msg['Subject'] = 'Huge files in uat box'
    msg['From'] = 'yongheng.min@citi.com'
    msg['To'] = 'yongheng.min@citi.com'

    s = smtplib.SMTP('127.0.0.1')
    s.send_message(msg)
    s.quit()

##############################################################################
if __name__ == '__main__':
    send_email(create_top_file_list())