# w-snmpwalk

A multi-thread snmpwalk program, it's originally desgined for network device
monitor system. And it works just like snmpwalk command of net-snmp project.


Author
==============
Wang Dayong (Email: wandering_997@sina.com, http://weibo.com/wandering997)


Help
==============

[root@TEST w-snmpwalk]# ./w-snmpwalk.py
usage: w-snmpwalk.py [-h] [--ver VER] [--comm COMM] [--port PORT]
[--datadir DATADIR] [--ip IP] [--ipfile IPFILE]
[--oid OID] [--oidfile OIDFILE] [--oldstyle] [--pysnmp]
[--silent] [--singlefile] [--max MAX] [--timeout TIMEOUT]
[--process]

This is a multi-device snmpwalk program, it works like snmpwalk command of
net-snmp project. So make sure you have installed snmpwalk before using it.

optional arguments:
-h, --help         show this help message and exit
--ver VER          SNMP version, default is 2c
--comm COMM        SNMP community
--port PORT        SNMP UDP port, default is 161
--datadir DATADIR  The path where arp or mac data is stored, default is current directory
                   For example:
                   /var/log/snmp/$(date "+%Y")/$(date "+%Y%m%d")/
--ip IP            ip[:port] list for snmp fetching
--ipfile IPFILE    A filename of ip[:port] list, --ip has higher priority than --ipfile
--oid OID          OID list for snmpwalk
--oidfile OIDFILE  A filename of oid list, --oid has higher priority than --oidfile
--oldstyle         For compatible, use an old format to log.
                   Old Style:
                       shell> cat /var/log/snmp/2015/20151123/172.17.54.1/172.17.54.1#ifHCInOctets.1
                       2015-11-23 12:58:57, ifHCInOctets.1 = Counter64: 2799462542644320;
                   New Style:
                       shell> cat /var/log/snmp/2015/20151123/172.17.54.1/ifHCInOctets.1
                       12:58:57, 2799462542644320
--pysnmp           Use pysnmp module instead of snmpwalk command of net-snmp.
--silent           Silence mode.
--singlefile       If given then write all snmp output of one IP to single file.
--max MAX          The maximum threads/processes could be spread each time, default is 1000.
--timeout TIMEOUT  Time to wait for command executing, default is 5 seconds.
--process          Use multi-process instead of multi-thread.

Example:

./w-snmpwalk.py --comm <YOUR_COMM> --ip 192.168.0.1
./w-snmpwalk.py --comm <YOUR_COMM> --datadir /var/log/snmp/2016/20160123/ --ipfile ./ip.test --silent


[root@TEST w-snmpwalk]#


Examples
==============

    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ls -l
    total 20
    -rwxrwxr-x 1 wangdayong wangdayong 18249 Nov 29 21:53 w-snmpwalk.py
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ./w-snmpwalk.py --comm xxxx --ip 192.168.161.10 --oid sysName
    [2015-11-29 22:29:35] snmpwalk -Os -v 2c -c xxxx 192.168.161.10:161 sysName
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ls -l
    total 24
    drwxrwxr-x 2 wangdayong wangdayong  4096 Nov 29 22:29 192.168.161.10
    -rwxrwxr-x 1 wangdayong wangdayong 18249 Nov 29 21:53 w-snmpwalk.py
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ls -l 192.168.161.10/
    total 4
    -rw-rw-r-- 1 wangdayong wangdayong 51 Nov 29 22:29 sysName
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ cat 192.168.161.10/sysName
    2015-11-29 22:29:35, H3C_S5500
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ./w-snmpwalk.py --comm xxxx --ip 192.168.161.10 --oid sysName --pysnmp
    [2015-11-29 22:29:57] pysnmpwalk -v 2c -c xxxx 192.168.161.10:161 sysName
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ls -l 192.168.161.10/
    total 4
    -rw-rw-r-- 1 wangdayong wangdayong 102 Nov 29 22:29 sysName
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ cat 192.168.161.10/sysName
    2015-11-29 22:29:35, H3C_S5500
    2015-11-29 22:29:57, H3C_S5500
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ./w-snmpwalk.py --comm xxxx --ip 192.168.161.10 --oid ifDescr --silent
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ls 192.168.161.10/
    ifDescr.1   ifDescr.14  ifDescr.19  ifDescr.23  ifDescr.28  ifDescr.32  ifDescr.37  ifDescr.41  ifDescr.46  ifDescr.50  ifDescr.55  ifDescr.8
    ifDescr.10  ifDescr.15  ifDescr.2   ifDescr.24  ifDescr.29  ifDescr.33  ifDescr.38  ifDescr.42  ifDescr.47  ifDescr.51  ifDescr.56  ifDescr.9
    ifDescr.11  ifDescr.16  ifDescr.20  ifDescr.25  ifDescr.3   ifDescr.34  ifDescr.39  ifDescr.43  ifDescr.48  ifDescr.52  ifDescr.57  sysName
    ifDescr.12  ifDescr.17  ifDescr.21  ifDescr.26  ifDescr.30  ifDescr.35  ifDescr.4   ifDescr.44  ifDescr.49  ifDescr.53  ifDescr.6
    ifDescr.13  ifDescr.18  ifDescr.22  ifDescr.27  ifDescr.31  ifDescr.36  ifDescr.40  ifDescr.45  ifDescr.5   ifDescr.54  ifDescr.7
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ cat 192.168.161.10/ifDescr.1
    2015-11-29 22:30:37, GigabitEthernet1/0/1
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ./w-snmpwalk.py --comm xxxx --ip 192.168.161.10 --oid ifDescr --silent --pysnmp
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ cat 192.168.161.10/ifDescr.1
    2015-11-29 22:30:37, GigabitEthernet1/0/1
    2015-11-29 22:30:59, GigabitEthernet1/0/1
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ time ./w-snmpwalk.py --comm xxxx --ip 192.168.161.10 --oid ifDescr --silent
    
    real	0m0.376s
    user	0m0.057s
    sys	    0m0.015s
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ time snmpwalk -On -v 2c -c xxxx 192.168.161.10 ifDescr > tmp
    
    real	0m0.334s
    user	0m0.033s
    sys	    0m0.002s
    [wangdayong@TEST w-snmpwalk]$



    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ls -l
    total 36
    -rw-rw-r-- 1 wangdayong wangdayong 13901 Nov 29 22:36 ip
    -rwxrwxr-x 1 wangdayong wangdayong 18620 Nov 29 22:51 w-snmpwalk.py
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ cat ip |wc -l
    1000
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ tail ip
    172.17.129.6
    172.17.129.60
    172.17.129.61
    172.17.129.62
    172.17.129.63
    172.17.129.64
    172.17.129.65
    172.17.129.66
    172.17.129.67
    172.17.129.68
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ time ./w-snmpwalk.py --comm xxxx --ipfile ip --datadir ./snmp --oid ifDescr --silent
    
    real	0m24.850s
    user	0m47.635s
    sys	    0m56.156s
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ls -l
    total 72
    -rw-rw-r--    1 wangdayong wangdayong 13901 Nov 29 22:36 ip
    drwxrwxr-x 1000 wangdayong wangdayong 36864 Nov 29 22:56 snmp
    -rwxrwxr-x    1 wangdayong wangdayong 18620 Nov 29 22:51 w-snmpwalk.py
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ls -l snmp/ |tail
    drwxrwxr-x 2 wangdayong wangdayong 4096 Nov 29 22:56 172.17.129.6
    drwxrwxr-x 2 wangdayong wangdayong 4096 Nov 29 22:56 172.17.129.60
    drwxrwxr-x 2 wangdayong wangdayong 4096 Nov 29 22:56 172.17.129.61
    drwxrwxr-x 2 wangdayong wangdayong 4096 Nov 29 22:56 172.17.129.62
    drwxrwxr-x 2 wangdayong wangdayong 4096 Nov 29 22:56 172.17.129.63
    drwxrwxr-x 2 wangdayong wangdayong 4096 Nov 29 22:56 172.17.129.64
    drwxrwxr-x 2 wangdayong wangdayong 4096 Nov 29 22:56 172.17.129.65
    drwxrwxr-x 2 wangdayong wangdayong 4096 Nov 29 22:56 172.17.129.66
    drwxrwxr-x 2 wangdayong wangdayong 4096 Nov 29 22:56 172.17.129.67
    drwxrwxr-x 2 wangdayong wangdayong 4096 Nov 29 22:56 172.17.129.68
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ls snmp/172.17.129.68 |tail
    ifDescr.52
    ifDescr.53
    ifDescr.54
    ifDescr.55
    ifDescr.56
    ifDescr.57
    ifDescr.6
    ifDescr.7
    ifDescr.8
    ifDescr.9
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ cat snmp/172.17.129.68/ifDescr.9
    2015-11-29 22:56:06, GigabitEthernet1/0/9
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$


    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ rm -f snmp/172.17.129.68/ifDescr.*
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ls -l snmp/172.17.129.68/ifDescr*
    ls: cannot access snmp/172.17.129.68/ifDescr*: No such file or directory
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ time ./w-snmpwalk.py --comm xxxx --ipfile ip --datadir ./snmp --oid ifDescr --silent --singlefile --ip 172.17.129.68
    
    real	0m0.370s
    user	0m0.055s
    sys	    0m0.013s
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ ls -l snmp/172.17.129.68/ifDescr*
    -rw-rw-r-- 1 wangdayong wangdayong 2423 Nov 29 23:10 snmp/172.17.129.68/ifDescr
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$ cat snmp/172.17.129.68/ifDescr |tail
    2015-11-29 23:10:27, GigabitEthernet1/0/48
    2015-11-29 23:10:27, GigabitEthernet1/0/49
    2015-11-29 23:10:27, GigabitEthernet1/0/50
    2015-11-29 23:10:27, M-GigabitEthernet0/0/0
    2015-11-29 23:10:27, NULL0
    2015-11-29 23:10:27, Ten-GigabitEthernet1/0/51
    2015-11-29 23:10:27, Ten-GigabitEthernet1/0/52
    2015-11-29 23:10:27, Vlan-interface1
    2015-11-29 23:10:27, Vlan-interface100
    2015-11-29 23:10:27, Bridge-Aggregation1
    [wangdayong@TEST w-snmpwalk]$
    [wangdayong@TEST w-snmpwalk]$


