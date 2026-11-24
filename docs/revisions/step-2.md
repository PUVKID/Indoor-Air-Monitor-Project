<div align="center">

<a name="-최종"></a>
# 최종

DHT와 AM1008W-K를 함께 읽고 LCD의 DHT·AM 온습도·공기질 화면을 순환합니다.

**기술 분류:** Arduino · DHT11·AM1008W-K · I²C LCD · Python 시리얼 CSV

[핵심 기능](#features) · [사용 흐름](#usage) · [자료 구성](#structure) · [준비와 실행](#setup) · [결과 읽기](#results) · [직전 변경](#changes)

</div>
<!-- reading-levels:start -->
[LEVEL 1 - Beginner](#reading-level-1) · [LEVEL 2 - Explorer](#reading-level-2) · [LEVEL 3 - Practitioner](#reading-level-3) · [LEVEL 4 - Advanced](#reading-level-4) · [LEVEL 5 - Expert](#reading-level-5)

프로젝트 전체의 설명은 [LEVEL 1 - Beginner](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A81.md)부터 [LEVEL 5 - Expert](../%EC%9D%BD%EA%B8%B0%EC%95%88%EB%82%B4/%EB%A0%88%EB%B2%A85.md)까지 같은 범위로 연결됩니다.

<a id="reading-level-1"></a>
## LEVEL 1 - Beginner

### LEVEL 1 · 이 자료가 하는 일과 달라진 점

DHT와 AM1008W-K를 함께 읽고 LCD의 DHT·AM 온습도·공기질 화면을 순환합니다.

### LEVEL 1 · 실제 동작을 따라 읽기

DHT와 AM1008W-K를 함께 읽고 LCD의 DHT·AM 온습도·공기질 화면을 순환합니다.

읽기에 성공한 측정 항목 중 가장 높은 위험 등급을 RGB LED로 표시합니다. 전부 실패하면 LED를 끕니다.

parse_line은 센서 값 7 필드가 숫자 또는 빈 칸인지 확인합니다. 일부 실패는 빈 칸으로 보존하고 전부 빈 행은 제외합니다.

기본 포트 COM4, 9600 baud로 수신하고 UTF-8 air_log.csv에 PC 시각을 앞에 붙여 8 열로 저장합니다.

CSV는 값을 쉼표로 나눈 표 파일입니다.

DHT11은 온도와 습도를 읽는 센서입니다.

LCD는 측정 값이나 상태를 문자로 보여 주는 표시 창입니다.

RGB LED는 색을 바꾸어 상태를 나타내는 불빛입니다. baud는 장치와 PC가 맞춰야하는 통신 속도의 단위입니다.

체크섬은 받은 바이트가 형식상 손상되지 않았는지 대조하는 값입니다.

입력 — DHT 온습도·AM 온습도·CO₂·VOC·PM2.5

처리 — Arduino 센싱 → LCD·RGB LED → 9600 baud 시리얼 → Python 기록

출력 — air_log.csv: PC 시각과 7개 센서 값, 총 8 열

### LEVEL 1 · 준비하고 확인할 것

DHT sensor library와 LiquidCrystal_I2C를 지원하는 Arduino IDE·보드·USB 포트를 준비합니다. Python에는 pyserial이 필요합니다. LCD의 I²C 주소와 실제 보드 SDA/SCL을 확인합니다.

Arduino 스케치를 보드에 업로드하고 시리얼 출력을 9600 baud로 확인합니다. 시리얼 모니터를 닫은 뒤 수집기 폴더에서 `python pc_csv_logger.py`로 기록하고 Ctrl +C로 끝냅니다.

#### LEVEL 1 · 이 차수 원래 안내의 세부 조건

#### LEVEL 1 · 저장소 구성

원본 최종 폴더의 세 파일을 폴더 구조 그대로 보관했습니다.

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── 아두이노 코드/
│   └── dht_am1008w_lcd_csv/
│       └── dht_am1008w_lcd_csv.ino
└── CSV 파이썬 코드/
    ├── pc_csv_logger.py
    └── air_log.csv
```

- [아두이노 스케치](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/%EC%95%84%EB%91%90%EC%9D%B4%EB%85%B8%20%EC%BD%94%EB%93%9C/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino): 센서 읽기, LCD 표시, LED 등급 판정, CSV 전송.
- [Python 수집기](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py): 데이터 형식 검사 및 타임스탬프를 포함한 CSV 저장.
- `air_log.csv`: 수집기를 실행하면 작업 위치에 생성되는 기록 파일입니다. **당시 안내에는 공개 저장소에 포함하지 않았다고 적혀 있지만, 현재 보존된 최종 폴더에는 [CSV 원본](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/air_log.csv)이 제공됩니다.** 기존 기록 파일의 제공과 새 환경에서의 측정은 별개이며, 새 기록은 `OUTPUT_FILE`을 다른 이름으로 지정해 분리합니다.

#### LEVEL 1 · 데이터 구성

CSV는 PC 수신 시각과 센서 값 7개로 구성됩니다. `timestamp`는 PC의 로컬 시각이며 시간대 정보는 포함하지 않습니다.

| 열 | 의미 | 단위 |
| --- | --- | --- |
| `timestamp` | PC에서 데이터를 수신한 시각 | `YYYY-MM-DD HH:MM:SS` |
| `dht_temp_C` | DHT 온도 | °C |
| `dht_humi_pct` | DHT 상대습도 | % |
| `am_temp_C` | AM1008W-K 온도 | °C |
| `am_humi_pct` | AM1008W-K 상대습도 | % |
| `co2_ppm` | CO₂ | ppm |
| `voc_level` | VOC 단계 | 센서 단계 값 |
| `pm25_ugm3` | PM2.5 | µg/m³ |

수집기는 헤더, 열 개수가 잘못된 행, 숫자 또는 빈칸 이외의 값이 있는 행을 건너뜁니다. 일부 센서가 실패한 행은 정상 항목을 보존합니다.

원본 CSV의 첫 기록은 `2026-10-03 00:29:31`, 마지막 기록은 `2026-10-14 14:44:49`입니다. 이 범위가 중단 없는 연속 측정을 의미하지는 않습니다.

#### LEVEL 1 · 이 보관본의 의존성 목록

[requirements.txt](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/requirements.txt)의 실제 항목입니다. 외부 실행 도구와 GPU 드라이버는 별도로 준비합니다.

```text
pyserial
```

#### LEVEL 1 · 센서 프레임·등급·CSV 처리

`readAM1008W`는 I²C 주소 0x28에서 25바이트를 읽고 길이·0x16 헤더·앞 24바이트 XOR 체크섬을 검사합니다. 온도는 `(rawTemp-500)/10.0`, 습도는 `rawHumi/10.0`으로 바꿉니다. DHT11은 2번 핀, RGB는9/10/11번 핀, LCD는 0x27·16×2 설정입니다.

`showPage`는 DHT 온습도 →AM 온습도 →CO ₂/VOC/PM2.5 화면을 3초씩 순환합니다. `lcdLine`은 남은 16 칸을 공백으로 채워 잔상을 지웁니다. 센서 실패 화면과 실제 0 값은 구분합니다.

**항목:** 온도

**코드의 0·1·2·3 등급 판정 순서:** 20≤t<26 /18≤t<28 /15≤t<30 /그 밖

**항목:** 습도

**코드의 0·1·2·3 등급 판정 순서:** 40≤h≤60 /30≤h≤70 /20≤h≤80 /그 밖

**항목:** CO₂

**코드의 0·1·2·3 등급 판정 순서:** 800 미만/1000 미만/1500 미만/그 이상

**항목:** VOC

**코드의 0·1·2·3 등급 판정 순서:** 1 이하 →0,2 →1, 나머지 →2

**항목:** PM2.5

**코드의 0·1·2·3 등급 판정 순서:** 15 이하/35 이하/75 이하/그 이상


읽기에 성공한 모든 항목의 최대 등급을 초록·노랑·빨강·보라로 표시하고 둘 다 실패하면 LED를 끕니다. 이 값은 프로젝트의 표시 규칙입니다.

PC의 `parse_line`은 쉼표 7 필드, 각 필드 숫자 또는 빈 칸, 적어도 하나의 값 존재를 요구합니다.

헤더·잘못된 열 수·모두 빈 행은 버리고 일부 센서 실패는 빈 칸으로 보존합니다. `main`은 COM4·9600baud·timeout2초로 열고 2초 대기 후 수신 버퍼를 비웁니다. `air_log.csv`를 UTF-8 추가 모드로 열어 빈 파일일 때만 헤더를 쓰고, PC 수신 시각을 붙인 8 열을 매 행 flush합니다.

Ctrl +C 때 안내를 남기고 finally에서 포트를 닫습니다.

자동 재연결 루프는 이 수집기에 없습니다.

<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 1 · [CSV 파이썬 코드/pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py)

| 정의 | 소스에 적힌 역할 |
| --- | --- |
| [`is_number_or_blank`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L22) | 빈칸(센서 읽기 실패)이거나 숫자면 True.<br>헤더 줄 같은 문자열은 False. |
| [`parse_line`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L34) | 아두이노 한 줄 -&gt; 값 리스트.<br>형식이 맞지 않으면(헤더 줄, 깨진 줄 등) None. |

**설정·옵션:** [`PORT`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L6)

**코드의 선언:** `정의="COM4"`

**설정·옵션:** [`BAUD`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L7)

**코드의 선언:** `정의=9600`

**설정·옵션:** [`OUTPUT_FILE`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L8)

**코드의 선언:** `정의="air_log.csv"`

**설정·옵션:** [`COLUMNS`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L11)

**코드의 선언:** `정의=[     "dht_temp_C",     "dht_humi_pct",     "am_temp_C",     "am_humi_pct",     "co2_ppm",     "voc_level",     "pm25_ugm3", ]`


</details>

1. 보드와 센서·LCD·RGB LED 배선을 확인합니다.
2. 이 차수 .ino를 업로드하고 실제 센서 출력을 확인합니다.
3. 수집기의 PORT를 실제 장치로 지정하고 OUTPUT_FILE을 새 기록 이름으로 정합니다.
4. Python 수집기를 실행해 헤더·열 수·시각·센서값을 확인합니다.

### LEVEL 1 · 결과와 주의할 범위

출력 CSV는 현재 작업 폴더에 누적됩니다. 새 측정은 OUTPUT_FILE을 다른 이름으로 지정해 기존 측정 원본과 분리합니다. timestamp는 PC 수신 시각이며 센서 자체 시각이나 중단 없는 연속 측정 보증이 아닙니다.

| 상황 | 확인할 내용 |
| --- | --- |
| 포트를 열지 못함 | PORT·USB 연결·다른 프로그램의 포트 점유를 확인합니다. |
| LCD 표시 오류 | 주소·배선·대비·라이브러리 init/backlight 지원을 확인합니다. |
| 측정 누락 | 센서 배선·종류와 수집기의 행 형식 조건을 확인합니다. |

[자료 폴더](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85) · [직전 비교·자료 범위](step-2.patch) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-2"></a>
## LEVEL 2 - Explorer

### LEVEL 2 · 목적과 구성의 연결

DHT와 AM1008W-K를 함께 읽고 LCD의 DHT·AM 온습도·공기질 화면을 순환합니다.

DHT와 AM1008W-K를 함께 읽고 LCD의 DHT·AM 온습도·공기질 화면을 순환합니다.

읽기에 성공한 측정 항목 중 가장 높은 위험 등급을 RGB LED로 표시합니다. 전부 실패하면 LED를 끕니다.

parse_line은 센서 값 7 필드가 숫자 또는 빈 칸인지 확인합니다. 일부 실패는 빈 칸으로 보존하고 전부 빈 행은 제외합니다.

기본 포트 COM4, 9600 baud로 수신하고 UTF-8 air_log.csv에 PC 시각을 앞에 붙여 8 열로 저장합니다.

### LEVEL 2 · 입력에서 출력으로

| 단계 | 내용 |
| --- | --- |
| 입력 | DHT 온습도·AM 온습도·CO₂·VOC·PM2.5 |
| 처리 | Arduino 센싱 → LCD·RGB LED → 9600 baud 시리얼 → Python 기록 |
| 출력 | air_log.csv: PC 시각과 7개 센서 값, 총 8 열 |

입력·처리·출력은 위의 같은 자료 흐름을 다른 단계에서 읽는 기준입니다. 처리 조건과 출력의 의미를 함께 확인합니다.

### LEVEL 2 · 설정과 처리 순서의 관계

1. 보드와 센서·LCD·RGB LED 배선을 확인합니다.
2. 이 차수 .ino를 업로드하고 실제 센서 출력을 확인합니다.
3. 수집기의 PORT를 실제 장치로 지정하고 OUTPUT_FILE을 새 기록 이름으로 정합니다.
4. Python 수집기를 실행해 헤더·열 수·시각·센서값을 확인합니다.

DHT sensor library와 LiquidCrystal_I2C를 지원하는 Arduino IDE·보드·USB 포트를 준비합니다. Python에는 pyserial이 필요합니다. LCD의 I²C 주소와 실제 보드 SDA/SCL을 확인합니다.

Arduino 스케치를 보드에 업로드하고 시리얼 출력을 9600 baud로 확인합니다. 시리얼 모니터를 닫은 뒤 수집기 폴더에서 `python pc_csv_logger.py`로 기록하고 Ctrl +C로 끝냅니다.

#### LEVEL 2 · 이 차수 원래 안내의 세부 조건

#### LEVEL 2 · 저장소 구성

원본 최종 폴더의 세 파일을 폴더 구조 그대로 보관했습니다.

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── 아두이노 코드/
│   └── dht_am1008w_lcd_csv/
│       └── dht_am1008w_lcd_csv.ino
└── CSV 파이썬 코드/
    ├── pc_csv_logger.py
    └── air_log.csv
```

- [아두이노 스케치](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/%EC%95%84%EB%91%90%EC%9D%B4%EB%85%B8%20%EC%BD%94%EB%93%9C/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino): 센서 읽기, LCD 표시, LED 등급 판정, CSV 전송.
- [Python 수집기](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py): 데이터 형식 검사 및 타임스탬프를 포함한 CSV 저장.
- `air_log.csv`: 수집기를 실행하면 작업 위치에 생성되는 기록 파일입니다. **당시 안내에는 공개 저장소에 포함하지 않았다고 적혀 있지만, 현재 보존된 최종 폴더에는 [CSV 원본](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/air_log.csv)이 제공됩니다.** 기존 기록 파일의 제공과 새 환경에서의 측정은 별개이며, 새 기록은 `OUTPUT_FILE`을 다른 이름으로 지정해 분리합니다.

#### LEVEL 2 · 데이터 구성

CSV는 PC 수신 시각과 센서 값 7개로 구성됩니다. `timestamp`는 PC의 로컬 시각이며 시간대 정보는 포함하지 않습니다.

| 열 | 의미 | 단위 |
| --- | --- | --- |
| `timestamp` | PC에서 데이터를 수신한 시각 | `YYYY-MM-DD HH:MM:SS` |
| `dht_temp_C` | DHT 온도 | °C |
| `dht_humi_pct` | DHT 상대습도 | % |
| `am_temp_C` | AM1008W-K 온도 | °C |
| `am_humi_pct` | AM1008W-K 상대습도 | % |
| `co2_ppm` | CO₂ | ppm |
| `voc_level` | VOC 단계 | 센서 단계 값 |
| `pm25_ugm3` | PM2.5 | µg/m³ |

수집기는 헤더, 열 개수가 잘못된 행, 숫자 또는 빈칸 이외의 값이 있는 행을 건너뜁니다. 일부 센서가 실패한 행은 정상 항목을 보존합니다.

원본 CSV의 첫 기록은 `2026-10-03 00:29:31`, 마지막 기록은 `2026-10-14 14:44:49`입니다. 이 범위가 중단 없는 연속 측정을 의미하지는 않습니다.

#### LEVEL 2 · 이 보관본의 의존성 목록

[requirements.txt](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/requirements.txt)의 실제 항목입니다. 외부 실행 도구와 GPU 드라이버는 별도로 준비합니다.

```text
pyserial
```

#### LEVEL 2 · 센서 프레임·등급·CSV 처리

`readAM1008W`는 I²C 주소 0x28에서 25바이트를 읽고 길이·0x16 헤더·앞 24바이트 XOR 체크섬을 검사합니다. 온도는 `(rawTemp-500)/10.0`, 습도는 `rawHumi/10.0`으로 바꿉니다. DHT11은 2번 핀, RGB는9/10/11번 핀, LCD는 0x27·16×2 설정입니다.

`showPage`는 DHT 온습도 →AM 온습도 →CO ₂/VOC/PM2.5 화면을 3초씩 순환합니다. `lcdLine`은 남은 16 칸을 공백으로 채워 잔상을 지웁니다. 센서 실패 화면과 실제 0 값은 구분합니다.

**항목:** 온도

**코드의 0·1·2·3 등급 판정 순서:** 20≤t<26 /18≤t<28 /15≤t<30 /그 밖

**항목:** 습도

**코드의 0·1·2·3 등급 판정 순서:** 40≤h≤60 /30≤h≤70 /20≤h≤80 /그 밖

**항목:** CO₂

**코드의 0·1·2·3 등급 판정 순서:** 800 미만/1000 미만/1500 미만/그 이상

**항목:** VOC

**코드의 0·1·2·3 등급 판정 순서:** 1 이하 →0,2 →1, 나머지 →2

**항목:** PM2.5

**코드의 0·1·2·3 등급 판정 순서:** 15 이하/35 이하/75 이하/그 이상


읽기에 성공한 모든 항목의 최대 등급을 초록·노랑·빨강·보라로 표시하고 둘 다 실패하면 LED를 끕니다. 이 값은 프로젝트의 표시 규칙입니다.

PC의 `parse_line`은 쉼표 7 필드, 각 필드 숫자 또는 빈 칸, 적어도 하나의 값 존재를 요구합니다.

헤더·잘못된 열 수·모두 빈 행은 버리고 일부 센서 실패는 빈 칸으로 보존합니다. `main`은 COM4·9600baud·timeout2초로 열고 2초 대기 후 수신 버퍼를 비웁니다. `air_log.csv`를 UTF-8 추가 모드로 열어 빈 파일일 때만 헤더를 쓰고, PC 수신 시각을 붙인 8 열을 매 행 flush합니다.

Ctrl +C 때 안내를 남기고 finally에서 포트를 닫습니다.

자동 재연결 루프는 이 수집기에 없습니다.

<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 2 · [CSV 파이썬 코드/pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py)

| 정의 | 소스에 적힌 역할 |
| --- | --- |
| [`is_number_or_blank`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L22) | 빈칸(센서 읽기 실패)이거나 숫자면 True.<br>헤더 줄 같은 문자열은 False. |
| [`parse_line`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L34) | 아두이노 한 줄 -&gt; 값 리스트.<br>형식이 맞지 않으면(헤더 줄, 깨진 줄 등) None. |

**설정·옵션:** [`PORT`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L6)

**코드의 선언:** `정의="COM4"`

**설정·옵션:** [`BAUD`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L7)

**코드의 선언:** `정의=9600`

**설정·옵션:** [`OUTPUT_FILE`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L8)

**코드의 선언:** `정의="air_log.csv"`

**설정·옵션:** [`COLUMNS`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L11)

**코드의 선언:** `정의=[     "dht_temp_C",     "dht_humi_pct",     "am_temp_C",     "am_humi_pct",     "co2_ppm",     "voc_level",     "pm25_ugm3", ]`


</details>

### LEVEL 2 · 관측과 해석을 구분하기

출력 CSV는 현재 작업 폴더에 누적됩니다. 새 측정은 OUTPUT_FILE을 다른 이름으로 지정해 기존 측정 원본과 분리합니다. timestamp는 PC 수신 시각이며 센서 자체 시각이나 중단 없는 연속 측정 보증이 아닙니다.

| 상황 | 확인할 내용 |
| --- | --- |
| 포트를 열지 못함 | PORT·USB 연결·다른 프로그램의 포트 점유를 확인합니다. |
| LCD 표시 오류 | 주소·배선·대비·라이브러리 init/backlight 지원을 확인합니다. |
| 측정 누락 | 센서 배선·종류와 수집기의 행 형식 조건을 확인합니다. |

[자료 폴더](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85) · [직전 비교·자료 범위](step-2.patch) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-3"></a>
## LEVEL 3 - Practitioner

### LEVEL 3 · 이 차수를 준비하는 범위

DHT와 AM1008W-K를 함께 읽고 LCD의 DHT·AM 온습도·공기질 화면을 순환합니다.

DHT sensor library와 LiquidCrystal_I2C를 지원하는 Arduino IDE·보드·USB 포트를 준비합니다. Python에는 pyserial이 필요합니다. LCD의 I²C 주소와 실제 보드 SDA/SCL을 확인합니다.

Arduino 스케치를 보드에 업로드하고 시리얼 출력을 9600 baud로 확인합니다. 시리얼 모니터를 닫은 뒤 수집기 폴더에서 `python pc_csv_logger.py`로 기록하고 Ctrl +C로 끝냅니다.

#### LEVEL 3 · 이 차수 원래 안내의 세부 조건

#### LEVEL 3 · 저장소 구성

원본 최종 폴더의 세 파일을 폴더 구조 그대로 보관했습니다.

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── 아두이노 코드/
│   └── dht_am1008w_lcd_csv/
│       └── dht_am1008w_lcd_csv.ino
└── CSV 파이썬 코드/
    ├── pc_csv_logger.py
    └── air_log.csv
```

- [아두이노 스케치](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/%EC%95%84%EB%91%90%EC%9D%B4%EB%85%B8%20%EC%BD%94%EB%93%9C/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino): 센서 읽기, LCD 표시, LED 등급 판정, CSV 전송.
- [Python 수집기](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py): 데이터 형식 검사 및 타임스탬프를 포함한 CSV 저장.
- `air_log.csv`: 수집기를 실행하면 작업 위치에 생성되는 기록 파일입니다. **당시 안내에는 공개 저장소에 포함하지 않았다고 적혀 있지만, 현재 보존된 최종 폴더에는 [CSV 원본](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/air_log.csv)이 제공됩니다.** 기존 기록 파일의 제공과 새 환경에서의 측정은 별개이며, 새 기록은 `OUTPUT_FILE`을 다른 이름으로 지정해 분리합니다.

#### LEVEL 3 · 데이터 구성

CSV는 PC 수신 시각과 센서 값 7개로 구성됩니다. `timestamp`는 PC의 로컬 시각이며 시간대 정보는 포함하지 않습니다.

| 열 | 의미 | 단위 |
| --- | --- | --- |
| `timestamp` | PC에서 데이터를 수신한 시각 | `YYYY-MM-DD HH:MM:SS` |
| `dht_temp_C` | DHT 온도 | °C |
| `dht_humi_pct` | DHT 상대습도 | % |
| `am_temp_C` | AM1008W-K 온도 | °C |
| `am_humi_pct` | AM1008W-K 상대습도 | % |
| `co2_ppm` | CO₂ | ppm |
| `voc_level` | VOC 단계 | 센서 단계 값 |
| `pm25_ugm3` | PM2.5 | µg/m³ |

수집기는 헤더, 열 개수가 잘못된 행, 숫자 또는 빈칸 이외의 값이 있는 행을 건너뜁니다. 일부 센서가 실패한 행은 정상 항목을 보존합니다.

원본 CSV의 첫 기록은 `2026-10-03 00:29:31`, 마지막 기록은 `2026-10-14 14:44:49`입니다. 이 범위가 중단 없는 연속 측정을 의미하지는 않습니다.

#### LEVEL 3 · 이 보관본의 의존성 목록

[requirements.txt](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/requirements.txt)의 실제 항목입니다. 외부 실행 도구와 GPU 드라이버는 별도로 준비합니다.

```text
pyserial
```

#### LEVEL 3 · 센서 프레임·등급·CSV 처리

`readAM1008W`는 I²C 주소 0x28에서 25바이트를 읽고 길이·0x16 헤더·앞 24바이트 XOR 체크섬을 검사합니다. 온도는 `(rawTemp-500)/10.0`, 습도는 `rawHumi/10.0`으로 바꿉니다. DHT11은 2번 핀, RGB는9/10/11번 핀, LCD는 0x27·16×2 설정입니다.

`showPage`는 DHT 온습도 →AM 온습도 →CO ₂/VOC/PM2.5 화면을 3초씩 순환합니다. `lcdLine`은 남은 16 칸을 공백으로 채워 잔상을 지웁니다. 센서 실패 화면과 실제 0 값은 구분합니다.

**항목:** 온도

**코드의 0·1·2·3 등급 판정 순서:** 20≤t<26 /18≤t<28 /15≤t<30 /그 밖

**항목:** 습도

**코드의 0·1·2·3 등급 판정 순서:** 40≤h≤60 /30≤h≤70 /20≤h≤80 /그 밖

**항목:** CO₂

**코드의 0·1·2·3 등급 판정 순서:** 800 미만/1000 미만/1500 미만/그 이상

**항목:** VOC

**코드의 0·1·2·3 등급 판정 순서:** 1 이하 →0,2 →1, 나머지 →2

**항목:** PM2.5

**코드의 0·1·2·3 등급 판정 순서:** 15 이하/35 이하/75 이하/그 이상


읽기에 성공한 모든 항목의 최대 등급을 초록·노랑·빨강·보라로 표시하고 둘 다 실패하면 LED를 끕니다. 이 값은 프로젝트의 표시 규칙입니다.

PC의 `parse_line`은 쉼표 7 필드, 각 필드 숫자 또는 빈 칸, 적어도 하나의 값 존재를 요구합니다.

헤더·잘못된 열 수·모두 빈 행은 버리고 일부 센서 실패는 빈 칸으로 보존합니다. `main`은 COM4·9600baud·timeout2초로 열고 2초 대기 후 수신 버퍼를 비웁니다. `air_log.csv`를 UTF-8 추가 모드로 열어 빈 파일일 때만 헤더를 쓰고, PC 수신 시각을 붙인 8 열을 매 행 flush합니다.

Ctrl +C 때 안내를 남기고 finally에서 포트를 닫습니다.

자동 재연결 루프는 이 수집기에 없습니다.

<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 3 · [CSV 파이썬 코드/pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py)

| 정의 | 소스에 적힌 역할 |
| --- | --- |
| [`is_number_or_blank`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L22) | 빈칸(센서 읽기 실패)이거나 숫자면 True.<br>헤더 줄 같은 문자열은 False. |
| [`parse_line`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L34) | 아두이노 한 줄 -&gt; 값 리스트.<br>형식이 맞지 않으면(헤더 줄, 깨진 줄 등) None. |

**설정·옵션:** [`PORT`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L6)

**코드의 선언:** `정의="COM4"`

**설정·옵션:** [`BAUD`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L7)

**코드의 선언:** `정의=9600`

**설정·옵션:** [`OUTPUT_FILE`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L8)

**코드의 선언:** `정의="air_log.csv"`

**설정·옵션:** [`COLUMNS`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L11)

**코드의 선언:** `정의=[     "dht_temp_C",     "dht_humi_pct",     "am_temp_C",     "am_humi_pct",     "co2_ppm",     "voc_level",     "pm25_ugm3", ]`


</details>

### LEVEL 3 · 실제 사용·실험 순서

1. 보드와 센서·LCD·RGB LED 배선을 확인합니다.
2. 이 차수 .ino를 업로드하고 실제 센서 출력을 확인합니다.
3. 수집기의 PORT를 실제 장치로 지정하고 OUTPUT_FILE을 새 기록 이름으로 정합니다.
4. Python 수집기를 실행해 헤더·열 수·시각·센서값을 확인합니다.

| 단계 | 내용 |
| --- | --- |
| 입력 | DHT 온습도·AM 온습도·CO₂·VOC·PM2.5 |
| 처리 | Arduino 센싱 → LCD·RGB LED → 9600 baud 시리얼 → Python 기록 |
| 출력 | air_log.csv: PC 시각과 7개 센서 값, 총 8 열 |

### LEVEL 3 · 결과와 실패를 확인하기

출력 CSV는 현재 작업 폴더에 누적됩니다. 새 측정은 OUTPUT_FILE을 다른 이름으로 지정해 기존 측정 원본과 분리합니다. timestamp는 PC 수신 시각이며 센서 자체 시각이나 중단 없는 연속 측정 보증이 아닙니다.

| 상황 | 확인할 내용 |
| --- | --- |
| 포트를 열지 못함 | PORT·USB 연결·다른 프로그램의 포트 점유를 확인합니다. |
| LCD 표시 오류 | 주소·배선·대비·라이브러리 init/backlight 지원을 확인합니다. |
| 측정 누락 | 센서 배선·종류와 수집기의 행 형식 조건을 확인합니다. |

### LEVEL 3 · 실행 전 대조할 차수 조건

DHT와 AM1008W-K를 함께 읽고 LCD의 DHT·AM 온습도·공기질 화면을 순환합니다.

읽기에 성공한 측정 항목 중 가장 높은 위험 등급을 RGB LED로 표시합니다. 전부 실패하면 LED를 끕니다.

parse_line은 센서 값 7 필드가 숫자 또는 빈 칸인지 확인합니다. 일부 실패는 빈 칸으로 보존하고 전부 빈 행은 제외합니다.

기본 포트 COM4, 9600 baud로 수신하고 UTF-8 air_log.csv에 PC 시각을 앞에 붙여 8 열로 저장합니다.

[자료 폴더](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85) · [직전 비교·자료 범위](step-2.patch) · [이 차수의 원래 전체 상세](#reading-level-5)

<a id="reading-level-4"></a>
## LEVEL 4 - Advanced

### LEVEL 4 · 설계 의도와 검토 경계

DHT와 AM1008W-K를 함께 읽고 LCD의 DHT·AM 온습도·공기질 화면을 순환합니다.

DHT와 AM1008W-K를 함께 읽고 LCD의 DHT·AM 온습도·공기질 화면을 순환합니다.

읽기에 성공한 측정 항목 중 가장 높은 위험 등급을 RGB LED로 표시합니다. 전부 실패하면 LED를 끕니다.

parse_line은 센서 값 7 필드가 숫자 또는 빈 칸인지 확인합니다. 일부 실패는 빈 칸으로 보존하고 전부 빈 행은 제외합니다.

기본 포트 COM4, 9600 baud로 수신하고 UTF-8 air_log.csv에 PC 시각을 앞에 붙여 8 열로 저장합니다.

### LEVEL 4 · 이 차수 구현의 실제 근거

| 파일 | 원문에 정의된 역할·구성 |
| --- | --- |
| [CSV 파이썬 코드/pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py) | 정의: `is_number_or_blank`, `parse_line`, `main` |
| [아두이노 코드/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/%EC%95%84%EB%91%90%EC%9D%B4%EB%85%B8%20%EC%BD%94%EB%93%9C/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino) | 소스 본문과 설정을 함께 읽는 구성요소 |

| 단계 | 내용 |
| --- | --- |
| 입력 | DHT 온습도·AM 온습도·CO₂·VOC·PM2.5 |
| 처리 | Arduino 센싱 → LCD·RGB LED → 9600 baud 시리얼 → Python 기록 |
| 출력 | air_log.csv: PC 시각과 7개 센서 값, 총 8 열 |

### LEVEL 4 · 조건·변경·결과를 함께 검토하기

DHT sensor library와 LiquidCrystal_I2C를 지원하는 Arduino IDE·보드·USB 포트를 준비합니다. Python에는 pyserial이 필요합니다. LCD의 I²C 주소와 실제 보드 SDA/SCL을 확인합니다.

Arduino 스케치를 보드에 업로드하고 시리얼 출력을 9600 baud로 확인합니다. 시리얼 모니터를 닫은 뒤 수집기 폴더에서 `python pc_csv_logger.py`로 기록하고 Ctrl +C로 끝냅니다.

#### LEVEL 4 · 이 차수 원래 안내의 세부 조건

#### LEVEL 4 · 저장소 구성

원본 최종 폴더의 세 파일을 폴더 구조 그대로 보관했습니다.

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── 아두이노 코드/
│   └── dht_am1008w_lcd_csv/
│       └── dht_am1008w_lcd_csv.ino
└── CSV 파이썬 코드/
    ├── pc_csv_logger.py
    └── air_log.csv
```

- [아두이노 스케치](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/%EC%95%84%EB%91%90%EC%9D%B4%EB%85%B8%20%EC%BD%94%EB%93%9C/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino): 센서 읽기, LCD 표시, LED 등급 판정, CSV 전송.
- [Python 수집기](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py): 데이터 형식 검사 및 타임스탬프를 포함한 CSV 저장.
- `air_log.csv`: 수집기를 실행하면 작업 위치에 생성되는 기록 파일입니다. **당시 안내에는 공개 저장소에 포함하지 않았다고 적혀 있지만, 현재 보존된 최종 폴더에는 [CSV 원본](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/air_log.csv)이 제공됩니다.** 기존 기록 파일의 제공과 새 환경에서의 측정은 별개이며, 새 기록은 `OUTPUT_FILE`을 다른 이름으로 지정해 분리합니다.

#### LEVEL 4 · 데이터 구성

CSV는 PC 수신 시각과 센서 값 7개로 구성됩니다. `timestamp`는 PC의 로컬 시각이며 시간대 정보는 포함하지 않습니다.

| 열 | 의미 | 단위 |
| --- | --- | --- |
| `timestamp` | PC에서 데이터를 수신한 시각 | `YYYY-MM-DD HH:MM:SS` |
| `dht_temp_C` | DHT 온도 | °C |
| `dht_humi_pct` | DHT 상대습도 | % |
| `am_temp_C` | AM1008W-K 온도 | °C |
| `am_humi_pct` | AM1008W-K 상대습도 | % |
| `co2_ppm` | CO₂ | ppm |
| `voc_level` | VOC 단계 | 센서 단계 값 |
| `pm25_ugm3` | PM2.5 | µg/m³ |

수집기는 헤더, 열 개수가 잘못된 행, 숫자 또는 빈칸 이외의 값이 있는 행을 건너뜁니다. 일부 센서가 실패한 행은 정상 항목을 보존합니다.

원본 CSV의 첫 기록은 `2026-10-03 00:29:31`, 마지막 기록은 `2026-10-14 14:44:49`입니다. 이 범위가 중단 없는 연속 측정을 의미하지는 않습니다.

#### LEVEL 4 · 이 보관본의 의존성 목록

[requirements.txt](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/requirements.txt)의 실제 항목입니다. 외부 실행 도구와 GPU 드라이버는 별도로 준비합니다.

```text
pyserial
```

#### LEVEL 4 · 센서 프레임·등급·CSV 처리

`readAM1008W`는 I²C 주소 0x28에서 25바이트를 읽고 길이·0x16 헤더·앞 24바이트 XOR 체크섬을 검사합니다. 온도는 `(rawTemp-500)/10.0`, 습도는 `rawHumi/10.0`으로 바꿉니다. DHT11은 2번 핀, RGB는9/10/11번 핀, LCD는 0x27·16×2 설정입니다.

`showPage`는 DHT 온습도 →AM 온습도 →CO ₂/VOC/PM2.5 화면을 3초씩 순환합니다. `lcdLine`은 남은 16 칸을 공백으로 채워 잔상을 지웁니다. 센서 실패 화면과 실제 0 값은 구분합니다.

**항목:** 온도

**코드의 0·1·2·3 등급 판정 순서:** 20≤t<26 /18≤t<28 /15≤t<30 /그 밖

**항목:** 습도

**코드의 0·1·2·3 등급 판정 순서:** 40≤h≤60 /30≤h≤70 /20≤h≤80 /그 밖

**항목:** CO₂

**코드의 0·1·2·3 등급 판정 순서:** 800 미만/1000 미만/1500 미만/그 이상

**항목:** VOC

**코드의 0·1·2·3 등급 판정 순서:** 1 이하 →0,2 →1, 나머지 →2

**항목:** PM2.5

**코드의 0·1·2·3 등급 판정 순서:** 15 이하/35 이하/75 이하/그 이상


읽기에 성공한 모든 항목의 최대 등급을 초록·노랑·빨강·보라로 표시하고 둘 다 실패하면 LED를 끕니다. 이 값은 프로젝트의 표시 규칙입니다.

PC의 `parse_line`은 쉼표 7 필드, 각 필드 숫자 또는 빈 칸, 적어도 하나의 값 존재를 요구합니다.

헤더·잘못된 열 수·모두 빈 행은 버리고 일부 센서 실패는 빈 칸으로 보존합니다. `main`은 COM4·9600baud·timeout2초로 열고 2초 대기 후 수신 버퍼를 비웁니다. `air_log.csv`를 UTF-8 추가 모드로 열어 빈 파일일 때만 헤더를 쓰고, PC 수신 시각을 붙인 8 열을 매 행 flush합니다.

Ctrl +C 때 안내를 남기고 finally에서 포트를 닫습니다.

자동 재연결 루프는 이 수집기에 없습니다.

<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

#### LEVEL 4 · [CSV 파이썬 코드/pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py)

| 정의 | 소스에 적힌 역할 |
| --- | --- |
| [`is_number_or_blank`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L22) | 빈칸(센서 읽기 실패)이거나 숫자면 True.<br>헤더 줄 같은 문자열은 False. |
| [`parse_line`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L34) | 아두이노 한 줄 -&gt; 값 리스트.<br>형식이 맞지 않으면(헤더 줄, 깨진 줄 등) None. |

**설정·옵션:** [`PORT`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L6)

**코드의 선언:** `정의="COM4"`

**설정·옵션:** [`BAUD`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L7)

**코드의 선언:** `정의=9600`

**설정·옵션:** [`OUTPUT_FILE`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L8)

**코드의 선언:** `정의="air_log.csv"`

**설정·옵션:** [`COLUMNS`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L11)

**코드의 선언:** `정의=[     "dht_temp_C",     "dht_humi_pct",     "am_temp_C",     "am_humi_pct",     "co2_ppm",     "voc_level",     "pm25_ugm3", ]`


</details>

출력 CSV는 현재 작업 폴더에 누적됩니다. 새 측정은 OUTPUT_FILE을 다른 이름으로 지정해 기존 측정 원본과 분리합니다. timestamp는 PC 수신 시각이며 센서 자체 시각이나 중단 없는 연속 측정 보증이 아닙니다.

| 상황 | 확인할 내용 |
| --- | --- |
| 포트를 열지 못함 | PORT·USB 연결·다른 프로그램의 포트 점유를 확인합니다. |
| LCD 표시 오류 | 주소·배선·대비·라이브러리 init/backlight 지원을 확인합니다. |
| 측정 누락 | 센서 배선·종류와 수집기의 행 형식 조건을 확인합니다. |

### LEVEL 4 · 재현과 전체 비교

1. 보드와 센서·LCD·RGB LED 배선을 확인합니다.
2. 이 차수 .ino를 업로드하고 실제 센서 출력을 확인합니다.
3. 수집기의 PORT를 실제 장치로 지정하고 OUTPUT_FILE을 새 기록 이름으로 정합니다.
4. Python 수집기를 실행해 헤더·열 수·시각·센서값을 확인합니다.

위 구성요소의 입력·출력과 실패 조건을 같은 차수 소스에 연결해 검토합니다. 전체 비교는 추가·수정·삭제와 원래 보관 범위를 구분하는 근거입니다.

[자료 폴더](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85) · [직전 비교·자료 범위](step-2.patch) · [이 차수의 원래 전체 상세](#reading-level-5)
<a id="reading-level-5"></a>
## LEVEL 5 - Expert

기존의 전체 설명·표·코드·함수 참조·파일별 비교는 아래에 그대로 이어집니다. [자료 폴더](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85) · [직전 비교·자료 범위](step-2.patch) · [이 차수의 원래 전체 상세](#reading-level-5)
<!-- reading-levels:end -->


[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85) · [← 이전: 1차](step-1.md)

<a name="-목적과-이-차수의-역할"></a>
## 목적과 이 차수의 역할

DHT와 AM1008W-K를 함께 읽고 LCD의 DHT·AM 온습도·공기질 화면을 순환합니다.

<a name="features"></a>

<a name="-핵심-기능과-보존-범위"></a>
## 핵심 기능과 보존 범위

**항목:** 1

**이 차수에서 확인할 내용:** DHT와 AM1008W-K를 함께 읽고 LCD의 DHT·AM 온습도·공기질 화면을 순환합니다.

**항목:** 2

**이 차수에서 확인할 내용:** 읽기에 성공한 측정 항목 중 가장 높은 위험 등급을 RGB LED로 표시합니다. 전부 실패하면 LED를 끕니다.

**항목:** 3

**이 차수에서 확인할 내용:** parse_line은 센서 값 7 필드가 숫자 또는 빈 칸인지 확인합니다. 일부 실패는 빈 칸으로 보존하고 전부 빈 행은 제외합니다.

**항목:** 4

**이 차수에서 확인할 내용:** 기본 포트 COM4, 9600 baud로 수신하고 UTF-8 air_log.csv에 PC 시각을 앞에 붙여 8 열로 저장합니다.


<a name="-입력처리출력"></a>
## 입력·처리·출력

| 단계 | 내용 |
| --- | --- |
| 입력 | DHT 온습도·AM 온습도·CO₂·VOC·PM2.5 |
| 처리 | Arduino 센싱 → LCD·RGB LED → 9600 baud 시리얼 → Python 기록 |
| 출력 | air_log.csv: PC 시각과 7개 센서 값, 총 8 열 |

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

| 경로 | 자료 종류 |
| --- | --- |
| [CSV 파이썬 코드/](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C) | 하위 자료 폴더 |
| [아두이노 코드/](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/%EC%95%84%EB%91%90%EC%9D%B4%EB%85%B8%20%EC%BD%94%EB%93%9C) | 하위 자료 폴더 |
| [.gitignore](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/.gitignore) | 파일 |
| [README.md](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/README.md) | MD 파일 |
| [requirements.txt](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/requirements.txt) | TXT 파일 |

<a name="-주요-모듈과-코드-읽기"></a>
## 주요 모듈과 코드 읽기

| 파일 | 원문에 정의된 역할·구성 |
| --- | --- |
| [CSV 파이썬 코드/pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py) | 정의: `is_number_or_blank`, `parse_line`, `main` |
| [아두이노 코드/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/%EC%95%84%EB%91%90%EC%9D%B4%EB%85%B8%20%EC%BD%94%EB%93%9C/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino) | 소스 본문과 설정을 함께 읽는 구성요소 |

<a name="setup"></a>

<a name="-설치-환경과-실행사용법"></a>
## 설치 환경과 실행·사용법

DHT sensor library와 LiquidCrystal_I2C를 지원하는 Arduino IDE·보드·USB 포트를 준비합니다. Python에는 pyserial이 필요합니다. LCD의 I²C 주소와 실제 보드 SDA/SCL을 확인합니다.

Arduino 스케치를 보드에 업로드하고 시리얼 출력을 9600 baud로 확인합니다. 시리얼 모니터를 닫은 뒤 수집기 폴더에서 `python pc_csv_logger.py`로 기록하고 Ctrl +C로 끝냅니다.

<a name="-이-차수-원래-안내의-세부-조건"></a>
### 이 차수 원래 안내의 세부 조건

<a name="-저장소-구성"></a>
### 저장소 구성

원본 최종 폴더의 세 파일을 폴더 구조 그대로 보관했습니다.

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── 아두이노 코드/
│   └── dht_am1008w_lcd_csv/
│       └── dht_am1008w_lcd_csv.ino
└── CSV 파이썬 코드/
    ├── pc_csv_logger.py
    └── air_log.csv
```

- [아두이노 스케치](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/%EC%95%84%EB%91%90%EC%9D%B4%EB%85%B8%20%EC%BD%94%EB%93%9C/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino): 센서 읽기, LCD 표시, LED 등급 판정, CSV 전송.
- [Python 수집기](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py): 데이터 형식 검사 및 타임스탬프를 포함한 CSV 저장.
- `air_log.csv`: 당시 원래 안내에는 공개 저장소에 포함하지 않는다고 적혀 있었습니다. 현재는 `코드/최종/CSV 파이썬 코드/air_log.csv`에 당시 측정 원본을 보존합니다. 새 측정은 다른 `OUTPUT_FILE` 이름으로 분리합니다.

<a name="-데이터-구성"></a>
### 데이터 구성

CSV는 PC 수신 시각과 센서 값 7개로 구성됩니다. `timestamp`는 PC의 로컬 시각이며 시간대 정보는 포함하지 않습니다.

| 열 | 의미 | 단위 |
| --- | --- | --- |
| `timestamp` | PC에서 데이터를 수신한 시각 | `YYYY-MM-DD HH:MM:SS` |
| `dht_temp_C` | DHT 온도 | °C |
| `dht_humi_pct` | DHT 상대습도 | % |
| `am_temp_C` | AM1008W-K 온도 | °C |
| `am_humi_pct` | AM1008W-K 상대습도 | % |
| `co2_ppm` | CO₂ | ppm |
| `voc_level` | VOC 단계 | 센서 단계 값 |
| `pm25_ugm3` | PM2.5 | µg/m³ |

수집기는 헤더, 열 개수가 잘못된 행, 숫자 또는 빈칸 이외의 값이 있는 행을 건너뜁니다. 일부 센서가 실패한 행은 정상 항목을 보존합니다.

원본 CSV의 첫 기록은 `2026-10-03 00:29:31`, 마지막 기록은 `2026-10-14 14:44:49`입니다. 이 범위가 중단 없는 연속 측정을 의미하지는 않습니다.

<a name="-이-보관본의-의존성-목록"></a>
### 이 보관본의 의존성 목록

[requirements.txt](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/requirements.txt)의 실제 항목입니다. 외부 실행 도구와 GPU 드라이버는 별도로 준비합니다.

```text
pyserial
```

### 센서 프레임·등급·CSV 처리

`readAM1008W`는 I²C 주소 0x28에서 25바이트를 읽고 길이·0x16 헤더·앞 24바이트 XOR 체크섬을 검사합니다. 온도는 `(rawTemp-500)/10.0`, 습도는 `rawHumi/10.0`으로 바꿉니다. DHT11은 2번 핀, RGB는9/10/11번 핀, LCD는 0x27·16×2 설정입니다.

`showPage`는 DHT 온습도 →AM 온습도 →CO ₂/VOC/PM2.5 화면을 3초씩 순환합니다. `lcdLine`은 남은 16 칸을 공백으로 채워 잔상을 지웁니다. 센서 실패 화면과 실제 0 값은 구분합니다.

**항목:** 온도

**코드의 0·1·2·3 등급 판정 순서:** 20≤t<26 /18≤t<28 /15≤t<30 /그 밖

**항목:** 습도

**코드의 0·1·2·3 등급 판정 순서:** 40≤h≤60 /30≤h≤70 /20≤h≤80 /그 밖

**항목:** CO₂

**코드의 0·1·2·3 등급 판정 순서:** 800 미만/1000 미만/1500 미만/그 이상

**항목:** VOC

**코드의 0·1·2·3 등급 판정 순서:** 1 이하 →0,2 →1, 나머지 →2

**항목:** PM2.5

**코드의 0·1·2·3 등급 판정 순서:** 15 이하/35 이하/75 이하/그 이상


읽기에 성공한 모든 항목의 최대 등급을 초록·노랑·빨강·보라로 표시하고 둘 다 실패하면 LED를 끕니다. 이 값은 프로젝트의 표시 규칙입니다.

PC의 `parse_line`은 쉼표 7 필드, 각 필드 숫자 또는 빈 칸, 적어도 하나의 값 존재를 요구합니다.

헤더·잘못된 열 수·모두 빈 행은 버리고 일부 센서 실패는 빈 칸으로 보존합니다. `main`은 COM4·9600baud·timeout2초로 열고 2초 대기 후 수신 버퍼를 비웁니다. `air_log.csv`를 UTF-8 추가 모드로 열어 빈 파일일 때만 헤더를 쓰고, PC 수신 시각을 붙인 8 열을 매 행 flush합니다.

Ctrl +C 때 안내를 남기고 finally에서 포트를 닫습니다.

자동 재연결 루프는 이 수집기에 없습니다.

<details>
<summary>함수 역할·기본값·입력 거부 조건의 세부 참조</summary>

다음 항목은 이 자료의 Python 소스에 명시된 선언입니다. 전체 분기와 호출 순서는 각 행의 코드 위치에서 이어서 읽을 수 있습니다.

### [CSV 파이썬 코드/pc_csv_logger.py](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py)

| 정의 | 소스에 적힌 역할 |
| --- | --- |
| [`is_number_or_blank`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L22) | 빈칸(센서 읽기 실패)이거나 숫자면 True.<br>헤더 줄 같은 문자열은 False. |
| [`parse_line`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L34) | 아두이노 한 줄 -&gt; 값 리스트.<br>형식이 맞지 않으면(헤더 줄, 깨진 줄 등) None. |

**설정·옵션:** [`PORT`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L6)

**코드의 선언:** `정의="COM4"`

**설정·옵션:** [`BAUD`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L7)

**코드의 선언:** `정의=9600`

**설정·옵션:** [`OUTPUT_FILE`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L8)

**코드의 선언:** `정의="air_log.csv"`

**설정·옵션:** [`COLUMNS`](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85/CSV%20%ED%8C%8C%EC%9D%B4%EC%8D%AC%20%EC%BD%94%EB%93%9C/pc_csv_logger.py#L11)

**코드의 선언:** `정의=[     "dht_temp_C",     "dht_humi_pct",     "am_temp_C",     "am_humi_pct",     "co2_ppm",     "voc_level",     "pm25_ugm3", ]`


</details>

<a name="results"></a>

<a name="-처리-결과와-출력-읽기"></a>
## 처리 결과와 출력 읽기

출력 CSV는 현재 작업 폴더에 누적됩니다. 새 측정은 OUTPUT_FILE을 다른 이름으로 지정해 기존 측정 원본과 분리합니다. timestamp는 PC 수신 시각이며 센서 자체 시각이나 중단 없는 연속 측정 보증이 아닙니다.

<a name="️-제약과-문제-해결"></a>
## 제약과 문제 해결

| 상황 | 확인할 내용 |
| --- | --- |
| 포트를 열지 못함 | PORT·USB 연결·다른 프로그램의 포트 점유를 확인합니다. |
| LCD 표시 오류 | 주소·배선·대비·라이브러리 init/backlight 지원을 확인합니다. |
| 측정 누락 | 센서 배선·종류와 수집기의 행 형식 조건을 확인합니다. |

<a name="changes"></a>

<a name="-직전-자료와-전체-비교"></a>
## 직전 자료와 전체 비교

1차에서 최종로 이어지는 실제 파일 비교입니다.

[전체 비교·자료 범위](step-2.patch)

추가·수정·삭제, 주석·공백·개행과 바이너리 크기·해시는 연결된 원래 비교 자료에서 확인합니다.

<details>
<summary>파일별 비교·크기·해시 자세히 보기</summary>

[전체 텍스트 차이](step-2.patch) · [파일별 크기·SHA-256](step-2-files.json)

| 구분 | 파일 |
| --- | --- |
| 추가 | `.gitignore` |
| 추가 | `CSV 파이썬 코드/air_log.csv` |
| 추가 | `CSV 파이썬 코드/pc_csv_logger.py` |
| 추가 | `README.md` |
| 추가 | `requirements.txt` |
| 추가 | `아두이노 코드/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino` |
| 이전에만 존재 | `dht_lcd_rgb_csv/dht_lcd_rgb_csv.ino` |
| 이전에만 존재 | `dht_log.csv` |
| 이전에만 존재 | `pc_csv_logger.py` |

</details>

[프로젝트](../../README.md) · [전체 차수](../REVISION_INDEX.md) · [원본 자료](../../%EC%BD%94%EB%93%9C/%EC%B5%9C%EC%A2%85) · [← 이전: 1차](step-1.md)
