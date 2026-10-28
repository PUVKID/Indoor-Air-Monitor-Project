# 📚 최종

AM1008W-K를 더해 일곱 센서 값과 세 LCD 화면·종합 RGB 등급을 구성합니다.

## 🔎 확인할 자료

- [주요 근거 파일](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/%EC%95%84%EB%91%90%EC%9D%B4%EB%85%B8%20%EC%BD%94%EB%93%9C/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino) · `AM1008`
- [전체 차수와 파일 집계](../VERSIONS.md)
- [프로젝트 소개](../../README.md)

## 🧭 실험 조건

최종 수집기는 형식 검사와 시간 기록을 포함합니다. 센서·배선과 라이브러리를 준비한 뒤 실행합니다.


## 🧩 주요 내용

- DHT에 AM1008W 온습도·CO₂·VOC·PM2.5를 추가하여 LCD 순환 표시와 센서별 위험 등급을 종합합니다.
- parse_line이 일곱 필드의 숫자 또는 빈칸 여부를 검사합니다. 일부 센서 실패는 빈칸으로 남기고 전부 빈 행은 제외합니다.
- 포트 기본값은 COM4로 바뀌고 air_log.csv를 UTF-8로 저장합니다. PC 수신 시각을 앞에 붙여 총 여덟 열을 기록합니다.

## 🔄 자료 구성

센서 두 필드→일곱 필드, 단순 열 개수 검사→값 형식 검사, dht_log.csv→air_log.csv로 바뀝니다. 기존 CSV를 덮어쓰는 마이그레이션은 아닙니다.

## 📍 관련 자료

- [코드/최종/아두이노 코드/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/%EC%95%84%EB%91%90%EC%9D%B4%EB%85%B8%20%EC%BD%94%EB%93%9C/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino) · `void loop` · 183
- [코드/최종/CSV 파이썬 코드/pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py) · `def parse_line` · 34
- [코드/최종/CSV 파이썬 코드/pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py) · `def main` · 46

셀 번호는 0부터, 소스 행 번호와 PDF 쪽 번호는 1부터 셉니다. 
