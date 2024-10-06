# i mport RPI.GPIO

from Utils import DatabaseUtils as dbUtils
from Utils import PredictionUtils as predUtils
from Utils import SettingsUtils as setUtils
from Utils import StyleUtils as styleUtils
from Utils import SnifferUtils as snifferUtils
from Utils import EmailUtils as emailService
import streamlit.components.v1 as components
import streamlit as st
import threading
import datetime
import time
import sys
import os


def connect():
    connection = dbUtils.connect_to_database()
    if connection:
        return connection
    else:
        connection = dbUtils.create_database()
        if connection:
            dbUtils.create_table(connection)
            return connection
        else:
            sys.exit()


# LED_PIN = 18
# BUZZER_PIN = 23

# Initialize GPIO settings
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(LED_PIN, GPIO.OUT)
# GPIO.setup(BUZZER_PIN, GPIO.OUT)


    #def turn_on_alarm():
    # Turn on the LED and buzzer
    #GPIO.output(LED_PIN, GPIO.HIGH)
    #GPIO.output(BUZZER_PIN, GPIO.HIGH)
    #time.sleep(3)  # Keep the LED and buzzer on for 3 seconds
    #GPIO.output(LED_PIN, GPIO.LOW)
#GPIO.output(BUZZER_PIN, GPIO.LOW)


class WebUi:
    def __init__(self):
        self.conn = None
        self.model = None
        self.scaler = None
        self.settings = None
        self.emailService = None

        self.requests = []
        self.requests_count = 0
        self.bening_requests_count = 0
        self.attacks_count = 0

    def fill_data(self):
        attack_type = st.session_state.prediction_type if "prediction_type" in st.session_state else 'All'
        r_date = st.session_state.prediction_date if "prediction_date" in st.session_state else datetime.datetime.today().date()
        self.requests = dbUtils.get_all_packets_no_parts(self.conn, attack_type, r_date)
        counts = dbUtils.get_packets_count(self.conn, datetime.datetime.today().date())
        self.requests_count = counts[0]
        self.bening_requests_count = counts[1]
        self.attacks_count = counts[2]
        html_iframe = styleUtils.make_frame(styleUtils.make_divs(self.requests))
        return html_iframe

    def start(self):
        st.set_page_config(page_title="intrusion detection system", page_icon=":tada:")
        self.conn = connect()
        self.settings = setUtils.getSettings()
        self.emailService = emailService.EmailSender(self.settings)
        self.model = predUtils.load_cmodel(self.settings)
        self.scaler = predUtils.load_cscaler()

        st.markdown(styleUtils.whole_page_css(), unsafe_allow_html=True)
        st.sidebar.title("IDS Monitoring")

        spacing, prediction_type, spacing, time_picker, spacing, apply_button, spacing = st.columns(
            [1, 10, 3, 10, 1, 6, 3])

        prediction_type.selectbox("x",
                                  ['All', 'Benign', 'BruteForce', 'DDoS', 'DoS', 'Mirai', 'Recon', 'Spoofing', 'Web'],
                                  label_visibility='hidden', key="prediction_type")
        time_picker.date_input("x", value=datetime.datetime.today(), key="prediction_date", label_visibility='hidden')

        frame_container = st.empty()

        loading = st.empty()
        styleUtils.display_loading(loading)
        html_iframe = self.fill_data()

        with frame_container:
            components.html(html_iframe, height=500, scrolling=True)

        styleUtils.hide_loading(loading)

        st.sidebar.markdown(styleUtils.model_used(self.settings['machine_learnign_model']), unsafe_allow_html=True)

        container_request_count = st.sidebar.container()
        container_request_count.markdown(
            "<p class='count_container'></p><h3 class='count_container'>Requests count</h3>", unsafe_allow_html=True)
        container_request_count_c = st.sidebar.container().empty()
        container_request_count_c.write(self.requests_count)

        container_bening_requests = st.sidebar.container()
        container_bening_requests.markdown(
            "<p class='count_container'></p><h3 class='count_container'>Bening Requests</h3>", unsafe_allow_html=True)
        container_bening_requests_c = st.sidebar.container().empty()
        container_bening_requests_c.write(self.bening_requests_count)

        container_attacks_detected = st.sidebar.container()
        container_attacks_detected.markdown(
            "<p class='count_container'></p><h3 class='count_container'>Attacks detected</h3>", unsafe_allow_html=True)
        container_attacks_detected_c = st.sidebar.container().empty()
        container_attacks_detected_c.write(self.attacks_count)

        def generate_excel():
            attack_type = st.session_state.prediction_type if "prediction_type" in st.session_state else 'All'
            s_date = st.session_state.prediction_date if "prediction_date" in st.session_state else datetime.datetime.today().date()
            if os.name == 'nt':
                folder = self.settings['generated_excels_folder_windows']
            else:
                folder = self.settings['generated_excels_folder_linux']
            filename = f"report_{attack_type}_{s_date}.xlsx"
            packets = dbUtils.get_all_packets_no_parts(self.conn, attack_type, s_date)
            if packets is not None:
                prediction_thread = threading.Thread(target=dbUtils.generate_excel, args=(packets, folder, filename,))
                prediction_thread.start()

            # dbUtils.generate_excel(dbUtils.get_all_packets_no_parts(), folder, filename)

        st.sidebar.button("Generate excel", on_click=generate_excel, use_container_width=True)

        while True:
            packet = snifferUtils.sniff_packet()
            if packet is None:
                continue
            prediction = predUtils.predict_type(self.model, self.scaler, packet)
            packet.label_predicted = prediction
            packet.request_id = dbUtils.insert_row(self.conn, packet)
            if packet.request_id is not None:
                self.requests_count += 1
                self.bening_requests_count += 1 if packet.label_predicted == 'Benign' else 0
                self.attacks_count += 1 if packet.label_predicted != 'Benign' else 0

                container_request_count_c.write(self.requests_count)
                container_bening_requests_c.write(self.bening_requests_count)
                container_attacks_detected_c.write(self.attacks_count)
                # if packet is not Benign send email
                if packet.label_predicted != 'Benign':
                    self.emailService.send_alert(datetime.datetime.now(), packet.label_predicted)
                    # turn_on_alarm()
                    should_turn_off = self.settings['turn_off_network_on_attack_detection']
                    if should_turn_off:
                        network_interface = self.settings['network_interface']
                        os.system(f"ifconfig {network_interface} down")

            time.sleep(self.settings['time_between_sniffed_packet'])


if __name__ == '__main__':
    web_ui = WebUi()
    web_ui.start()
