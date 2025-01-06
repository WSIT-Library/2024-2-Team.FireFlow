#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

#define DHTPIN 26 
#define DHTTYPE    DHT22
#define SDA_PIN 14
#define SCL_PIN 15


DHT_Unified dht(DHTPIN, DHTTYPE);
LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display


int Relay = 32;
int led = 33;

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

void setup() {
  // put your setup code here, to run once:sharon
  //pinMode(Relay, OUTPUT);
  Serial.begin(115200);
  dht.begin();
  pinMode(led, OUTPUT);
  pinMode(Relay, OUTPUT);
  lcdSetUp();

  // DHT22 센서에 관한 정보를 PC모니터에 보여준다
  setupDHT22();
}


// 온습도센서가 측정하고 있는 데이터를 컴퓨터 pc에 print
// DHT22 Example 코드의 loop함수 내부에 있는 코드를 함수로 따로 분리
void checkDHT22() {
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));
  }
  else {
    Serial.print(F("Temperature: "));
    Serial.print(event.temperature);
    Serial.println(F("°C"));

    // lcd 출력
    lcd.setCursor(0,0);
    lcd.print("Temp: ");
    lcd.print(event.temperature);
    lcd.print(" C");
  }
  // Get humidity event and print its value.
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!"));
  }
  else {
    Serial.print(F("Humidity: "));
    Serial.print(event.relative_humidity);
    Serial.println(F("%"));
        
    // lcd 출력 
    lcd.setCursor(0,1);
    lcd.print("Humid: ");
    lcd.print(event.relative_humidity);
    lcd.print("%");
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  // led, 릴레이 ON
  digitalWrite(Relay, HIGH);
  digitalWrite(led, HIGH); 
  checkDHT22();

  delay(5000);

  // led, 릴레이 off
  digitalWrite(Relay, LOW);
  digitalWrite(led, LOW);
  checkDHT22();

  delay(5000);
}