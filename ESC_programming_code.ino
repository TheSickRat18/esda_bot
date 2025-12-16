#include <Servo.h>
// To go forward, enter neutral (1500), then 1600 
// To go backward, enter neutral (1500), then 1400
// to brake, enter neutral
#define MAX_SIGNAL 2000
#define NEUTRAL_SIGNAL 1500
#define MIN_SIGNAL 1000
#define MOTOR_PIN 9
const int sensorPin =2;
const int ledPin = 3;       // Output pin (D3)

// Variables
volatile unsigned long pulse_count = 0;
unsigned long last_state = HIGH;
unsigned long current_state = HIGH;
unsigned long last_millis = 0;
unsigned long rpm = 0;

int DELAY = 1000;
Servo motor;
void setup() {
  Serial.begin(9600);
  pinMode(sensorPin, INPUT);
  Serial.println("ESC calibration...");
  Serial.println(" ");
  delay(1500);
  Serial.println("Starting...");
  delay(1000);
  motor.attach(MOTOR_PIN);
  // Wait for input
  Serial.println("The ESC is calibrated");
  Serial.println("----");
  Serial.println("Now, type a values between 1000 and 2000 and press enter");
}
void loop() {
    // --- Read Pin ---
    current_state = digitalRead(sensorPin);
    //Serial.print("current state: ");
    //Serial.print(current_state);
    //Serial.println();
    // --- Count Falling Edges (1 → 0) ---
    if (last_state == HIGH && current_state == LOW) {
      pulse_count++;
      //Serial.print("pulse count: ");
      //Serial.println(pulse_count);
      digitalWrite(ledPin, !digitalRead(ledPin));  // toggle LED
    }

    last_state = current_state;

    // --- Calculate Every 1 Second ---
    if (millis() - last_millis > 1000) {
      // Same formula you used:
      // rpm = (pulse_count * 60000 / 1000) / 48;
      rpm = (pulse_count * 60) / 48;
      Serial.print("pulse_count: ");
      Serial.println(pulse_count);
      Serial.print("RPM: ");
      Serial.println(rpm);
      // Reset count & timer
      pulse_count = 0;
      last_millis = millis();
    }
    // read velocity command
    if (Serial.available() > 0) {
      int cmd = Serial.parseInt();
      if (cmd > 999) { // Enter any value between 1000-2000 for any speed
        motor.writeMicroseconds(cmd);
        float SPEED = (cmd-1000)/10;
        Serial.print("\n");
        Serial.println("Motor speed:");
        Serial.print(" ");
        Serial.print(SPEED);
        Serial.print("%");
      }
    }
    
  }