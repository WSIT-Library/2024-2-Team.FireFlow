//YWROBOT
//Compatible with the Arduino IDE 1.0
//Library version:1.1
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#define SDA_PIN 14
#define SCL_PIN 15

LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display

// LCD 초기화 코드
void lcdSetUp() {
  Wire.begin(SDA_PIN, SCL_PIN);
  Serial.begin(115200);
  lcd.init();

  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("Welcome...");
  lcd.setCursor(0,1);
  lcd.print("Green Friend!");
}


void setup()
{
  // Print a message to the LCD.
  // lcd.setCursor(0,0);
  // lcd.print("Welcome,");
  // lcd.setCursor(0,1);
  // lcd.print("Green Friend!");
  lcdSetUp();
}


void loop()
{
}
