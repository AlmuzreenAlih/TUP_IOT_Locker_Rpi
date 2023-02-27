#define Button1 (2)
#define Button2 (3)
#define Button3 (4)
#define Button4 (5)
#define Button5 (6)

// #define Motor (3)

#include <millisDelay.h>
millisDelay Timer1;

#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,20,4);

void setup() {
    Serial.begin(9600);
    //Buttons
    pinMode(Button1, INPUT_PULLUP);
    pinMode(Button2, INPUT_PULLUP);
    pinMode(Button3, INPUT_PULLUP);
    pinMode(Button4, INPUT_PULLUP);
    pinMode(Button5, INPUT_PULLUP);

    //Relays
    // pinMode(Motor, OUTPUT); digitalWrite(Motor, HIGH);

    // lcd.init();
    // lcd.backlight();
}

char receivedChar;
void loop() {
    if (Serial.available()) {
        receivedChar = Serial.read();
             if (receivedChar == '1') {}
    }
    receivedChar = ' ';

    if (digitalRead(Button1) == 0) {Serial.println("A"); delay(2000);}
    if (digitalRead(Button2) == 0) {Serial.println("B"); delay(2000);}
    if (digitalRead(Button3) == 0) {Serial.println("X"); delay(2000);}
    if (digitalRead(Button4) == 0) {Serial.println("Y"); delay(2000);}
    if (digitalRead(Button5) == 0) {Serial.println("Z"); delay(2000);}
}

void ToggleLH(long delayings, int relayName) {
    digitalWrite(relayName, LOW); delay(delayings);
    digitalWrite(relayName, HIGH);
}

void ToggleHL(long delayings, int relayName) {
    digitalWrite(relayName, HIGH); delay(delayings);
    digitalWrite(relayName, LOW);
}

void RelayLOWwithLimit(int relayName, int MSName) {
    if (digitalRead(MSName) == 1){
        digitalWrite(relayName, LOW); delay(50);
        while(1) {if (digitalRead(MSName) == 0) {break;}}
        digitalWrite(relayName, HIGH);
    }
}

void LCDprint(int x, int y, String z) {
    lcd.setCursor(x,y); lcd.print(z);
}

void LCDClear() {
    LCDprint(0,0,"					");
    LCDprint(0,1,"					");
    LCDprint(0,2,"					");
    LCDprint(0,3,"					");
}