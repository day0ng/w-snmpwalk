#!/usr/bin/env python

"""
    A multi-thread snmpwalk program, it's originally desgined for network device
    monitor system. And it works just like snmpwalk command of net-snmp project.

    Copyright (c) Dayong Wang, wandering_997@sina.com
    Distributable under the terms of the GNU General Public License
    version 2. Provided with no warranties of any sort.

    Revision history
    ~~~~~~~~~~~~~~~~
    2016/01/23
    updated by Dayong wang (wandering_997@sina.com)
    replace getopt with argparse

    2016/01/18
    updated by Dayong Wang (wandering_997@sina.com)
    optimize a little bit for the performace.

    2015/11/23
    creates by Dayong Wang (wandering_997@sina.com)

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate: $
    $Rev: $
    $Author: $
"""

import argparse
import getopt
import os
import re
import subprocess
import sys
import threading
import time


g_oid = dict()
g_oid['sysName']                = '1.3.6.1.2.1.1.5'             # do not use 1.3.6.1.2.1.1.5.0, pysnmp will raise error
g_oid['sysDescr']               = '1.3.6.1.2.1.1.1'             # do not use 1.3.6.1.2.1.1.1.0, pysnmp will raise error
g_oid['sysUpTime']              = '1.3.6.1.2.1.1.3'             # do not use 1.3.6.1.2.1.1.3.0, pysnmp will raise error
g_oid['sysLocation']            = '1.3.6.1.2.1.1.6'             # do not use 1.3.6.1.2.1.1.6.0, pysnmp will raise error
g_oid['ifDescr']                = '1.3.6.1.2.1.2.2.1.2'
g_oid['ifAlias']                = '1.3.6.1.2.1.31.1.1.1.18'
g_oid['ifName']                 = '1.3.6.1.2.1.31.1.1.1.1'
g_oid['ifOperStatus']           = '1.3.6.1.2.1.2.2.1.8'
g_oid['ifHighSpeed']            = '1.3.6.1.2.1.31.1.1.1.15'
g_oid['ifHCInOctets']           = '1.3.6.1.2.1.31.1.1.1.6'
g_oid['ifHCInUcastPkts']        = '1.3.6.1.2.1.31.1.1.1.7'
g_oid['ifHCInMulticastPkts']    = '1.3.6.1.2.1.31.1.1.1.8'
g_oid['ifHCInBroadcastPkts']    = '1.3.6.1.2.1.31.1.1.1.9'
g_oid['ifInDiscards']           = '1.3.6.1.2.1.2.2.1.13'
g_oid['ifInErrors']             = '1.3.6.1.2.1.2.2.1.14'
g_oid['ifHCOutOctets']          = '1.3.6.1.2.1.31.1.1.1.10'
g_oid['ifHCOutUcastPkts']       = '1.3.6.1.2.1.31.1.1.1.11'
g_oid['ifHCOutMulticastPkts']   = '1.3.6.1.2.1.31.1.1.1.12'
g_oid['ifHCOutBroadcastPkts']   = '1.3.6.1.2.1.31.1.1.1.13'
g_oid['ifOutDiscards']          = '1.3.6.1.2.1.2.2.1.19'
g_oid['ifOutErrors']            = '1.3.6.1.2.1.2.2.1.20'


g_oid_valuetype = dict()
g_oid_valuetype['sysName']              = 'STRING'
g_oid_valuetype['sysDescr']             = 'STRING'
g_oid_valuetype['sysUpTime']            = 'Timeticks'
g_oid_valuetype['sysLocation']          = 'STRING'
g_oid_valuetype['ifDescr']              = 'STRING'
g_oid_valuetype['ifAlias']              = 'STRING'
g_oid_valuetype['ifName']               = 'STRING'
g_oid_valuetype['ifOperStatus']         = 'INTEGER'
g_oid_valuetype['ifHighSpeed']          = 'Gauge32'
g_oid_valuetype['ifHCInOctets']         = 'Counter64'
g_oid_valuetype['ifHCInUcastPkts']      = 'Counter64'
g_oid_valuetype['ifHCInMulticastPkts']  = 'Counter64'
g_oid_valuetype['ifHCInBroadcastPkts']  = 'Counter64'
g_oid_valuetype['ifInDiscards']         = 'Counter32'
g_oid_valuetype['ifInErrors']           = 'Counter32'
g_oid_valuetype['ifHCOutOctets']        = 'Counter64'
g_oid_valuetype['ifHCOutUcastPkts']     = 'Counter64'
g_oid_valuetype['ifHCOutMulticastPkts'] = 'Counter64'
g_oid_valuetype['ifHCOutBroadcastPkts'] = 'Counter64'
g_oid_valuetype['ifOutDiscards']        = 'Counter32'
g_oid_valuetype['ifOutErrors']          = 'Counter32'



def w_time(time_format = '%Y-%m-%d %H:%M:%S'):

    return time.strftime(time_format, time.localtime(time.time()))



def sys_cmd(str_cmd):
    sp = subprocess.Popen(str_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    str_out = sp.stdout.read()
    str_err = sp.stderr.read()
    sp.wait()
    return [str_out, str_err]


def w_multiprocessing(func_name, func_args, max_process):

    # multi processing
    if func_name == None or func_name == '':
        print('w_multiprocessing() error: func_name is empty.\n')
        return False
    if func_args == None or not isinstance(func_args, list):
        print('w_multiprocessing() error: func_args is wrong.\n')
        return False
    if not isinstance(max_process, int) or max_process == None or max_process == '':
        max_process = 1000

    # create process pool
    process_pool = list()
    for i in range(0, len(func_args)):
        p = multiprocessing.Process(target=func_name, args=func_args[i])
        process_pool.append(p)

    # execute processs for max_process number of processs each time
    process_count = len(process_pool)
    if process_count > max_process:
        i_begin = 0
        i_end = 0
        round_num = process_count / max_process
        if process_count % max_process > 0:
            round_num += 1
        # max_process: How many processs (test) could be executed at one time
        for j in range(0, round_num):
            i_begin = j * max_process
            if j == round_num - 1:                 # the last round
                i_end = process_count
            else:
                i_end = i_begin + max_process
            # start processs
            for i in range(i_begin, i_end):
                process_pool[i].start()
            # terminate processs
            for i in range(i_begin, i_end):
                process_pool[i].join()
    # === process_count <= max_process ===
    else:
        # start processs
        for i in range(0, process_count):
            process_pool[i].start()
        # terminate processs
        for i in range(0, process_count):
            process_pool[i].join()
    # ========== Run processs - End ==========

#___ End of w_multiprocessing() ____



def w_threading(func_name, list_args, int_max_thread):

    # multi threading
    if not func_name:
        print('Error: func_name is not available.\n')
        return False
    if not isinstance(list_args, list):
        print('Error: list_args should be a list().\n')
        return False
    if not isinstance(int_max_thread, int) or int_max_thread < 1:
        int_max_thread = 1000

    # create thread pool
    thread_pool = list()
    for i in xrange(0, len(list_args)):
        th = threading.Thread(target=func_name, args=list_args[i])
        thread_pool.append(th)

    # execute threads for int_max_thread number of threads each time
    thread_count = len(thread_pool)
    if thread_count > int_max_thread:
        i_begin = 0
        i_end = 0
        round_num = thread_count / int_max_thread
        if thread_count % int_max_thread > 0:
            round_num += 1
        # int_max_thread: How many threads (test) could be executed at one time
        for j in xrange(0, round_num):
            i_begin = j * int_max_thread
            if j == round_num - 1:                 # the last round
                i_end = thread_count
            else:
                i_end = i_begin + int_max_thread
            # start threads
            for i in xrange(i_begin, i_end):
                thread_pool[i].start()
            # terminate threads
            for i in xrange(i_begin, i_end):
                thread_pool[i].join()

    # === thread_count <= int_max_thread ===
    else:
        # start threads
        for i in xrange(0, thread_count):
            thread_pool[i].start()
        # terminate threads
        for i in xrange(0, thread_count):
            thread_pool[i].join()
    # ========== Run threads - End ==========

# End of w_threading()



def snmp_oid_label2num(oid_label):

    global g_oid
    if g_oid.has_key(oid_label):
        return g_oid[oid_label]
    else:
        return oid_label



def snmp_oid_num2label(oid_num):

    global g_oid
    tmp_oid_num = oid_num
    for oid_label in g_oid:
        g_oid_num = g_oid[oid_label]
        if re.search("^%s[^0-9]?" % (g_oid_num), oid_num) == None:
            continue
        else:
            tmp_oid_num = re.sub(g_oid_num, oid_label, tmp_oid_num)
            break
    return tmp_oid_num



def snmp_valuetype(oid_label):

    global g_oid
    global g_oid_valuetype
    if g_oid.has_key(oid_label):
        return g_oid_valuetype[oid_label]
    else:
        return ''

# End of snmp_valuetype()



def pysnmp_getnext(snmp_host, snmp_port, snmp_comm, snmp_oid, trans_oid):

    dict_tmp = dict()

    # check arguments
    if (not isinstance(snmp_host, str) or snmp_host.strip() == '' or
        not isinstance(snmp_oid,  str) or snmp_oid.strip()  == ''):
        print('pysnmp_getnext() has wrong arguments: %s, %s, %s' % (snmp_host, snmp_comm, snmp_oid))
        return dict_tmp

    if not isinstance(snmp_port, str) or snmp_port.strip() == '':
        snmp_port = '161'

    if not isinstance(snmp_comm, str) or snmp_port.strip() == '':
        snmp_comm = ''

    if not isinstance(trans_oid, bool):
        trans_oid = False

    # translate OID from lable to number
    snmp_oid_num = snmp_oid_label2num(snmp_oid)

    try:
        cg = cmdgen.CommandGenerator()
        cg_run = cg.nextCmd(
            cmdgen.CommunityData(snmp_comm),
            cmdgen.UdpTransportTarget((snmp_host, snmp_port)),
            snmp_oid_num
        )
    except:
        print("[%s] pysnmp_getnext failed on %s:%s %s" % (w_time(), snmp_host, snmp_port, snmp_comm))
        return dict_tmp

    '''
    varBinds = [[ ObjectType(
                    ObjectIdentity(ObjectName('1.3.6.1.2.1.1.5.0')), 
                    DisplayString(
                        'BJ_HuangCun_3_22-JG-305_S5500', 
                        subtypeSpec=ConstraintsIntersection(
                            ConstraintsIntersection(
                                ConstraintsIntersection(
                                    ConstraintsIntersection(), 
                                    ValueSizeConstraint(0, 65535)
                                    ), 
                                ValueSizeConstraint(0, 255)
                                ), 
                            ValueSizeConstraint(0, 255)
                        )
                    )
                  )
               ]]
    '''
    varBinds = cg_run[3]
    for tmp_line in varBinds:
        try:
            oid = tmp_line[0][0].getOid().prettyPrinter()
            val = tmp_line[0][1].prettyPrint()
        except:
            continue
        # translate OID lable back to number
        if trans_oid:
            oid = snmp_oid_num2label(oid)
        dict_tmp[oid] = val

    # {'ifDescr.1': 'GigabitEthernet0/1',...}
    return dict_tmp                 

# End of pysnmp_getnext()



def pysnmp_snmpwalk(snmp_host, snmp_port, snmp_comm, snmp_oid):
    '''
    This is a net-snmp-utils's snmpwalk like function.
    And the output should be same as 'snmpwalk -Os'.
    '''

    dict_out = pysnmp_getnext(snmp_host, snmp_port, snmp_comm, snmp_oid, True)

    s_out = ''
    s_oid = snmp_oid_num2label(snmp_oid)
    s_valuetype = snmp_valuetype(s_oid)

    list_out = list()
    re_sub = re.sub

    for s_key in dict_out:

        s_value = dict_out[s_key]
        if s_valuetype == 'Timeticks':
            flt_days = float(s_value) / (86400 * 100)
            s_value = "(%s) %0.2f days" % (s_value, flt_days)
        if s_valuetype == '':
            s_valuetype = 'UNKNOWN'
        if s_oid == 'ifOperStatus':
            if s_value == '1':
                s_value = 'up(1)'
            if s_value == '2':
                s_value = 'down(2)'
        new_key = re_sub('^.*\.', '', s_key)
        new_key = "%s.%s" % (s_oid, new_key)
        s_out = "%s = %s: %s\n" % (new_key, s_valuetype, s_value)
        list_out.append(s_out)

    list_out.sort()
    return "".join(list_out).strip()
    #return s_out.strip()
    '''
    ifDescr.1 = STRING: GigabitEthernet0/1
    ifHCInOctets.1 = Counter64: 5563710
    '''
# End of pysnmp_snmpwalk()



def w_snmpwalk(snmp_ip, snmp_comm = '', snmp_oid = '', snmp_ver = '2c', datadir = '.', pysnmp = False, silent = False, singlefile = False, oldstyle = False):

    re_sub          = re.sub
    re_search       = re.search
    os_path_dirname = os.path.dirname
    os_path_exists  = os.path.exists

    # snmp_host - ip[:port]
    if snmp_ip.strip() == '':
        return False
    else:
        if len(re.findall(':', snmp_ip)) == 1:
            (snmp_host, snmp_port) = snmp_ip.split(':')
        else:
            snmp_host = re.sub(':.*$', '', snmp_ip)
            snmp_port = '161'

    # snmp_comm
    if snmp_comm.strip() == '':
        print("snmp comm could not be null.")
        return False

    # snmp_oid
    if snmp_oid.strip() == '':
        print("snmp oid could not be null.")
        return False

    # snmp_ver
    if re_search('^(1|2c|3)$', snmp_ver) == None:
        snmp_ver = '2c'

    # datadir
    if datadir.strip() == '':
        datadir = '.'

    # do snmpwalk
    if pysnmp:
        if not silent:
            print("[%s] pysnmpwalk -v %s -c %s %s:%s %s" % (w_time(), snmp_ver, snmp_comm, snmp_host, snmp_port, snmp_oid))
        data_out = pysnmp_snmpwalk(snmp_host, snmp_port, snmp_comm, snmp_oid)
    else:
        cmd_snmp = 'snmpwalk -Os -v %s -c %s %s:%s %s' % (snmp_ver, snmp_comm, snmp_host, snmp_port, snmp_oid)
        if not silent:
            print("[%s] %s" % (w_time(), cmd_snmp))
        data_out = sys_cmd(cmd_snmp)[0].strip()
    if data_out.strip() == '':
        return False

    s_time = w_time()

    # Write log to file
    for s_line in data_out.split("\n"):
        '''
        sysUpTimeInstance = Timeticks: (2138271723) 247 days, 11:38:37.23
        sysName.0 = STRING: BJ_XX_XXX_S5820_1180_1181
        ifDescr.1 = STRING: Ten-GigabitEthernet1/0/1
        ifHCInOctets.1 = Counter64: 279918467939157
        '''
        # oid
        if singlefile:
            s_oid = snmp_oid
        else:
            s_oid = re_sub(" =.*$", '', s_line)
            s_oid = re_sub("\.0$", '', s_oid)
        # for example: sysUpTimeInstance
        if s_oid != snmp_oid:
            if re_search("%s[0-9\.]+" % (snmp_oid), s_oid) == None:
                s_oid = snmp_oid
        if s_oid.strip() == '':
            continue

        # log format and filename
        if oldstyle:
            s_data = "%s, %s;\n" % (s_time, s_line)
            output_file = "%s/%s/%s#%s" % (datadir, snmp_host, snmp_host, s_oid)
            output_file = re_sub('\.0$', '', output_file)
        else:
            s_valuetype = snmp_valuetype(snmp_oid)
            if s_valuetype != '':
                s_data = "%s, %s\n" % (s_time, re_sub("^.*%s: " % (s_valuetype), '', s_line))
            else:
                s_data = "%s, %s\n" % (s_time, re_sub("^.* = ([0-9a-zA-Z:]+ )?", '', s_line))
            output_file = "%s/%s/%s" % (datadir, snmp_host, s_oid)

        # log path
        output_path = os_path_dirname(output_file)
        if not os_path_exists(output_path):
            try:
                sys_cmd('mkdir -p %s' % (output_path))
            except:
                print('[%s] %s:%s Error: mkdir %s failed!' % (w_time(), snmp_host, snmp_port, output_path))
                return False

        # write
        try:
            f_out = open(output_file, 'a')
            f_out.write(s_data)
            f_out.close()
        except:
            print('[%s] %s:%s Error: file %s is failed to write.' % (w_time(), snmp_host, snmp_port, output_file))
            return False

    return True

# End of w_snmpwalk()



if __name__ == '__main__':


    p = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter,
            description='''
  This is a multi-device snmpwalk program, it works like snmpwalk command of
  net-snmp project. So make sure you have installed snmpwalk before using it.
''',
            epilog='''

Example:

  %s --comm <YOUR_COMM> --ip 192.168.0.1
  %s --comm <YOUR_COMM> --datadir /var/log/snmp/%s/%s/ --ipfile ./ip.test --silent

                   ''' % (sys.argv[0], sys.argv[0], w_time('%Y'), w_time('%Y%m%d'))
        )

    p.add_argument("--ver",         type=str,   default="2c",  help="SNMP version, default is 2c")
    p.add_argument("--comm",        type=str,   default="",    help="SNMP community")
    p.add_argument("--port",        type=str,   default="161", help="SNMP UDP port, default is 161")
    p.add_argument("--datadir",     type=str,   default=".",   help='''The path where arp or mac data is stored, default is current directory
For example:
/var/log/snmp/$(date "+%%Y")/$(date "+%%Y%%m%%d")/
''')
    p.add_argument("--ip",          type=str,   help="ip[:port] list for snmp fetching")
    p.add_argument("--ipfile",      type=str,   help="A filename of ip[:port] list, --ip has higher priority than --ipfile")
    p.add_argument("--oid",         type=str,   help="OID list for snmpwalk")
    p.add_argument("--oidfile",     type=str,   help="A filename of oid list, --oid has higher priority than --oidfile")
    p.add_argument("--oldstyle",    action="store_true", help='''For compatible, use an old format to log.
Old Style:
    shell> cat /var/log/snmp/2015/20151123/172.17.54.1/172.17.54.1#ifHCInOctets.1
    2015-11-23 12:58:57, ifHCInOctets.1 = Counter64: 2799462542644320;
New Style:
    shell> cat /var/log/snmp/2015/20151123/172.17.54.1/ifHCInOctets.1
    12:58:57, 2799462542644320
''')
    p.add_argument("--pysnmp",      action="store_true", help="Use pysnmp module instead of snmpwalk command of net-snmp.")
    p.add_argument("--silent",      action="store_true", help="Silence mode.")
    p.add_argument("--singlefile",  action="store_true", help="If given then write all snmp output of one IP to single file.")
    p.add_argument("--max",         type=int,   default=1000,  help="The maximum threads/processes could be spread each time, default is 1000.")
    p.add_argument("--timeout",     type=int,   default=5,     help="Time to wait for command executing, default is 5 seconds.")
    p.add_argument("--process",   action="store_true", help="Use multi-process instead of multi-thread.")

    args = p.parse_args()

    # func_name
    func_name = w_snmpwalk

    # func_args
    func_args = list()

    # ip
    if args.ip:
        list_ip = args.ip.split(',')
    elif args.ipfile:
        if not os.path.exists(args.ipfile):
            print('%s does not exist, please specified host with --ip or --ipfile.\n' % (args.ipfile))
            sys.exit()
        f_ip = open(args.ipfile)
        list_ip = f_ip.readlines()
        f_ip.close()
    else:
        p.print_help()
        sys.exit()

    # snmp_oid
    if args.oid:
        list_oid = args.oid.split(',')
    elif args.oidfile:
        if not os.path.exists(args.oidfile):
            print('%s does not exist, please set host with --oid or --oidfile.\n' % (args.oidfile))
            sys.exit()
        f_oid = open(args.oidfile)
        list_oid = f_oid.readlines()
        f_oid.close()
    else:
        print('Please set host with --oid or --oidfile.\n')
        sys.exit()

    # pysnmp
    if args.pysnmp:
        from pysnmp.entity.rfc3413.oneliner import cmdgen

    # Prepare threding
    len_ip  = len(list_ip)
    len_oid = len(list_oid)
    for s_ip in list_ip:
        for s_oid in list_oid:
            func_args.append([s_ip.strip(), args.comm, s_oid.strip(), args.ver, args.datadir, args.pysnmp, args.silent, args.singlefile, args.oldstyle])
 
    if args.process:
        # Start multi-processing
        try:
            w_multiprocessing(func_name, func_args, args.max)
        except:
            print("Fail to run w_multiprocessing().")
            pass
    else:
        # Start multi-threading
        try:
            w_threading(func_name, func_args, args.max)
        except:
            print("Fail to run w_threading().")
            pass

    # Exit
    sys.exit()


