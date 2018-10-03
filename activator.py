#!/usr/bin/env python

import os
from os import system, popen
import sys
from time import sleep


if (len(sys.argv) != 4) and (len(sys.argv) != 3):
    print "Usage: %s <Export Port> <Image Base> <Timeout>" % sys.argv[0]
    exit()

base = os.path.dirname(os.path.abspath(__file__)) + '/chal/'
chal = [f for f in os.listdir(base)]



dockerfile='''FROM %s

RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y lib32z1 xinetd

RUN useradd -m ctf

COPY ./bin/ /home/ctf/
COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./start.sh /start.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /start.sh
RUN chown -R root:ctf /home/ctf
RUN chmod -R 750 /home/ctf
RUN chmod 740 /home/ctf/flag

RUN cp -R /lib* /home/ctf
RUN cp -R /usr/lib* /home/ctf

RUN mkdir /home/ctf/dev
RUN mknod /home/ctf/dev/null c 1 3
RUN mknod /home/ctf/dev/zero c 1 5
RUN mknod /home/ctf/dev/random c 1 8
RUN mknod /home/ctf/dev/urandom c 1 9
RUN chmod 666 /home/ctf/dev/*

RUN mkdir /home/ctf/bin
RUN cp /bin/sh /home/ctf/bin
RUN cp /bin/ls /home/ctf/bin
RUN cp /bin/cat /home/ctf/bin
RUN cp /usr/bin/timeout /home/ctf/bin

WORKDIR /home/ctf

CMD ["/start.sh"]

EXPOSE 9999
''' %sys.argv[2]

startsh='''#!/bin/sh
# Add your startup script

# DO NOT DELETE
/etc/init.d/xinetd start;
sleep infinity;
'''

with open('xinetd_setting', 'r') as setting:
    ctf_xinetd = setting.read()


if len(sys.argv) == 4:
    timeout = int(sys.argv[3])

port = sys.argv[1]


for i in range(0, len(chal)):
    baseaddr = base + chal[i] + '/'
    flag = baseaddr + 'flag'
    binary = baseaddr + chal[i]
    if len(sys.argv) == 4:
        timeout = int(sys.argv[3])
        if timeout == 0:
            runsh = '''
            #!/bin/sh
            exec 2>/dev/null
            ./%s
            ''' % chal[i]
        else:
            runsh = '''
            #!/bin/sh
            exec 2>/dev/null
            timeout %d ./%s
            ''' % (timeout, chal[i])
    else:
        runsh = '''
        #!/bin/sh
        exec 2>/dev/null
        timeout %d ./%s
        ''' % (120, chal[i])

    system('rm -rf ctf_xinetd')
    system('rm -rf libc')
    system('mkdir ctf_xinetd')
    system('mkdir ctf_xinetd/bin')

    open('ctf_xinetd/Dockerfile','w').write(dockerfile)
    open('ctf_xinetd/ctf.xinetd','w').write(ctf_xinetd)
    open('ctf_xinetd/start.sh','w').write(startsh)
    open('ctf_xinetd/bin/run.sh','w').write(runsh)

    system('cp chal/%s/* ctf_xinetd/bin/'% chal[i])
    system('chmod +x ctf_xinetd/bin/%s'%chal[i])
    system('chmod +x ctf_xinetd/bin/run.sh')
    system('chmod +x ctf_xinetd/start.sh')
    if popen("sudo docker images -q %s" % chal[i]).read() == '':
        system('sudo docker build -t "%s" ./ctf_xinetd'%chal[i])
    else:
        if_rm = raw_input("\033[0;31mimage already exist, remove or just run it ?[rm/run]\n\033[0m")
        checker = popen('sudo docker ps -aq --filter "name=%s"' % chal[i]).read()
        if checker:
            system('sudo docker stop %s' % checker)
            system('sudo docker rm %s' % checker)
        if if_rm == 'rm':
            system('sudo docker rmi $(sudo docker images -q %s)' % chal[i])
            system('sudo docker build -t "%s" ./ctf_xinetd'% chal[i])
    sleep(1)
    system('sudo docker run --ulimit nproc=1024:2048 -d -p "0.0.0.0:%s:9999" -h "%s" --name="%s" %s'%(port,chal[i], chal[i], chal[i]))
    system('mkdir libc')
    system('sudo docker cp --follow-link %s:lib/x86_64-linux-gnu/libc.so.6 libc/libc64.so'%chal[i])
    system('sudo docker cp --follow-link %s:lib32/libc.so.6 libc/libc32.so'%chal[i])
    print '''\033[0;32m
    ============================
    ||  [+] Deploy finish :)  ||
    ============================
    Challenge: %s
    try nc 0 %s\033[0m
    '''% (chal[i], port)
    port = str(int(port) + 1)