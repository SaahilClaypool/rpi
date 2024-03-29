from pcapfile import savefile
from pcapfile.protocols.linklayer import ethernet
from pcapfile.protocols.network import ip
from pcapfile.protocols.transport import tcp
import binascii
import matplotlib.pyplot as plt
import re
from functools import reduce
import time

"""
Usage:
> pip3 install pypcapfile
"""

def main():
    testcap = open('./sample_pcap.pcap', 'rb')

    capfile = savefile.load_savefile(testcap, verbose=True)

    sender_src = re.compile(f"192.168.2..")
    sender_dst = re.compile(f"192.168.1..")

    goodput_per_packet(capfile.packets, sender_src, sender_dst)
    
def parse(packet) -> (ethernet.Ethernet, ip.IP, tcp.TCP):
    eth_frame: ethernet.Ethernet = ethernet.Ethernet(packet.raw())
    ip_packet: ip.IP = ip.IP(binascii.unhexlify(eth_frame.payload))
    tcp_pkt: tcp.TCP = tcp.TCP(binascii.unhexlify(ip_packet.payload))
    return eth_frame, ip_packet, tcp_pkt

def packet_len(packet) -> int:
    (eth_f, ip_p, tcp_p) = parse(packet)
    return ip_p.len - ip_p.hl * 4- tcp_p.data_offset

# returns througput in bytes per second for each packet
# bytes recieved
def goodput_per_packet(packets, sender_src, sender_dst) -> list((any, int)):
    """
    calculate the bytes received after each packet arrives

    Each time packet arrives, add data (recieved amount, time)
    """
    acked_data = [] # list of (bytes, time)
    _limit = -100
    for idx, packet in enumerate(packets):
        (eth_f, ip_p, tcp_p) = parse(packet)
        pkt_dst = ip_p.dst.decode("utf-8")
        pkt_src = ip_p.src.decode("utf-8")

        bytes_received = 0
        if (tcp_p.syn and tcp_p.ack):
            # restart flow
            print("restart at ", idx)
            acked_data = []
            _limit = -100

        if (sender_src.match(pkt_src)): # if the packet is arriving at the client
            bytes_received += packet_len(packet)
            acked_data.append((bytes_received, packet.timestamp_ms))

            
        if (sender_src.match(pkt_dst)): # packet is leaving the client
            pass

        _limit -= 1
        if (_limit == 0):
            break
    
    t_bottom = 0
    t_top = 0
    data = []
    acked_data.sort(key=lambda v: v[1])
    print(f"analyzing: {len(acked_data)} packets")
    ind_bottom = 0
    ind_top = 0
    gran = 0.3
    idx = 0
    for ad in acked_data:
        t_top = ad[1]
        t_bottom = t_top - 1000 * gran

        ind_bottom = first_index(\
        lambda v: v[1] > t_bottom, acked_data, start=ind_bottom)

        ind_top = first_index(\
        lambda v: v[1] >= t_top, acked_data, start=ind_top)

        throughput = 0
        print(f"i: {idx}, checking, {ind_top - ind_bottom} {ind_top} {ind_bottom} {t_top} {t_bottom}")
        idx += 1
        for i in range(ind_top, ind_bottom):
            throughput += acked_data[i][0]
        throughput /= gran

        data.append((ad[1], throughput))
    plot_data(data)

def first_index(cond, l, start=0):
    """
    return first index where condition f is true
    -1 on failure
    """
    for i, v in enumerate(l[start:]):
        if (cond(v)):
            return i
    return -1


def plot_data(data):
    data.sort(key=lambda x: x[0])
    x = [i for i in map(lambda x1: x1[0], data)]
    y = [i for i in map(lambda x1: x1[1], data)]
    
    plt.plot(x, y)
    plt.ticklabel_format(style='sci', axis='y',  scilimits=(0,0))
    plt.show()

if __name__ == '__main__':
    main()
