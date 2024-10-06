import datetime
import os
import sqlite3
import xlsxwriter


def connect_to_database():
    database_file = "database.db"
    try:
        connection = sqlite3.connect(f'file:{database_file}?mode=rw', uri=True, check_same_thread=False)
        return connection
    except sqlite3.Error:
        return None


def create_database():
    database_file = "database.db"
    try:
        connection = sqlite3.connect(database_file, check_same_thread=False)
        return connection
    except sqlite3.Error:
        return None


def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""create table if not exists networkRequest(
                            request_id INTEGER PRIMARY KEY,
                            flow_duration real,
                            Header_Length real,
                            Protocol_Type real,
                            Duration real,
                            Rate real,
                            Srate real,
                            Drate real,
                            fin_flag_number real,
                            syn_flag_number real,
                            rst_flag_number real,
                            psh_flag_number real,
                            ack_flag_number real,
                            ece_flag_number real,
                            cwr_flag_number real,
                            ack_count real,
                            syn_count	 real,
                            fin_count real,
                            urg_count real,
                            rst_count real,
                            HTTP real,
                            HTTPS real,
                            DNS real,
                            Telnet real,
                            SMTP real,
                            SSH real,
                            IRC real,
                            TCP real,
                            UDP real,
                            DHCP real,
                            ARP real,
                            ICMP real,
                            IPv real,
                            LLC real,
                            Tot_sum real,
                            Min real,
                            Max real,
                            AVG real,
                            Std real,
                            Tot_size real,
                            IAT real,
                            Number real,
                            Magnitue real,
                            Radius real,
                            Covariance real,
                            Variance real,
                            Weight real,
                            is_processed integer,
                            label_predicted text,
                            timestamp TEXT
                            );""")
        connection.commit()

    except Exception as e:
        print(e)
    finally:
        cursor.close()


def get_packets_count(connection, date):
    cursor = connection.cursor()
    try:
        cursor.execute("""
                SELECT 
                    COUNT(*) AS total_count,
                    COUNT(CASE WHEN label_predicted = 'Benign' THEN 1 END) AS count_valid_requests,
                    COUNT(CASE WHEN label_predicted != 'Benign' THEN 1 END) AS count_unvalid_requests
                FROM networkRequest
                WHERE date(timestamp) = ?
            """, (date,))
        counts = cursor.fetchone()
        return counts
    except sqlite3.Error:
        return None
    finally:
        cursor.close()


def insert_row(connection, packet):
    cursor = connection.cursor()
    try:

        # Insert the new packet into the networkRequest table
        cursor.execute("""
            INSERT INTO networkRequest (
                flow_duration, Header_Length, Protocol_Type, Duration, Rate, Srate, Drate,
                fin_flag_number, syn_flag_number, rst_flag_number, psh_flag_number, ack_flag_number,
                ece_flag_number, cwr_flag_number, ack_count, syn_count, fin_count, urg_count, rst_count,
                HTTP, HTTPS, DNS, Telnet, SMTP, SSH, IRC, TCP, UDP, DHCP, ARP, ICMP, IPv, LLC,
                Tot_sum, Min, Max, AVG, Std, Tot_size, IAT, Number, Magnitue, Radius, Covariance,
                Variance, Weight, is_processed, label_predicted, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                       ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            packet.flow_duration, packet.Header_Length, packet.Protocol_Type, packet.Duration,
            packet.Rate, packet.Srate, packet.Drate, packet.fin_flag_number, packet.syn_flag_number,
            packet.rst_flag_number, packet.psh_flag_number, packet.ack_flag_number, packet.ece_flag_number,
            packet.cwr_flag_number, packet.ack_count, packet.syn_count, packet.fin_count, packet.urg_count,
            packet.rst_count, packet.HTTP, packet.HTTPS, packet.DNS, packet.Telnet, packet.SMTP,
            packet.SSH, packet.IRC, packet.TCP, packet.UDP, packet.DHCP, packet.ARP, packet.ICMP,
            packet.IPv, packet.LLC, packet.Tot_sum, packet.Min, packet.Max, packet.AVG, packet.Std,
            packet.Tot_size, packet.IAT, packet.Number, packet.Magnitude, packet.Radius, packet.Covariance,
            packet.Variance, packet.Weight, 0, packet.label_predicted,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ))

        # Commit the changes to the database
        connection.commit()
        return cursor.lastrowid

    except sqlite3.Error as e:
        print("x::::" + str(e))
        return -1

    finally:
        cursor.close()


def generate_excel(packets, folder, filename):
    filename = os.path.join(folder, filename)
    if os.path.exists(filename):
        base_filename, extension = os.path.splitext(filename)
        count = 1
        while os.path.exists(filename):
            filename = f"{base_filename}_{count}{extension}"
            count += 1
        filename = os.path.join(folder, filename)

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    # Write some data headers.
    worksheet.write('A1', 'Request ID', bold)
    worksheet.write('B1', 'Flow Duration', bold)
    worksheet.write('C1', 'Header Length', bold)
    worksheet.write('D1', 'Protocol Type', bold)
    worksheet.write('E1', 'Duration', bold)
    worksheet.write('F1', 'Rate', bold)
    worksheet.write('G1', 'Srate', bold)
    worksheet.write('H1', 'Drate', bold)
    worksheet.write('I1', 'FIN Flag Number', bold)
    worksheet.write('J1', 'SYN Flag Number', bold)
    worksheet.write('K1', 'RST Flag Number', bold)
    worksheet.write('L1', 'PSH Flag Number', bold)
    worksheet.write('M1', 'ACK Flag Number', bold)
    worksheet.write('N1', 'ECE Flag Number', bold)
    worksheet.write('O1', 'CWR Flag Number', bold)
    worksheet.write('P1', 'ACK Count', bold)
    worksheet.write('Q1', 'SYN Count', bold)
    worksheet.write('R1', 'FIN Count', bold)
    worksheet.write('S1', 'URG Count', bold)
    worksheet.write('T1', 'RST Count', bold)
    worksheet.write('U1', 'HTTP', bold)
    worksheet.write('V1', 'HTTPS', bold)
    worksheet.write('W1', 'DNS', bold)
    worksheet.write('X1', 'Telnet', bold)
    worksheet.write('Y1', 'SMTP', bold)
    worksheet.write('Z1', 'SSH', bold)
    worksheet.write('AA1', 'IRC', bold)
    worksheet.write('AB1', 'TCP', bold)
    worksheet.write('AC1', 'UDP', bold)
    worksheet.write('AD1', 'DHCP', bold)
    worksheet.write('AE1', 'ARP', bold)
    worksheet.write('AF1', 'ICMP', bold)
    worksheet.write('AG1', 'IPv', bold)
    worksheet.write('AH1', 'LLC', bold)
    worksheet.write('AI1', 'Tot Sum', bold)
    worksheet.write('AJ1', 'Min', bold)
    worksheet.write('AK1', 'Max', bold)
    worksheet.write('AL1', 'AVG', bold)
    worksheet.write('AM1', 'STD', bold)
    worksheet.write('AN1', 'Tot Size', bold)
    worksheet.write('AO1', 'IAT', bold)
    worksheet.write('AP1', 'Number', bold)
    worksheet.write('AQ1', 'Magnitude', bold)
    worksheet.write('AR1', 'Radius', bold)
    worksheet.write('AS1', 'Covariance', bold)
    worksheet.write('AT1', 'Variance', bold)
    worksheet.write('AU1', 'Weight', bold)
    worksheet.write('AW1', 'Label Predicted', bold)
    worksheet.write('AX1', 'Timestamp', bold)

    # Start from the first cell. Rows and columns are zero indexed.
    row = 1
    col = 0

    # Iterate over the data and write it out row by row.
    for packet in packets:
        worksheet.write(row, col, packet['request_id'])
        worksheet.write(row, col + 1, packet['flow_duration'])
        worksheet.write(row, col + 2, packet['Header_Length'])
        worksheet.write(row, col + 3, packet['Protocol_Type'])
        worksheet.write(row, col + 4, packet['Duration'])
        worksheet.write(row, col + 5, packet['Rate'])
        worksheet.write(row, col + 6, packet['Srate'])
        worksheet.write(row, col + 7, packet['Drate'])
        worksheet.write(row, col + 8, packet['fin_flag_number'])
        worksheet.write(row, col + 9, packet['syn_flag_number'])
        worksheet.write(row, col + 10, packet['rst_flag_number'])
        worksheet.write(row, col + 11, packet['psh_flag_number'])
        worksheet.write(row, col + 12, packet['ack_flag_number'])
        worksheet.write(row, col + 13, packet['ece_flag_number'])
        worksheet.write(row, col + 14, packet['cwr_flag_number'])
        worksheet.write(row, col + 15, packet['ack_count'])
        worksheet.write(row, col + 16, packet['syn_count'])
        worksheet.write(row, col + 17, packet['fin_count'])
        worksheet.write(row, col + 18, packet['urg_count'])
        worksheet.write(row, col + 19, packet['rst_count'])
        worksheet.write(row, col + 20, packet['HTTP'])
        worksheet.write(row, col + 21, packet['HTTPS'])
        worksheet.write(row, col + 22, packet['DNS'])
        worksheet.write(row, col + 23, packet['Telnet'])
        worksheet.write(row, col + 24, packet['SMTP'])
        worksheet.write(row, col + 25, packet['SSH'])
        worksheet.write(row, col + 26, packet['IRC'])
        worksheet.write(row, col + 27, packet['TCP'])
        worksheet.write(row, col + 28, packet['UDP'])
        worksheet.write(row, col + 29, packet['DHCP'])
        worksheet.write(row, col + 30, packet['ARP'])
        worksheet.write(row, col + 31, packet['ICMP'])
        worksheet.write(row, col + 32, packet['IPv'])
        worksheet.write(row, col + 33, packet['LLC'])
        worksheet.write(row, col + 34, packet['Tot_sum'])
        worksheet.write(row, col + 35, packet['Min'])
        worksheet.write(row, col + 36, packet['Max'])
        worksheet.write(row, col + 37, packet['AVG'])
        worksheet.write(row, col + 38, packet['Std'])
        worksheet.write(row, col + 39, packet['Tot_size'])
        worksheet.write(row, col + 40, packet['IAT'])
        worksheet.write(row, col + 41, packet['Number'])
        worksheet.write(row, col + 42, packet['Magnitue'])
        worksheet.write(row, col + 43, packet['Radius'])
        worksheet.write(row, col + 44, packet['Covariance'])
        worksheet.write(row, col + 45, packet['Variance'])
        worksheet.write(row, col + 46, packet['Weight'])
        worksheet.write(row, col + 47, packet['label_predicted'])
        worksheet.write(row, col + 48, packet['timestamp'])
        row += 1

    workbook.close()

    return True


def get_all_packets_no_parts(conn_fast, attack_type, date):
    cursor = conn_fast.cursor()
    try:
        cursor.row_factory = sqlite3.Row
        if attack_type == "All":
            cursor.execute("SELECT * FROM networkRequest WHERE date(timestamp) = ? ORDER BY timestamp DESC", (date,))
        else:
            cursor.execute(
                "SELECT * FROM networkRequest WHERE label_predicted = ? AND date(timestamp) = ? ORDER BY timestamp DESC",
                (attack_type, date))
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error:
        return None
    finally:
        cursor.close()
