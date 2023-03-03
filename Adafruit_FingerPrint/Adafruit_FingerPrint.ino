#include <Adafruit_Fingerprint.h>

#if (defined(__AVR__) || defined(ESP8266)) && !defined(__AVR_ATmega2560__)
// For UNO and others without hardware serial, we must use software serial...
// pin #2 is IN from sensor (GREEN wire)
// pin #3 is OUT from arduino  (WHITE wire)
// Set up the serial port to use softwareserial..
SoftwareSerial mySerial(2, 3);

#else
// On Leonardo/M0/etc, others with hardware serial, use hardware serial!
// #0 is green wire, #1 is white
#define mySerial Serial3

#endif

Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);
int debug = 0;
void setup() {
    Serial.begin(9600); while (!Serial); delay(100);
    DBG("\n\nAdafruit finger detect test");

    finger.begin(57600); delay(5);
    if (finger.verifyPassword()) {
        Serial.println("Found fingerprint sensor!");
    } else {
        Serial.println("Did not find fingerprint sensor :(");
        while (1) { delay(1); }
    }
    Serial.println("Z");
    finger.getParameters();

    if (debug == 1) {
        Serial.println(F("Reading sensor parameters"));
        Serial.print(F("Status: 0x")); Serial.println(finger.status_reg, HEX);
        Serial.print(F("Sys ID: 0x")); Serial.println(finger.system_id, HEX);
        Serial.print(F("Capacity: ")); Serial.println(finger.capacity);
        Serial.print(F("Security level: ")); Serial.println(finger.security_level);
        Serial.print(F("Device address: ")); Serial.println(finger.device_addr, HEX);
        Serial.print(F("Packet len: ")); Serial.println(finger.packet_len);
        Serial.print(F("Baud rate: ")); Serial.println(finger.baud_rate);
    }
    finger.getTemplateCount();

    if (debug == 1) {
        if (finger.templateCount == 0) {
            Serial.print("Sensor doesn't contain any fingerprint data. Please run the 'enroll' example.");
        } else {
            Serial.println("Waiting for valid finger...");
            Serial.print("Sensor contains "); Serial.print(finger.templateCount); Serial.println(" templates");
        }
    }   
}
uint8_t id;

void loop() {
    //LOGIN: Fingerprint Wait
    getFingerprintIDez(); delay(50);

    //REGISTER: Serial Fingerprint ID to register
    if (Serial.available()) {
        id = Serial.parseInt(); delay(500);
        getFingerprintEnroll();
        while (Serial.available()) {Serial.read();}
    }
}

uint8_t getFingerprintID() {
    uint8_t p = finger.getImage();
    switch (p) {
    case FINGERPRINT_OK:
        DBG("Image taken");
        break;
    case FINGERPRINT_NOFINGER:
        DBG("No finger detected");
        return p;
    case FINGERPRINT_PACKETRECIEVEERR:
        DBG("Communication error");
        return p;
    case FINGERPRINT_IMAGEFAIL:
        DBG("Imaging error");
        return p;
    default:
        DBG("Unknown error");
        return p;
    }

  // OK success!

    p = finger.image2Tz();
    switch (p) {
    case FINGERPRINT_OK:
        DBG("Image converted");
        break;
    case FINGERPRINT_IMAGEMESS:
        DBG("Image too messy");
        return p;
    case FINGERPRINT_PACKETRECIEVEERR:
        DBG("Communication error");
        return p;
    case FINGERPRINT_FEATUREFAIL:
        DBG("Could not find fingerprint features");
        return p;
    case FINGERPRINT_INVALIDIMAGE:
        DBG("Could not find fingerprint features");
        return p;
    default:
        DBG("Unknown error");
        return p;
    }

    // OK converted!
    p = finger.fingerSearch();
    if (p == FINGERPRINT_OK) {
        DBG("Found a print match!");
    } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
        DBG("Communication error");
        return p;
    } else if (p == FINGERPRINT_NOTFOUND) {
        DBG("Did not find a match");
        return p;
    } else {
        DBG("Unknown error");
        return p;
    }

    // found a match!
    Serial.print("Found ID #"); //
    Serial.print(finger.fingerID);
    Serial.print(" with confidence of "); Serial.println(finger.confidence);//

    return finger.fingerID; // returns -1 if failed, otherwise returns ID #
}


int getFingerprintIDez() {
    uint8_t p = finger.getImage();
    if (p != FINGERPRINT_OK)  return -1;

    p = finger.image2Tz();
    if (p != FINGERPRINT_OK)  return -1;

    p = finger.fingerFastSearch();
    if (p != FINGERPRINT_OK)  return -1;

    // found a match!
    // Serial.print("Found ID #"); 
    Serial.print(finger.fingerID);
    // Serial.print(" with confidence of "); Serial.println(finger.confidence);
    return finger.fingerID;
}

// int debug = 1;
void DBG(String str) {
    if (debug) {Serial.println(str);}
}

// // uint8_t readnumber(void) {
// //   uint8_t num = 0;

// //   while (num == 0) {
// //     while (! Serial.available());
// //     num = Serial.parseInt();
// //   }
// //   return num;
// // }

// // void loop() {
// //     if (Serial.available()) {
// //         id = Serial.parseInt(); delay(500);
// //         while (!getFingerprintEnroll());
// //     }
// // }

uint8_t getFingerprintEnroll() {
    int p = -1;
    // Serial.print("Waiting for valid finger to enroll as #"); Serial.println(id);
    while (p != FINGERPRINT_OK) {
        p = finger.getImage();
        switch (p) {
            case FINGERPRINT_OK:
                // Serial.println("Image taken");
                // Serial.println("A");
                break; //broken since "while not"
            // case FINGERPRINT_NOFINGER:
            //     // Serial.println(".");
            //     break;
            // case FINGERPRINT_PACKETRECIEVEERR:
            //     // Serial.println("Communication error");
            //     break;
            // case FINGERPRINT_IMAGEFAIL:
            //     // Serial.println("Imaging error");
            //     break;
            default:
                // Serial.println("An Error");
                // Serial.println("X");
                break;
        }
    }

  // OK success!

    p = finger.image2Tz(1);
    switch (p) {
        case FINGERPRINT_OK:
            // Serial.println("Image converted");
            break;
        // case FINGERPRINT_IMAGEMESS:
        //     // Serial.println("Image too messy");
        //     return p;
        // case FINGERPRINT_PACKETRECIEVEERR:
        //     // Serial.println("Communication error");
        //     return p;
        // case FINGERPRINT_FEATUREFAIL:
        //     // Serial.println("Could not find fingerprint features");
        //     return p;
        // case FINGERPRINT_INVALIDIMAGE:
        //     // Serial.println("Could not find fingerprint features");
        //     return p;
        default:
            // Serial.println("An Error");
            Serial.println("Z");
            return -1;
    }

    // Serial.println("Remove Finger"); 
    Serial.println("A"); delay(2000);
    p = 0;
    while (p != FINGERPRINT_NOFINGER) {
        p = finger.getImage();
    }

    //Serial.print("ID "); Serial.println(id);
    p = -1;
    // Serial.println("Place same finger again");
    Serial.println("Y");

    while (p != FINGERPRINT_OK) {
        p = finger.getImage();
        switch (p) {
            case FINGERPRINT_OK:
                // Serial.println("Image taken");
                // Serial.println("B");
                break;
            // case FINGERPRINT_NOFINGER:
            //     // Serial.print(".");
            //     break;
            // case FINGERPRINT_PACKETRECIEVEERR:
            //     // Serial.println("Communication error");
            //     break;
            // case FINGERPRINT_IMAGEFAIL:
            //     // Serial.println("Imaging error");
            //     break;
            default:
                // Serial.println("An Error");
                // Serial.println("X");
                break;
        }
    }

  // OK success!

    p = finger.image2Tz(2);
    switch (p) {
        case FINGERPRINT_OK:
            // Serial.println("Image converted");
            break;
        // case FINGERPRINT_IMAGEMESS:
        //     // Serial.println("Image too messy");
        //     return p;
        // case FINGERPRINT_PACKETRECIEVEERR:
        //     // Serial.println("Communication error");
        //     return p;
        // case FINGERPRINT_FEATUREFAIL:
        //     // Serial.println("Could not find fingerprint features");
        //     return p;
        // case FINGERPRINT_INVALIDIMAGE:
        //     // Serial.println("Could not find fingerprint features");
        //     return p;
        default:
            // Serial.println("Unknown error");
            Serial.println("Z");
            return p;
    }

  // OK converted!
// //   Serial.print("Creating model for #");  Serial.println(id);

    p = finger.createModel();
    if (p == FINGERPRINT_OK) {
        // Serial.println("Prints matched!");
    } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
        // Serial.println("Communication error");
        Serial.println("Z");
        return p;
    } else if (p == FINGERPRINT_ENROLLMISMATCH) {
        // Serial.println("Fingerprints did not match");
        Serial.println("Z");
        return p;
    } else {
        // Serial.println("Unknown error");
        Serial.println("Z");
        return p;
    }

// //   Serial.print("ID "); Serial.println(id);
    p = finger.storeModel(id);
    if (p == FINGERPRINT_OK) {
        // Serial.println("Stored!");
    } else if (p == FINGERPRINT_PACKETRECIEVEERR) {
        // Serial.println("Communication error");
        Serial.println("Z");
        return p;
    } else if (p == FINGERPRINT_BADLOCATION) {
        // Serial.println("Could not store in that location");
        Serial.println("Z");
        return p;
    } else if (p == FINGERPRINT_FLASHERR) {
        // Serial.println("Error writing to flash");
        Serial.println("Z");
        return p;
    } else {
        // Serial.println("Unknown error");
        Serial.println("Z");
        return p;
    }
    Serial.println("B");

    return true;
}