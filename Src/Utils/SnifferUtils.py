import statistics
import numpy as np
from scapy.all import *
from scapy.layers.inet import TCP, IP
from Models.NetworkPacket import NetworkPacket as networkPacket

previous_packet_time = 0
packet_lengths = []
packet_times = []
flag_counts = {'FIN': 0, 'SYN': 0, 'RST': 0, 'PSH': 0, 'ACK': 0, 'URG': 0}
protocol_counts = {'HTTP': 0, 'HTTPS': 0, 'DNS': 0, 'Telnet': 0, 'SMTP': 0, 'SSH': 0, 'IRC': 0, 'TCP': 0, 'UDP': 0,
                   'DHCP': 0, 'ARP': 0, 'ICMP': 0, 'IPv': 0, 'LLC': 0}


def process_packet(sniffed_packet):
    global previous_packet_time, packet_lengths, packet_times, flag_counts, protocol_counts

    # Update packet times
    packet_times.append(sniffed_packet.time)
    iat = packet_times[-1] - packet_times[-2] if len(packet_times) > 1 else 0

    # Update packet lengths
    packet_lengths.append(len(sniffed_packet))
    # tot_sum = sum(packet_lengths)
    # minimum = min(packet_lengths)
    # maximum = max(packet_lengths)
    # average = tot_sum / len(packet_lengths)
    # std = statistics.stdev(packet_lengths) if len(packet_lengths) > 1 else 0

    # Update flag counts
    if sniffed_packet.haslayer(TCP):
        tcp = sniffed_packet[TCP]
        for flag in flag_counts.keys():
            if flag in str(tcp.flags):
                flag_counts[flag] += 1

    # Update protocol counts
    for protocol in protocol_counts.keys():
        if sniffed_packet.haslayer(protocol):
            protocol_counts[protocol] += 1

    flow_duration = packet_times[-1] - packet_times[0]
    header_length = sniffed_packet[IP].ihl * 4 if sniffed_packet.haslayer(IP) else 0
    protocol_type = sniffed_packet[IP].proto if sniffed_packet.haslayer(IP) else 0
    duration = iat
    rate = len(sniffed_packet) / iat if iat != 0 else 0
    srate = len(sniffed_packet[IP].src) / iat if sniffed_packet.haslayer(IP) and iat != 0 else 0
    drate = len(sniffed_packet[IP].dst) / iat if sniffed_packet.haslayer(IP) and iat != 0 else 0
    fin_flag_number = flag_counts['FIN'] if 'FIN' in flag_counts.keys() else 0
    syn_flag_number = flag_counts['SYN'] if 'SYN' in flag_counts.keys() else 0
    rst_flag_number = flag_counts['RST'] if 'RST' in flag_counts.keys() else 0
    psh_flag_number = flag_counts['PSH'] if 'PSH' in flag_counts.keys() else 0
    ack_flag_number = flag_counts['ACK'] if 'ACK' in flag_counts.keys() else 0
    ece_flag_number = flag_counts['URG'] if 'URG' in flag_counts.keys() else 0
    cwr_flag_number = flag_counts['CWR'] if 'CWR' in flag_counts.keys() else 0
    ack_count = protocol_counts['ACK'] if 'ACK' in protocol_counts.keys() else 0
    syn_count = protocol_counts['SYN'] if 'SYN' in protocol_counts.keys() else 0
    fin_count = protocol_counts['FIN'] if 'FIN' in protocol_counts.keys() else 0
    urg_count = protocol_counts['URG'] if 'URG' in protocol_counts.keys() else 0
    rst_count = protocol_counts['RST'] if 'RST' in protocol_counts.keys() else 0
    http = protocol_counts['HTTP'] if 'HTTP' in protocol_counts.keys() else 0
    https = protocol_counts['HTTPS'] if 'HTTPS' in protocol_counts.keys() else 0
    dns = protocol_counts['DNS'] if 'DNS' in protocol_counts.keys() else 0
    telnet = protocol_counts['Telnet'] if 'Telnet' in protocol_counts.keys() else 0
    smtp = protocol_counts['SMTP'] if 'SMTP' in protocol_counts.keys() else 0
    ssh = protocol_counts['SSH'] if 'SSH' in protocol_counts.keys() else 0
    irc = protocol_counts['IRC'] if 'IRC' in protocol_counts.keys() else 0
    tcp = protocol_counts['TCP'] if 'TCP' in protocol_counts.keys() else 0
    udp = protocol_counts['UDP'] if 'UDP' in protocol_counts.keys() else 0
    dhcp = protocol_counts['DHCP'] if 'DHCP' in protocol_counts.keys() else 0
    arp = protocol_counts['ARP'] if 'ARP' in protocol_counts.keys() else 0
    icmp = protocol_counts['ICMP'] if 'ICMP' in protocol_counts.keys() else 0
    ipv = protocol_counts['IPv'] if 'IPv' in protocol_counts.keys() else 0
    llc = protocol_counts['LLC'] if 'LLC' in protocol_counts.keys() else 0
    tot_sum = sum(packet_lengths)
    minimum = min(packet_lengths)
    maximum = max(packet_lengths)
    average = tot_sum / len(packet_lengths)
    std = statistics.stdev(packet_lengths) if len(packet_lengths) > 1 else 0
    tot_size = len(sniffed_packet)
    iat = packet_times[-1] - packet_times[0]
    number = len(packet_lengths)
    magnitude = math.sqrt(sum(i ** 2 for i in packet_lengths))
    radius = statistics.stdev(packet_lengths) if len(packet_lengths) > 1 else 0
    covariance = np.cov(packet_lengths, packet_times)[0, 1] if len(packet_lengths) > 1 else 0
    variance = statistics.variance(packet_lengths) if len(packet_lengths) > 1 else 0
    weight = 1

    return networkPacket(request_id=None, flow_duration=flow_duration, Header_Length=header_length,
                         Protocol_Type=protocol_type, Duration=duration, Rate=rate, Srate=srate, Drate=drate,
                         fin_flag_number=fin_flag_number, syn_flag_number=syn_flag_number,
                         rst_flag_number=rst_flag_number, psh_flag_number=psh_flag_number,
                         ack_flag_number=ack_flag_number, ece_flag_number=ece_flag_number,
                         cwr_flag_number=cwr_flag_number, ack_count=ack_count, syn_count=syn_count, fin_count=fin_count,
                         urg_count=urg_count, rst_count=rst_count, HTTP=http, HTTPS=https, DNS=dns, Telnet=telnet,
                         SMTP=smtp, SSH=ssh, IRC=irc, TCP=tcp, UDP=udp, DHCP=dhcp, ARP=arp, ICMP=icmp, IPv=ipv, LLC=llc,
                         Tot_sum=tot_sum, Min=minimum, Max=maximum, AVG=average, Std=std, Tot_size=tot_size, IAT=iat,
                         Number=number, Magnitude=magnitude, Radius=radius, Covariance=covariance, Variance=variance,
                         Weight=weight, is_processed=None, label_predicted=None)


def sniff_packet():
    try:
        sniffed_network = sniff(count=1)
        single_packet = sniffed_network[0]
        processed_packet = process_packet(single_packet)
        return processed_packet
    except Exception as ignored:
        return None
