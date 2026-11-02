<div align="center">

# 🍃 1차

DHT11 온도·습도를 LCD와 RGB LED로 표시하고 두 값의 CSV를 전송합니다.

**기술 분류:** Arduino · DHT11 · I²C LCD · Python 시리얼 CSV

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 원본 자료](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8) · [다음: 최종 →](step-2.md)

## 🎯 목적과 이 차수의 역할

DHT11 온도·습도를 LCD와 RGB LED로 표시하고 두 값의 CSV를 전송합니다.

<a name="features"></a>

## ✨ 핵심 기능과 보존 범위

| 항목 | 이 차수에서 확인할 내용 |
|---|---|
| 1 | DHT11 온도·습도를 LCD와 RGB LED로 표시하고 두 값의 CSV를 전송합니다. |
| 2 | 초기 Python 수집기는 쉼표로 나눈 2개 필드를 받아 PC 시각을 붙입니다. 최종판의 7필드 숫자·빈칸 검사를 소급하지 않습니다. |
| 3 | 기본 포트는 COM3, 전송속도는 9600 baud, 파일명은 dht_log.csv입니다. |

## 🔄 입력·처리·출력

| 단계 | 내용 |
|---|---|
| 📥 입력 | DHT 온습도 |
| ⚙️ 처리 | Arduino 센싱 → LCD·RGB LED → 9600 baud 시리얼 → Python 기록 |
| 📤 출력 | dht_log.csv: timestamp·temperature_C·humidity_% |

<a name="usage"></a>

## 🖐️ 화면과 사용 흐름

1. 보드와 센서·LCD·RGB LED 배선을 확인합니다.
2. 이 차수 .ino를 업로드하고 실제 센서 출력을 확인합니다.
3. 수집기의 PORT를 실제 장치로 지정하고 OUTPUT_FILE을 새 기록 이름으로 정합니다.
4. Python 수집기를 실행해 헤더·열 수·시각·센서값을 확인합니다.

<a name="structure"></a>

## 📁 실제 자료 구성

| 경로 | 자료 종류 |
|---|---|
| [dht_lcd_rgb_csv/](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/dht_lcd_rgb_csv) | 하위 자료 폴더 |
| [README.md](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/README.md) | MD 파일 |
| [dht_log.csv](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/dht_log.csv) | CSV 파일 |
| [pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py) | PY 파일 |

## 🧩 주요 모듈과 코드 읽기

| 파일 | 원문에 정의된 역할·구성 |
|---|---|
| [pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py) | 소스 본문과 설정을 함께 읽는 구성요소 |
| [dht_lcd_rgb_csv/dht_lcd_rgb_csv.ino](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/dht_lcd_rgb_csv/dht_lcd_rgb_csv.ino) | 소스 본문과 설정을 함께 읽는 구성요소 |

<a name="setup"></a>

## 🚀 설치 환경과 실행·사용법

DHT sensor library와 LiquidCrystal_I2C를 지원하는 Arduino IDE·보드·USB 포트를 준비합니다. Python에는 pyserial이 필요합니다. LCD의 I²C 주소와 실제 보드 SDA/SCL을 확인합니다.

Arduino 스케치를 보드에 업로드하고 시리얼 출력을 9600 baud로 확인합니다. 시리얼 모니터를 닫은 뒤 수집기 폴더에서 `python pc_csv_logger.py`로 기록하고 Ctrl+C로 끝냅니다.

### 초기 수집기의 범위

1차는 DHT11 온도·습도 두 값과 PC 수신시각을 기록하는 구성입니다. 기본 COM3·9600baud·dht_log.csv를 사용합니다. 최종판은 AM1008W-K의 다섯 측정값과 숫자/빈칸 검사를 더하고 파일을 air_log.csv로 분리하므로, 두 차수 CSV의 열을 같은 형식으로 합치지 않습니다. 실제 수집 함수와 스케치의 필드 순서는 아래 연결된 소스에서 확인할 수 있습니다.

<details>
<summary>🔬 함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py)


| 설정·옵션 | 코드의 선언 |
|---|---|
| [`PORT`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L5) | `정의="COM3"` |
| [`BAUD`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L6) | `정의=9600` |
| [`OUTPUT_FILE`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L7) | `정의="dht_log.csv"` |

</details>

<a name="results"></a>

## 📊 처리 결과와 출력 읽기

출력 CSV는 현재 작업 폴더에 누적됩니다. 새 측정은 OUTPUT_FILE을 다른 이름으로 지정해 기존 측정 원본과 분리합니다. timestamp는 PC 수신 시각이며 센서 자체 시각이나 중단 없는 연속 측정 보증이 아닙니다.

## 🛠️ 제약과 문제 해결

| 상황 | 확인할 내용 |
|---|---|
| 포트를 열지 못함 | PORT·USB 연결·다른 프로그램의 포트 점유를 확인합니다. |
| LCD 표시 오류 | 주소·배선·대비·라이브러리 init/backlight 지원을 확인합니다. |
| 측정 누락 | 센서 배선·종류와 수집기의 행 형식 조건을 확인합니다. |

<a name="changes"></a>

## 🔍 직전 자료와 전체 비교

이 자료의 보존 범위와 기준 파일을 연결합니다.

[📄 전체 비교·자료 범위](step-1.patch)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.

<details>
<summary>📚 파일별 비교·크기·해시 자세히 보기</summary>

[전체 텍스트 차이](step-1.patch) · [파일별 크기·SHA-256](step-1-files.json)

| 구분 | 파일 |
| :--- | :--- |
| 추가 | `dht_lcd_rgb_csv/dht_lcd_rgb_csv.ino` |
| 추가 | `dht_log.csv` |
| 추가 | `pc_csv_logger.py` |

</details>

[🏠 프로젝트](../../README.md) · [🗂️ 전체 차수](../REVISION_INDEX.md) · [📁 원본 자료](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8) · [다음: 최종 →](step-2.md)
