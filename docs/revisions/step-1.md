

<a name="-1차"></a>
# 1차

<!-- reading-levels:start -->
[LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

프로젝트 전체의 설명은 [LEVEL 1 - Beginner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md)부터 [LEVEL 5 - Expert](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)까지 같은 범위로 연결됩니다.

<a id="reading-level-1"></a>
## LEVEL 1 - Beginner

### LEVEL 1 · 이 자료가 하는 일과 달라진 점

DHT11 온도·습도를 LCD와 RGB LED로 표시하고 두 값의 CSV를 전송합니다.

### LEVEL 1 · 실제 동작을 따라 읽기

DHT11 온도·습도를 LCD와 RGB LED로 표시하고 두 값의 CSV를 전송합니다.

초기 Python 수집기는 쉼표로 나눈 2개 필드를 받아 PC 시각을 붙입니다. 최종판의 7필드 숫자·빈칸 검사를 소급하지 않습니다.

기본 포트는 COM3, 전송속도는 9600 baud, 파일명은 dht_log.csv입니다.

CSV는 값을 쉼표로 나눈 표 파일입니다. DHT11은 온도와 습도를 읽는 센서입니다. LCD는 측정값이나 상태를 문자로 보여 주는 표시창입니다. RGB LED는 색을 바꾸어 상태를 나타내는 불빛입니다. baud는 장치와 PC가 맞춰야 하는 통신 속도의 단위입니다.

입력 — DHT 온습도

처리 — Arduino 센싱 → LCD·RGB LED → 9600 baud 시리얼 → Python 기록

출력 — dht_log.csv: timestamp·temperature_C·humidity_%

### LEVEL 1 · 준비하고 확인할 것

DHT sensor library와 LiquidCrystal_I2C를 지원하는 Arduino IDE·보드·USB 포트를 준비합니다. Python에는 pyserial이 필요합니다. LCD의 I²C 주소와 실제 보드 SDA/SCL을 확인합니다.

Arduino 스케치를 보드에 업로드하고 시리얼 출력을 9600 baud로 확인합니다. 시리얼 모니터를 닫은 뒤 수집기 폴더에서 `python pc_csv_logger.py`로 기록하고 Ctrl+C로 끝냅니다.

#### LEVEL 1 · 초기 수집기의 범위

1차는 DHT11 온도·습도 두 값과 PC 수신시각을 기록하는 구성입니다. 기본 COM3·9600baud·dht_log.csv를 사용합니다. 최종판은 AM1008W-K의 다섯 측정값과 숫자/빈칸 검사를 더하고 파일을 air_log.csv로 분리하므로, 두 차수 CSV의 열을 같은 형식으로 합치지 않습니다. 실제 수집 함수와 스케치의 필드 순서는 아래 연결된 소스에서 확인할 수 있습니다.

<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 1 · [pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py)


| 내용 |
| --- |
| **설정·옵션:** [`PORT`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L5)<br>**코드의 선언:** `정의="COM3"` |
| **설정·옵션:** [`BAUD`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L6)<br>**코드의 선언:** `정의=9600` |
| **설정·옵션:** [`OUTPUT_FILE`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L7)<br>**코드의 선언:** `정의="dht_log.csv"` |

</details>

1. 보드와 센서·LCD·RGB LED 배선을 확인합니다.
2. 이 차수 .ino를 업로드하고 실제 센서 출력을 확인합니다.
3. 수집기의 PORT를 실제 장치로 지정하고 OUTPUT_FILE을 새 기록 이름으로 정합니다.
4. Python 수집기를 실행해 헤더·열 수·시각·센서값을 확인합니다.

### LEVEL 1 · 결과와 주의할 범위

출력 CSV는 현재 작업 폴더에 누적됩니다. 새 측정은 OUTPUT_FILE을 다른 이름으로 지정해 기존 측정 원본과 분리합니다. timestamp는 PC 수신 시각이며 센서 자체 시각이나 중단 없는 연속 측정 보증이 아닙니다.

**상황:** 포트를 열지 못함

**확인할 내용:** PORT·USB 연결·다른 프로그램의 포트 점유를 확인합니다.

**상황:** LCD 표시 오류

**확인할 내용:** 주소·배선·대비·라이브러리 init/backlight 지원을 확인합니다.

**상황:** 측정 누락

**확인할 내용:** 센서 배선·종류와 수집기의 행 형식 조건을 확인합니다.


[자료 폴더](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8) · [직전 비교·자료 범위](step-1.patch) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-2"></a>
## LEVEL 2 - Explorer

### LEVEL 2 · 목적과 구성의 연결

DHT11 온도·습도를 LCD와 RGB LED로 표시하고 두 값의 CSV를 전송합니다.

DHT11 온도·습도를 LCD와 RGB LED로 표시하고 두 값의 CSV를 전송합니다.

초기 Python 수집기는 쉼표로 나눈 2개 필드를 받아 PC 시각을 붙입니다. 최종판의 7필드 숫자·빈칸 검사를 소급하지 않습니다.

기본 포트는 COM3, 전송속도는 9600 baud, 파일명은 dht_log.csv입니다.

### LEVEL 2 · 입력에서 출력으로

**단계:** 입력

**내용:** DHT 온습도

**단계:** 처리

**내용:** Arduino 센싱 → LCD·RGB LED → 9600 baud 시리얼 → Python 기록

**단계:** 출력

**내용:** dht_log.csv: timestamp·temperature_C·humidity_%


입력·처리·출력은 위의 같은 자료 흐름을 다른 단계에서 읽는 기준입니다. 처리 조건과 출력의 의미를 함께 확인합니다.

### LEVEL 2 · 설정과 처리 순서의 관계

1. 보드와 센서·LCD·RGB LED 배선을 확인합니다.
2. 이 차수 .ino를 업로드하고 실제 센서 출력을 확인합니다.
3. 수집기의 PORT를 실제 장치로 지정하고 OUTPUT_FILE을 새 기록 이름으로 정합니다.
4. Python 수집기를 실행해 헤더·열 수·시각·센서값을 확인합니다.

DHT sensor library와 LiquidCrystal_I2C를 지원하는 Arduino IDE·보드·USB 포트를 준비합니다. Python에는 pyserial이 필요합니다. LCD의 I²C 주소와 실제 보드 SDA/SCL을 확인합니다.

Arduino 스케치를 보드에 업로드하고 시리얼 출력을 9600 baud로 확인합니다. 시리얼 모니터를 닫은 뒤 수집기 폴더에서 `python pc_csv_logger.py`로 기록하고 Ctrl+C로 끝냅니다.

#### LEVEL 2 · 초기 수집기의 범위

1차는 DHT11 온도·습도 두 값과 PC 수신시각을 기록하는 구성입니다. 기본 COM3·9600baud·dht_log.csv를 사용합니다. 최종판은 AM1008W-K의 다섯 측정값과 숫자/빈칸 검사를 더하고 파일을 air_log.csv로 분리하므로, 두 차수 CSV의 열을 같은 형식으로 합치지 않습니다. 실제 수집 함수와 스케치의 필드 순서는 아래 연결된 소스에서 확인할 수 있습니다.

<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 2 · [pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py)


| 내용 |
| --- |
| **설정·옵션:** [`PORT`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L5)<br>**코드의 선언:** `정의="COM3"` |
| **설정·옵션:** [`BAUD`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L6)<br>**코드의 선언:** `정의=9600` |
| **설정·옵션:** [`OUTPUT_FILE`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L7)<br>**코드의 선언:** `정의="dht_log.csv"` |

</details>

### LEVEL 2 · 관측과 해석을 구분하기

출력 CSV는 현재 작업 폴더에 누적됩니다. 새 측정은 OUTPUT_FILE을 다른 이름으로 지정해 기존 측정 원본과 분리합니다. timestamp는 PC 수신 시각이며 센서 자체 시각이나 중단 없는 연속 측정 보증이 아닙니다.

**상황:** 포트를 열지 못함

**확인할 내용:** PORT·USB 연결·다른 프로그램의 포트 점유를 확인합니다.

**상황:** LCD 표시 오류

**확인할 내용:** 주소·배선·대비·라이브러리 init/backlight 지원을 확인합니다.

**상황:** 측정 누락

**확인할 내용:** 센서 배선·종류와 수집기의 행 형식 조건을 확인합니다.


[자료 폴더](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8) · [직전 비교·자료 범위](step-1.patch) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-3"></a>
## LEVEL 3 - Practitioner

### LEVEL 3 · 이 차수를 준비하는 범위

DHT11 온도·습도를 LCD와 RGB LED로 표시하고 두 값의 CSV를 전송합니다.

DHT sensor library와 LiquidCrystal_I2C를 지원하는 Arduino IDE·보드·USB 포트를 준비합니다. Python에는 pyserial이 필요합니다. LCD의 I²C 주소와 실제 보드 SDA/SCL을 확인합니다.

Arduino 스케치를 보드에 업로드하고 시리얼 출력을 9600 baud로 확인합니다. 시리얼 모니터를 닫은 뒤 수집기 폴더에서 `python pc_csv_logger.py`로 기록하고 Ctrl+C로 끝냅니다.

#### LEVEL 3 · 초기 수집기의 범위

1차는 DHT11 온도·습도 두 값과 PC 수신시각을 기록하는 구성입니다. 기본 COM3·9600baud·dht_log.csv를 사용합니다. 최종판은 AM1008W-K의 다섯 측정값과 숫자/빈칸 검사를 더하고 파일을 air_log.csv로 분리하므로, 두 차수 CSV의 열을 같은 형식으로 합치지 않습니다. 실제 수집 함수와 스케치의 필드 순서는 아래 연결된 소스에서 확인할 수 있습니다.

<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 3 · [pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py)


| 내용 |
| --- |
| **설정·옵션:** [`PORT`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L5)<br>**코드의 선언:** `정의="COM3"` |
| **설정·옵션:** [`BAUD`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L6)<br>**코드의 선언:** `정의=9600` |
| **설정·옵션:** [`OUTPUT_FILE`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L7)<br>**코드의 선언:** `정의="dht_log.csv"` |

</details>

### LEVEL 3 · 실제 사용·실험 순서

1. 보드와 센서·LCD·RGB LED 배선을 확인합니다.
2. 이 차수 .ino를 업로드하고 실제 센서 출력을 확인합니다.
3. 수집기의 PORT를 실제 장치로 지정하고 OUTPUT_FILE을 새 기록 이름으로 정합니다.
4. Python 수집기를 실행해 헤더·열 수·시각·센서값을 확인합니다.

**단계:** 입력

**내용:** DHT 온습도

**단계:** 처리

**내용:** Arduino 센싱 → LCD·RGB LED → 9600 baud 시리얼 → Python 기록

**단계:** 출력

**내용:** dht_log.csv: timestamp·temperature_C·humidity_%


### LEVEL 3 · 결과와 실패를 확인하기

출력 CSV는 현재 작업 폴더에 누적됩니다. 새 측정은 OUTPUT_FILE을 다른 이름으로 지정해 기존 측정 원본과 분리합니다. timestamp는 PC 수신 시각이며 센서 자체 시각이나 중단 없는 연속 측정 보증이 아닙니다.

**상황:** 포트를 열지 못함

**확인할 내용:** PORT·USB 연결·다른 프로그램의 포트 점유를 확인합니다.

**상황:** LCD 표시 오류

**확인할 내용:** 주소·배선·대비·라이브러리 init/backlight 지원을 확인합니다.

**상황:** 측정 누락

**확인할 내용:** 센서 배선·종류와 수집기의 행 형식 조건을 확인합니다.


### LEVEL 3 · 실행 전 대조할 차수 조건

DHT11 온도·습도를 LCD와 RGB LED로 표시하고 두 값의 CSV를 전송합니다.

초기 Python 수집기는 쉼표로 나눈 2개 필드를 받아 PC 시각을 붙입니다. 최종판의 7필드 숫자·빈칸 검사를 소급하지 않습니다.

기본 포트는 COM3, 전송속도는 9600 baud, 파일명은 dht_log.csv입니다.

[자료 폴더](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8) · [직전 비교·자료 범위](step-1.patch) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-4"></a>
## LEVEL 4 - Advanced

### LEVEL 4 · 설계 의도와 검토 경계

DHT11 온도·습도를 LCD와 RGB LED로 표시하고 두 값의 CSV를 전송합니다.

DHT11 온도·습도를 LCD와 RGB LED로 표시하고 두 값의 CSV를 전송합니다.

초기 Python 수집기는 쉼표로 나눈 2개 필드를 받아 PC 시각을 붙입니다. 최종판의 7필드 숫자·빈칸 검사를 소급하지 않습니다.

기본 포트는 COM3, 전송속도는 9600 baud, 파일명은 dht_log.csv입니다.

### LEVEL 4 · 이 차수 구현의 실제 근거

| 내용 |
| --- |
| **파일:** [pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py)<br>**원문에 정의된 역할·구성:** 소스 본문과 설정을 함께 읽는 구성요소 |
| **파일:** [dht_lcd_rgb_csv/dht_lcd_rgb_csv.ino](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/dht_lcd_rgb_csv/dht_lcd_rgb_csv.ino)<br>**원문에 정의된 역할·구성:** 소스 본문과 설정을 함께 읽는 구성요소 |

**단계:** 입력

**내용:** DHT 온습도

**단계:** 처리

**내용:** Arduino 센싱 → LCD·RGB LED → 9600 baud 시리얼 → Python 기록

**단계:** 출력

**내용:** dht_log.csv: timestamp·temperature_C·humidity_%


### LEVEL 4 · 조건·변경·결과를 함께 검토하기

DHT sensor library와 LiquidCrystal_I2C를 지원하는 Arduino IDE·보드·USB 포트를 준비합니다. Python에는 pyserial이 필요합니다. LCD의 I²C 주소와 실제 보드 SDA/SCL을 확인합니다.

Arduino 스케치를 보드에 업로드하고 시리얼 출력을 9600 baud로 확인합니다. 시리얼 모니터를 닫은 뒤 수집기 폴더에서 `python pc_csv_logger.py`로 기록하고 Ctrl+C로 끝냅니다.

#### LEVEL 4 · 초기 수집기의 범위

1차는 DHT11 온도·습도 두 값과 PC 수신시각을 기록하는 구성입니다. 기본 COM3·9600baud·dht_log.csv를 사용합니다. 최종판은 AM1008W-K의 다섯 측정값과 숫자/빈칸 검사를 더하고 파일을 air_log.csv로 분리하므로, 두 차수 CSV의 열을 같은 형식으로 합치지 않습니다. 실제 수집 함수와 스케치의 필드 순서는 아래 연결된 소스에서 확인할 수 있습니다.

<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 4 · [pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py)


| 내용 |
| --- |
| **설정·옵션:** [`PORT`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L5)<br>**코드의 선언:** `정의="COM3"` |
| **설정·옵션:** [`BAUD`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L6)<br>**코드의 선언:** `정의=9600` |
| **설정·옵션:** [`OUTPUT_FILE`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L7)<br>**코드의 선언:** `정의="dht_log.csv"` |

</details>

출력 CSV는 현재 작업 폴더에 누적됩니다. 새 측정은 OUTPUT_FILE을 다른 이름으로 지정해 기존 측정 원본과 분리합니다. timestamp는 PC 수신 시각이며 센서 자체 시각이나 중단 없는 연속 측정 보증이 아닙니다.

**상황:** 포트를 열지 못함

**확인할 내용:** PORT·USB 연결·다른 프로그램의 포트 점유를 확인합니다.

**상황:** LCD 표시 오류

**확인할 내용:** 주소·배선·대비·라이브러리 init/backlight 지원을 확인합니다.

**상황:** 측정 누락

**확인할 내용:** 센서 배선·종류와 수집기의 행 형식 조건을 확인합니다.


### LEVEL 4 · 재현과 전체 비교

1. 보드와 센서·LCD·RGB LED 배선을 확인합니다.
2. 이 차수 .ino를 업로드하고 실제 센서 출력을 확인합니다.
3. 수집기의 PORT를 실제 장치로 지정하고 OUTPUT_FILE을 새 기록 이름으로 정합니다.
4. Python 수집기를 실행해 헤더·열 수·시각·센서값을 확인합니다.

위 구성요소의 입력·출력과 실패 조건을 같은 차수 소스에 연결해 검토합니다. 전체 비교는 추가·수정·삭제와 원래 보관 범위를 구분하는 근거입니다.

[자료 폴더](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8) · [직전 비교·자료 범위](step-1.patch) · [이 차수의 원래 전체 상세](#reading-level-5)
<a id="reading-level-5"></a>
## LEVEL 5 - Expert

기존의 전체 설명·표·코드·함수 참조·파일별 비교는 아래에 그대로 이어집니다. [자료 폴더](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8) · [직전 비교·자료 범위](step-1.patch) · [이 차수의 원래 전체 상세](#reading-level-5)
<!-- reading-levels:end -->


DHT11의 온도와 습도를 기록하는 초기 구성입니다.



**기술 분류:** Arduino · DHT11 · I²C LCD · Python 시리얼 CSV

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)



[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8) · [다음: 최종 →](step-2.md)

<a name="-목적과-이-차수의-역할"></a>
## 목적과 이 차수의 역할

DHT11 온도·습도를 LCD와 RGB LED로 표시하고 두 값의 CSV를 전송합니다.

<a name="features"></a>

<a name="-핵심-기능과-보존-범위"></a>
## 핵심 기능과 보존 범위

**항목:** 1

**이 차수에서 확인할 내용:** DHT11 온도·습도를 LCD와 RGB LED로 표시하고 두 값의 CSV를 전송합니다.

**항목:** 2

**이 차수에서 확인할 내용:** 초기 Python 수집기는 쉼표로 나눈 2개 필드를 받아 PC 시각을 붙입니다. 최종판의 7필드 숫자·빈칸 검사를 소급하지 않습니다.

**항목:** 3

**이 차수에서 확인할 내용:** 기본 포트는 COM3, 전송속도는 9600 baud, 파일명은 dht_log.csv입니다.


<a name="-입력처리출력"></a>
## 입력·처리·출력

**단계:** 입력

**내용:** DHT 온습도

**단계:** 처리

**내용:** Arduino 센싱 → LCD·RGB LED → 9600 baud 시리얼 → Python 기록

**단계:** 출력

**내용:** dht_log.csv: timestamp·temperature_C·humidity_%


<a name="usage"></a>

<a name="️-화면과-사용-흐름"></a>
## 화면과 사용 흐름

1. 보드와 센서·LCD·RGB LED 배선을 확인합니다.
2. 이 차수 .ino를 업로드하고 실제 센서 출력을 확인합니다.
3. 수집기의 PORT를 실제 장치로 지정하고 OUTPUT_FILE을 새 기록 이름으로 정합니다.
4. Python 수집기를 실행해 헤더·열 수·시각·센서값을 확인합니다.

<a name="structure"></a>

<a name="-실제-자료-구성"></a>
## 실제 자료 구성

| 내용 |
| --- |
| **경로:** [dht_lcd_rgb_csv/](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/dht_lcd_rgb_csv)<br>**자료 종류:** 하위 자료 폴더 |
| **경로:** [README.md](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/README.md)<br>**자료 종류:** MD 파일 |
| **경로:** [dht_log.csv](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/dht_log.csv)<br>**자료 종류:** CSV 파일 |
| **경로:** [pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py)<br>**자료 종류:** PY 파일 |

<a name="-주요-모듈과-코드-읽기"></a>
## 주요 모듈과 코드 읽기

| 내용 |
| --- |
| **파일:** [pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py)<br>**원문에 정의된 역할·구성:** 소스 본문과 설정을 함께 읽는 구성요소 |
| **파일:** [dht_lcd_rgb_csv/dht_lcd_rgb_csv.ino](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/dht_lcd_rgb_csv/dht_lcd_rgb_csv.ino)<br>**원문에 정의된 역할·구성:** 소스 본문과 설정을 함께 읽는 구성요소 |

<a name="setup"></a>

<a name="-설치-환경과-실행사용법"></a>
## 설치 환경과 실행·사용법

DHT sensor library와 LiquidCrystal_I2C를 지원하는 Arduino IDE·보드·USB 포트를 준비합니다. Python에는 pyserial이 필요합니다. LCD의 I²C 주소와 실제 보드 SDA/SCL을 확인합니다.

Arduino 스케치를 보드에 업로드하고 시리얼 출력을 9600 baud로 확인합니다. 시리얼 모니터를 닫은 뒤 수집기 폴더에서 `python pc_csv_logger.py`로 기록하고 Ctrl+C로 끝냅니다.

### 초기 수집기의 범위

1차는 DHT11 온도·습도 두 값과 PC 수신시각을 기록하는 구성입니다. 기본 COM3·9600baud·dht_log.csv를 사용합니다. 최종판은 AM1008W-K의 다섯 측정값과 숫자/빈칸 검사를 더하고 파일을 air_log.csv로 분리하므로, 두 차수 CSV의 열을 같은 형식으로 합치지 않습니다. 실제 수집 함수와 스케치의 필드 순서는 아래 연결된 소스에서 확인할 수 있습니다.

<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py)


| 내용 |
| --- |
| **설정·옵션:** [`PORT`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L5)<br>**코드의 선언:** `정의="COM3"` |
| **설정·옵션:** [`BAUD`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L6)<br>**코드의 선언:** `정의=9600` |
| **설정·옵션:** [`OUTPUT_FILE`](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8/pc_csv_logger.py#L7)<br>**코드의 선언:** `정의="dht_log.csv"` |

</details>

<a name="results"></a>

<a name="-처리-결과와-출력-읽기"></a>
## 처리 결과와 출력 읽기

출력 CSV는 현재 작업 폴더에 누적됩니다. 새 측정은 OUTPUT_FILE을 다른 이름으로 지정해 기존 측정 원본과 분리합니다. timestamp는 PC 수신 시각이며 센서 자체 시각이나 중단 없는 연속 측정 보증이 아닙니다.

<a name="️-제약과-문제-해결"></a>
## 제약과 문제 해결

**상황:** 포트를 열지 못함

**확인할 내용:** PORT·USB 연결·다른 프로그램의 포트 점유를 확인합니다.

**상황:** LCD 표시 오류

**확인할 내용:** 주소·배선·대비·라이브러리 init/backlight 지원을 확인합니다.

**상황:** 측정 누락

**확인할 내용:** 센서 배선·종류와 수집기의 행 형식 조건을 확인합니다.


<a name="changes"></a>

<a name="-직전-자료와-전체-비교"></a>
## 직전 자료와 전체 비교

이 자료의 보존 범위와 기준 파일을 연결합니다.

[전체 비교·자료 범위](step-1.patch)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.

<details>
<summary>파일별 비교·크기·해시 자세히 보기</summary>

[전체 텍스트 차이](step-1.patch) · [파일별 크기·SHA-256](step-1-files.json)

**구분:** 추가

**파일:** `dht_lcd_rgb_csv/dht_lcd_rgb_csv.ino`

**구분:** 추가

**파일:** `dht_log.csv`

**구분:** 추가

**파일:** `pc_csv_logger.py`


</details>

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../%EC%BD%94%EB%93%9C/1%EC%B0%A8) · [다음: 최종 →](step-2.md)
