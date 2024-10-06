class NetworkPacket:
    def __init__(self, request_id=None, flow_duration=None, Header_Length=None,
                 Protocol_Type=None, Duration=None, Rate=None, Srate=None, Drate=None,
                 fin_flag_number=None, syn_flag_number=None, rst_flag_number=None,
                 psh_flag_number=None, ack_flag_number=None, ece_flag_number=None,
                 cwr_flag_number=None, ack_count=None, syn_count=None, fin_count=None,
                 urg_count=None, rst_count=None, HTTP=None, HTTPS=None, DNS=None, Telnet=None,
                 SMTP=None, SSH=None, IRC=None, TCP=None, UDP=None, DHCP=None, ARP=None,
                 ICMP=None, IPv=None, LLC=None, Tot_sum=None, Min=None, Max=None, AVG=None,
                 Std=None, Tot_size=None, IAT=None, Number=None, Magnitude=None, Radius=None,
                 Covariance=None, Variance=None, Weight=None, is_processed=None, label_predicted=None):
        self.request_id = request_id
        self.flow_duration = flow_duration
        self.Header_Length = Header_Length
        self.Protocol_Type = Protocol_Type
        self.Duration = Duration
        self.Rate = Rate
        self.Srate = Srate
        self.Drate = Drate
        self.fin_flag_number = fin_flag_number
        self.syn_flag_number = syn_flag_number
        self.rst_flag_number = rst_flag_number
        self.psh_flag_number = psh_flag_number
        self.ack_flag_number = ack_flag_number
        self.ece_flag_number = ece_flag_number
        self.cwr_flag_number = cwr_flag_number
        self.ack_count = ack_count
        self.syn_count = syn_count
        self.fin_count = fin_count
        self.urg_count = urg_count
        self.rst_count = rst_count
        self.HTTP = HTTP
        self.HTTPS = HTTPS
        self.DNS = DNS
        self.Telnet = Telnet
        self.SMTP = SMTP
        self.SSH = SSH
        self.IRC = IRC
        self.TCP = TCP
        self.UDP = UDP
        self.DHCP = DHCP
        self.ARP = ARP
        self.ICMP = ICMP
        self.IPv = IPv
        self.LLC = LLC
        self.Tot_sum = Tot_sum
        self.Min = Min
        self.Max = Max
        self.AVG = AVG
        self.Std = Std
        self.Tot_size = Tot_size
        self.IAT = IAT
        self.Number = Number
        self.Magnitude = Magnitude
        self.Radius = Radius
        self.Covariance = Covariance
        self.Variance = Variance
        self.Weight = Weight
        self.is_processed = is_processed
        self.label_predicted = label_predicted

    def __repr__(self):
        return f"Requests(request_id={self.request_id}, flow_duration={self.flow_duration}, " \
               f"Header_Length={self.Header_Length}, Protocol_Type={self.Protocol_Type}, " \
               f"Duration_Rate={self.Duration}, Rate={self.Rate}, Srate={self.Srate}, Drate={self.Drate}, " \
               f"fin_flag_number={self.fin_flag_number}, syn_flag_number={self.syn_flag_number}, " \
               f"rst_flag_number={self.rst_flag_number}, psh_flag_number={self.psh_flag_number}, " \
               f"ack_flag_number={self.ack_flag_number}, ece_flag_number={self.ece_flag_number}, " \
               f"cwr_flag_number={self.cwr_flag_number}, ack_count={self.ack_count}, " \
               f"syn_count={self.syn_count}, fin_count={self.fin_count}, urg_count={self.urg_count}, " \
               f"rst_count_HTTP={self.rst_count}, HTTP={self.HTTP}, HTTPS={self.HTTPS}, DNS={self.DNS}, " \
               f"Telnet={self.Telnet}, SMTP={self.SMTP}, SSH={self.SSH}, IRC={self.IRC}, " \
               f"TCP={self.TCP}, UDP={self.UDP}, DHCP={self.DHCP}, ARP={self.ARP}, " \
               f"ICMP={self.ICMP}, IPv={self.IPv}, LLC={self.LLC}, Tot_sum={self.Tot_sum}, " \
               f"Min={self.Min}, Max={self.Max}, AVG={self.AVG}, Std={self.Std}, Tot_size={self.Tot_size}, " \
               f"IAT={self.IAT}, Number={self.Number}, Magnitude={self.Magnitude}, Radius={self.Radius}, " \
               f"Covariance={self.Covariance}, Variance={self.Variance}, Weight={self.Weight}, " \
               f"is_processed={self.is_processed}, label_predicted={self.label_predicted})"

    def __getattr__(self, key):
        # if key exists in the object, return it
        if key in self.__dict__:
            return self.__dict__[key]
        # if not, return None
        return None
