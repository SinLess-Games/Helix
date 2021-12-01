import os
import yaml
import logging
import sentry_sdk
from datetime import datetime

sentry_sdk.init(
    "https://fe349234191e4e86a83c8cd381068ab4@o901570.ingest.sentry.io/5994911",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

logging.basicConfig(filename=f"Logs/Scan_{datetime.today().strftime('%m-%d-%Y')}_log.txt", encoding='utf-8', level=logging.DEBUG)
logging.info("Starting system scan for programs. This may take a few minutes.")

drives = ["A:\\", "B:\\", "C:\\", "D:\\", "E:\\",
          "F:\\", "G:\\", "H:\\", "I:\\", "J:\\", "L:\\"]

system_file = []
for value in yaml.safe_load(open('system_files.yaml', 'r')):
    system_file.append(value)


def scan_file_exe():
    for drive in drives:
        logging.info("Searching in drive: " + f"'{drive}'")
        # print("\33[32m Searching in drive: " + f"'{drive}'")
        dir_path = drive

        for root, dirs, files in os.walk(dir_path):
            back = '\\'
            global directory
            for file in files:
                program = file
                directory = root + back + program
            if any(ele in directory for ele in system_file):
                # print("\033[93m " + root)
                # logging.warning("SYSTEM FILE LOCATION DETECTED!!!!!!!")
                # print("\033[93m SYSTEM FILE LOCATION DETECTED!!!!!!!  " + root)
                continue

            for file in files:
                # print("File path: " + f"'{root + back + str(file)}'")
                program = file
                path = root + back + str(file)
                # print(path)
                if file.endswith('.exe'):
                    logging.info("Adding path: " + path)
                    # print("\033[92m Adding path: " + path)

                    with open('programs.yaml', 'r') as yaml_file:
                        cur_yaml = yaml.safe_load(yaml_file)
                        info = {f'{program[:-4]}': f' {path}'}
                        # print("YAML data: " + f"'{info}'")
                        cur_yaml.update(info)
                        # print(cur_yaml)
                    if cur_yaml:
                        with open('programs.yaml', 'w') as yaml_file:
                            yaml.safe_dump(cur_yaml, yaml_file)
                else:
                    break


if __name__ == "__main__":
    scan_file_exe()
