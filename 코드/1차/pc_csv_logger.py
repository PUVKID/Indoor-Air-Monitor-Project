import serial
import csv
from datetime import datetime

PORT = "COM3"        # 환경에 맞게 변경 (Mac/Linux는 예: /dev/ttyUSB0, /dev/cu.usbmodemXXXX)
BAUD = 9600
OUTPUT_FILE = "dht_log.csv"

ser = serial.Serial(PORT, BAUD, timeout=2)

with open(OUTPUT_FILE, "a", newline="") as f:
    writer = csv.writer(f)
    if f.tell() == 0:
        writer.writerow(["timestamp", "temperature_C", "humidity_%"])

    print(f"{OUTPUT_FILE}에 저장을 시작합니다. (Ctrl+C로 종료)")
    try:
        while True:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if "," in line:
                parts = line.split(",")
                if len(parts) == 2:
                    temp, humi = parts
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    writer.writerow([timestamp, temp, humi])
                    f.flush()
                    print(timestamp, temp, humi)
    except KeyboardInterrupt:
        print("종료합니다.")
    finally:
        ser.close()
