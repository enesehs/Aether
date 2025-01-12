"""
86868686 86    86 86868686  868686  86868686 86     86  868686  
86       86#   86 86       86    86 86       86     86 86    86 
86       8686  86 86       86       86       86     86 86       
868686   86 86 86 868686    868686  868686   86868686#  868686  
86       86  8686 86             86 86       86     86       86 
86       86   86# 86       86    86 86       86     86 86    86 
86868686 86    86 86868686  868686  86868686 86     86  868686       

Author: enesehs
Email: enesehs@protonmail.com
Website: https://www.enesehs.me
Version: 0.1 Pre-Alpha
Script: Capture.py
Builder: pyinstaller
Build Command: pyinstaller --onefile -w --icon=img/small.ico 'Capture.py'
License: GNU General Public License v3.0
"""

import cv2
import os
from datetime import datetime
import logging
import py7zr
import configparser
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open('settings.key', 'wb') as key_file:
        key_file.write(key)

def encrypt_password(password):
    if not os.path.exists('settings.enc'):
        with open('settings.key', 'rb') as key_file:
            key = key_file.read()
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode())
        with open('settings.enc', 'wb') as enc_file:
            enc_file.write(encrypted_password)

def decrypt_password():
    with open('settings.key', 'rb') as key_file:
        key = key_file.read()
    with open('settings.enc', 'rb') as enc_file:
        encrypted_password = enc_file.read()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password).decode()

config = configparser.ConfigParser()
config.read('settings.ini')

save_dir = config.get('Settings', 'savelocation', fallback=r'D:\Users\%USERNAME%\Desktop\Captures')
selected_camera = config.getint('Settings', 'selectedcamera', fallback=0)
autostart = config.getboolean('Settings', 'autostart', fallback=True)
encryption = config.getboolean('Settings', 'encryption', fallback=True)
compress = config.getboolean('Settings', 'compress', fallback=True)
logging_enabled = config.getboolean('Settings', 'logging', fallback=True)

password = decrypt_password()

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

if logging_enabled:
    log_filename = os.path.join(save_dir, 'capture_log.txt')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_filename)

def capture_photo():
    if logging_enabled:
        logging.info("Starting camera.")
    try:
        cap = cv2.VideoCapture(selected_camera)
        
        if not cap.isOpened():
            if logging_enabled:
                logging.error("Failed to open camera.")
            return
        
        if logging_enabled:
            logging.info("Camera opened successfully.")
        
        ret, frame = cap.read() 
        
        if ret:
            if logging_enabled:
                logging.info("Frame captured successfully.")
            
            filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.png'
            filepath = os.path.join(save_dir, filename)
            
            cv2.imwrite(filepath, frame)
            if logging_enabled:
                logging.info(f"Photo saved to {filepath}.")
            
            if compress:
                if os.path.exists(filepath):
                    archive_name = os.path.join(save_dir, 'captures_archive.7z')
                    normalized_path = os.path.normpath(filepath)
                    compress_and_encrypt_photos(normalized_path, archive_name, password)
                else:
                    if logging_enabled:
                        logging.error(f"File not found: {filepath}")
        else:
            if logging_enabled:
                logging.error("Failed to capture photo.")
    except Exception as e:
        if logging_enabled:
            logging.error(f"Unexpected error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if logging_enabled:
            logging.info("Camera and all windows closed.")

def compress_and_encrypt_photos(file_path, archive_name, password):
    if os.path.exists(archive_name):
        mode = 'a'
    else:
        mode = 'w'

    with py7zr.SevenZipFile(archive_name, mode, password=password) as archive:
        archive.write(file_path, os.path.basename(file_path))
    
    if logging_enabled:
        logging.info(f"Photo saved and encrypted: {archive_name}")

    os.remove(file_path)
    if logging_enabled:
        logging.info(f"Original photo deleted: {file_path}")



if __name__ == "__main__":
    try:
        capture_photo()
        if logging_enabled:
            logging.info("Exiting...")
    finally:
        logging.shutdown()

