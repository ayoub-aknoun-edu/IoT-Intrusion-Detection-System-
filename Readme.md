# IoT Intrusion Detection System (IDS)

## Overview

This project is an Intrusion Detection System (IDS) designed for IoT networks. It uses machine learning models to detect potential security threats and provides a web-based user interface for monitoring and managing network security. The system is deployed on a Raspberry Pi 4 and utilizes a network sniffer to analyze network traffic in real-time.

## Prerequisites

- Raspberry Pi 4
- Micro SD card (16GB or more)
- Micro SD card reader
- Computer with internet connection
- Keyboard
- Mouse
- Monitor
- HDMI cable
- Power supply
- Python 3.11
- Required Python packages (listed in `requirements.txt`)

## Installation

### Setup Raspberry Pi OS

1. Go to the [Raspberry Pi OS download page](https://downloads.raspberrypi.org/imager/imager_latest.exe) and download the Raspberry Pi OS image.
2. Insert the Micro SD card into the Micro SD card reader and connect it to the computer.
3. Open the Raspberry Pi Imager and select the Raspberry Pi OS image you downloaded.
4. Select the Micro SD card you inserted.
5. Click on "Write" and wait until the process is finished.
6. Insert the Micro SD card into the Raspberry Pi.
7. Connect the keyboard, mouse, monitor, and power supply to the Raspberry Pi.
8. Turn on the Raspberry Pi.
9. Follow the instructions on the screen to configure the Raspberry Pi.
10. When the Raspberry Pi OS desktop appears, open a terminal and run the following commands:
    ```sh
    sudo apt update
    sudo apt upgrade
    ```

### Setup the IDS Project

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/iot-ids.git
    cd iot-ids
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Copy the example environment configuration file and update it with your settings:
    ```sh
    cp Src/env.json.example Src/env.json
    ```

5. Edit `Src/env.json` to configure the environment settings.

## Usage

1. Run the IDS system:
    ```sh
    python Src/system.py
    ```

2. Access the web UI at `http://localhost:8501`.

## Configuration

The configuration file `Src/env.json` contains various settings:

- **machine_learnign_model**: Specify either 'logistic_regression' or 'deep_learning'.
- **email_alerts**: Configuration for email alerts.
- **time_between_sniffed_packet**: Time between each packet sniffed in seconds.
- **turn_off_network_on_attack_detection**: Boolean to turn off the network interface on attack detection.
- **network_interface**: Network interface to monitor.
- **generated_excels_folder_windows**: Folder path for generated Excel reports on Windows.
- **generated_excels_folder_linux**: Folder path for generated Excel reports on Linux.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please contact [a.akanoun@edu.umi.ac.ma](mailto:a.akanoun@edu.umi.ac.ma).