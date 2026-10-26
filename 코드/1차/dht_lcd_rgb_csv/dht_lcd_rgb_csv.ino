#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11   // DHT22를 쓴다면 DHT22로 변경

#define RED_PIN 9
#define GREEN_PIN 10
#define BLUE_PIN 11

LiquidCrystal_I2C lcd(0x27, 16, 2);  // 화면이 안 나오면 0x3F로 변경
DHT dht(DHTPIN, DHTTYPE);

void setColor(bool r, bool g, bool b) {
  digitalWrite(RED_PIN, r ? HIGH : LOW);
  digitalWrite(GREEN_PIN, g ? HIGH : LOW);
  digitalWrite(BLUE_PIN, b ? HIGH : LOW);
}

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  dht.begin();

  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  setColor(0, 0, 0);

  lcd.setCursor(0, 0);
  lcd.print("Ready");
  delay(1000);
  lcd.clear();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    lcd.setCursor(0, 0);
    lcd.print("Sensor Error   ");
    setColor(0, 0, 0);
    delay(1000);
    return;
  }

  // LCD 표시
  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(t, 1);
  lcd.write(223); // 도(degree) 기호
  lcd.print("C       ");

  lcd.setCursor(0, 1);
  lcd.print("H:");
  lcd.print(h, 1);
  lcd.print("%       ");

  // 온도에 따라 RGB LED 색 변경 (높은 온도 조건 우선 적용)
  if (t >= 28.0) {
    setColor(0, 0, 1);       // 28도 이상: 파란불
  } else if (t >= 27.5) {
    setColor(1, 0, 0);       // 27.5~28도: 빨간불
  } else if (t >= 27.4) {
    setColor(0, 1, 0);       // 27.4~27.5도: 초록불
  } else {
    setColor(0, 0, 0);       // 27.4도 미만: 꺼짐
  }

  // PC로 CSV 형식 전송: 온도,습도
  Serial.print(t, 1);
  Serial.print(",");
  Serial.println(h, 1);

  delay(1000);
}
