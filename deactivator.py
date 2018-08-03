#!/usr/bin/env python

import popen
import os


base = os.path.dirname(os.path.abspath(__file__)) + '/chal/'
chal = [f for f in os.listdir(base)]

for i in range(0, len(chal)):
    checker = popen('sudo docker ps -aq --filter "name=%s"' % chal[i])
    if checker:
        print "\033[0;31mStopping & Removing %s container\n\033[0m" % chal[i]
        system('sudo docker stop %s' % checker)
        system('sudo docker rm %s' % checker)
        print "\033[0;31m%s container Removed\n\033[0m" % chal[i]
