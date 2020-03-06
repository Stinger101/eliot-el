# A simple script to add delay or packet loss to the docker interface used
# by ELIoT. The tc commands for some reason seems to ignore UDP and won't
# work in current state. A soultion might be to add a filter and to drop
# packets or add delay to packets going to or from the leshan server.

import os
import sys
import argparse

# Add parser
parser = argparse.ArgumentParser(description="""Add network features to simulate
        delay or packet drop to docker interface""")

# Add arguments tc-delay-ms, tc-delay-gauss, tc-dropn, tc-remove,  iptables-dropn, iptables-remove
parser.add_argument('-t', '--tc', help='Use traffic control (tc)', action="store_true")
parser.add_argument('-i', '--iptables', help='Use iptables (drop packets only)', action="store_true")
#parser.add_argument('--tc-delay-ms', metavar='ms', type=int, nargs=1)

args = parser.parse_args()

print("""Simple script to add delay or packet loss to docker interface. 
use network_manip -h to see options""")

if args.tc:
    #this adds 10 sec to all packets
    com_del_uni="sudo tc qdisc add dev br-$(docker network ls | grep eliot-el_default | awk '{print $1}') root handle 1:0 netem delay 10000msec"
    # this adds Gausssian delay with mean of 100 and std of 50 to packets
    com_del_nor="sudo tc qdisc add dev br-$(docker network ls | grep eliot-el_default | awk '{print $1}') root netem delay 100ms 50ms distribution normal"
    #this drops 5% of packets
    com_los_cor="sudo tc qdisc add dev br-$(docker network ls | grep eliot-el_default | awk '{print $1}') root netem loss 90% 25%"
    #this removes a loss or delay rule.
    com_ev_del="sudo tc qdisc del dev br-$(docker network ls | grep eliot-el_default | awk '{print $1}') root"

    try:
        action=int(input("Action (0:Delay-uni, 1: Delay-nor, 2: Los-cor, 3: No-rule):"))

        if action==0:
            r=os.system(com_del_uni)
            if(r == 0):
                print('Network is now with delay-uni')
        elif action==1:
            r=os.system(com_del_nor)
            if(r == 0):
                print('Network is now with delay-nor')
        elif action==2:
            r=os.system(com_los_cor)
            if(r == 0):
                print('Network is now with los-cor')
        elif action==3:
            r=os.system(com_ev_del)
            if(r == 0):
                print('Network is now with no delay-loss')
        else:
            print('Unvalid input. Exiting...')

    except ValueError:
        print('Unvalid input. Exiting...')

elif args.iptables:
    action=int(input("Action (0: Add UDP packet drop, 1: Remove packet drop): "))

    if action==0:
        n=input("Probability of UDP packets being dropped (0-1)")
        # Drop packets going from the leshan server with the probability of n
        ip_drop_n_add_rule='''sudo iptables -I FORWARD -p udp -s $(docker inspect \
                            -f '{{{{range .NetworkSettings.Networks}}}}{{{{.IPAddress}}}}{{{{end}}}}' \
                            eliot-el_ms_1) -m statistic --mode random --probability {} -j \
                            DROP'''.format(n)
        r=os.system(ip_drop_n_add_rule)
        if r==0:
            msg="Dropping {:.0%} of all UDP packets".format(float(n))
            print(msg)


    else:
        # Remove rule to drop packets from iptables
        ip_tables_n_rm_rule='''sudo iptables -D FORWARD $(sudo iptables --list \
                            FORWARD --line-numbers | grep $(docker inspect -f '{{range \
                            .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
                            eliot-el_ms_1) | awk '{print $1}')'''
        r=os.system(ip_tables_n_rm_rule)
        if r==0:
            msg="Removing rule from table"
            print(msg)

