# 📚 1차

DHT11 온습도 두 값의 측정·표시·PC 기록을 연결합니다.

## 🔎 확인할 자료

- [주요 근거 파일](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/dht_lcd_rgb_csv/dht_lcd_rgb_csv.ino) · `DHT`
- [전체 차수와 파일 집계](../VERSIONS.md)
- [프로젝트 소개](../../README.md)

## 🧭 실험 조건

PC 수집기는 코드/1차/pc_csv_logger.py에 있습니다.


## 🧩 주요 내용

- DHT 온습도 읽기와 LCD·RGB 표시를 수행하는 Arduino 스케치입니다.
- COM3·9600 baud 기본값으로 두 필드를 받아 PC 시각과 함께 dht_log.csv에 추가합니다. 두 필드 개수 검사만 있고 최종판의 숫자·빈칸 검사는 없습니다.

## 🔄 자료 구성

온습도 두 필드가 최종의 일곱 센서 필드로 확장되는 출발점입니다.

## 📍 관련 자료

- [코드/1차/dht_lcd_rgb_csv/dht_lcd_rgb_csv.ino](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/dht_lcd_rgb_csv/dht_lcd_rgb_csv.ino) · `void loop` · 38
- [코드/1차/pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py) · `len(parts) == 2` · 22

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다. 
