#include <WiFi.h>
#include <ThingSpeak.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// WiFi 설정
const char* ssid = "hwang_wifi";
const char* password = "202110748";

// ThingSpeak 설정
unsigned long channelID = 2726168;
const char* writeAPIKey = "GITGMUVXH6B46SD4";
const char* readAPIKey = "3CTBI0MAX1DWDU2I";

// 핀 설정
#define DHTPIN 26
#define DHTTYPE DHT22
#define SDA_PIN 14
#define SCL_PIN 15
#define RELAY_PIN 32
#define LED_PIN 33

// 객체 초기화
DHT_Unified dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27, 20, 4);
WiFiClient client;

// 시간 관리 변수
unsigned long lastDataTime = 0;
unsigned long lastControlTime = 0;

// LCD 초기화 코드
void lcdSetUp() {
  Wire.begin(SDA_PIN, SCL_PIN);
  lcd.init();

  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("Welcome...");
  lcd.setCursor(0,1);
  lcd.print("Green Friend!");
}

// DHT22센서에 관한 정보를 print하는 함수
// DHT22 Example 코드의 setup 함수의 센서정보를 print 하는 코드들만 따로 분리 (34-56)
void setupDHT22() {
  Serial.println(F("DHTxx Unified Sensor Example"));
  // Print temperature sensor details.
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  Serial.println(F("------------------------------------"));
  Serial.println(F("Temperature Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("°C"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("°C"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("°C"));
  Serial.println(F("------------------------------------"));
  // Print humidity sensor details.
  dht.humidity().getSensor(&sensor);
  Serial.println(F("Humidity Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("%"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("%"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("%"));
  Serial.println(F("------------------------------------"));
  // Set delay between sensor readings based on sensor details.
}

// WiFi 연결 함수
void setupWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");
  
  // ThingSpeak 초기화
  ThingSpeak.begin(client);
}

// 센서 데이터 읽기 및 전송
void sendSensorData() {
  sensors_event_t event;
  float temperature = 0;
  float humidity = 0;
  
  // 온도 읽기
  dht.temperature().getEvent(&event);
  if (!isnan(event.temperature)) {
    temperature = event.temperature;
    Serial.print(F("Temperature: "));
    Serial.print(temperature);
    Serial.println(F("°C"));
    
    lcd.setCursor(0,0);
    lcd.print("Temp: ");
    lcd.print(temperature);
    lcd.print(" C");
  }
  
  // 습도 읽기
  dht.humidity().getEvent(&event);
  if (!isnan(event.relative_humidity)) {
    humidity = event.relative_humidity;
    Serial.print(F("Humidity: "));
    Serial.print(humidity);
    Serial.println(F("%"));
    
    lcd.setCursor(0,1);
    lcd.print("Humid: ");
    lcd.print(humidity);
    lcd.print("%");
  }
  
  // ThingSpeak로 데이터 전송
  ThingSpeak.setField(1, temperature);
  ThingSpeak.setField(2, humidity);
  
  int response = ThingSpeak.writeFields(channelID, writeAPIKey);
  if (response == 200) {
    Serial.println("Data sent to ThingSpeak");
  } else {
    Serial.println("Error sending data");
  }
}

// LED와 릴레이 상태 확인 및 제어
void checkControl() {
  int controlValue = ThingSpeak.readFloatField(channelID, 3, readAPIKey);
  
  if(controlValue != -1) {
    digitalWrite(LED_PIN, controlValue);
    digitalWrite(RELAY_PIN, controlValue);
    Serial.print("Control state changed to: ");
    Serial.println(controlValue);
  }
}

void setup() {
  Serial.begin(115200);
  
  // 핀 모드 설정
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  
  // 초기화
  dht.begin();
  lcdSetUp();
  setupDHT22();
  setupWiFi();
}

void loop() {
  unsigned long currentTime = millis();
  
  // 15초마다 센서 데이터 전송
  if (currentTime - lastDataTime >= 15000) {
    sendSensorData();
    lastDataTime = currentTime;
  }
  
  // 2초마다 제어 상태 확인
  if (currentTime - lastControlTime >= 2000) {
    checkControl();
    lastControlTime = currentTime;
  }
}