import pickle
import threading
import numpy
import pandas

import os
import warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings("ignore")
from tensorflow import keras

current_directory = os.path.abspath(os.getcwd())
subdirectory = "prediction_models"
full_path = os.path.join(current_directory, subdirectory)

machine_learnign_model = None


def load_cmodel(env):
    try:
        global machine_learnign_model
        machine_learnign_model = env['machine_learnign_model']
        if machine_learnign_model == 'deep_learning':
            # return keras.models.load_model(full_path + '\\deep_learning_model.h5')
            return keras.models.load_model(full_path + '\\deep_learning_model_v3.keras')
        elif machine_learnign_model == 'logistic_regression':
            with open(full_path + '\\logisticRegression_v2.pkl', 'rb') as model:
                return pickle.load(model)
    except pickle.UnpicklingError:
        return None


def load_cscaler():
    try:
        with open(full_path + '\\standarScaler.pkl', 'rb') as scaler:
            return pickle.load(scaler)
    except pickle.UnpicklingError:
        return None


columns = [
    'flow_duration', 'Header_Length', 'Protocol Type', 'Duration',
    'Rate', 'Srate', 'Drate', 'fin_flag_number', 'syn_flag_number',
    'rst_flag_number', 'psh_flag_number', 'ack_flag_number',
    'ece_flag_number', 'cwr_flag_number', 'ack_count',
    'syn_count', 'fin_count', 'urg_count', 'rst_count',
    'HTTP', 'HTTPS', 'DNS', 'Telnet', 'SMTP', 'SSH', 'IRC', 'TCP',
    'UDP', 'DHCP', 'ARP', 'ICMP', 'IPv', 'LLC', 'Tot sum', 'Min',
    'Max', 'AVG', 'Std', 'Tot size', 'IAT', 'Number', 'Magnitue',
    'Radius', 'Covariance', 'Variance', 'Weight',
]

label_dict = {
    0: 'Benign',
    1: 'BruteForce',
    2: 'DDoS',
    3: 'DoS',
    4: 'Mirai',
    5: 'Recon',
    6: 'Spoofing',
    7: 'Web'}


def predict_type(model, scaler, packet):
    prediction_thread = threading.Thread(target=process_prediction, args=(packet, model, scaler))
    prediction_thread.start()
    prediction_thread.join()
    return packet.label_predicted


def process_prediction(packet, model, scaler):
    prediction_result = perform_prediction(packet, model, scaler)
    packet.label_predicted = prediction_result


def perform_prediction(packet, model, scaler):
    df = pandas.DataFrame([[packet.flow_duration, packet.Header_Length, packet.Protocol_Type, packet.Duration,
                            packet.Rate, packet.Srate, packet.Drate, packet.fin_flag_number, packet.syn_flag_number,
                            packet.rst_flag_number, packet.psh_flag_number, packet.ack_flag_number,
                            packet.ece_flag_number, packet.cwr_flag_number, packet.ack_count, packet.syn_count,
                            packet.fin_count, packet.urg_count, packet.rst_count, packet.HTTP, packet.HTTPS,
                            packet.DNS, packet.Telnet, packet.SMTP, packet.SSH, packet.IRC, packet.TCP, packet.UDP,
                            packet.DHCP, packet.ARP, packet.ICMP, packet.IPv, packet.LLC, packet.Tot_sum,
                            packet.Min,
                            packet.Max, packet.AVG, packet.Std, packet.Tot_size, packet.IAT,
                            packet.Number, packet.Magnitude, packet.Radius, packet.Covariance, packet.Variance,
                            packet.Weight]], columns=columns)

    scalled = scaler.transform(df)
    if machine_learnign_model == 'logistic_regression':
        prediction = model.predict(scalled)
    else:
        prediction = model.predict(scalled, verbose=0)
    prediction = numpy.argmax(prediction)
    df['label'] = label_dict[prediction]
    return label_dict[prediction]
    # return "DDOS"
