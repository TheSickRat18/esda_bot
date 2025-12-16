/* *************************************************************
   Encoder definitions
   
   Add an "#ifdef" block to this file to include support for
   a particular encoder board or library. Then add the appropriate
   #define near the top of the main ROSArduinoBridge.ino file.
   
   ************************************************************ */
#include "commands.h"
#define A3144_ENC_COUNTER
#include "Arduino.h"
#include "encoder_driver.h"
#include "motor_driver.h"
#define PID_RATE 30;
#define A3144_ENC_COUNTER

#if defined(A3144_ENC_COUNTER)
/*
// STATE
volatile long left_enc_pos  = 0L;
volatile long right_enc_pos = 0L;

// ISR
void leftEncoderISR();
void rightEncoderISR();

// INIT
void initEncoders() {
  pinMode(LEFT_ENC_PIN, INPUT_PULLUP);
  pinMode(RIGHT_ENC_PIN, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(LEFT_ENC_PIN),
                  leftEncoderISR, FALLING);
  attachInterrupt(digitalPinToInterrupt(RIGHT_ENC_PIN),
                  rightEncoderISR, FALLING);
  Serial.println("Encoders initialsed");
}

// ISR
void leftEncoderISR() {
  //Serial.println("Triggered");
  left_enc_pos++;
}

void rightEncoderISR() {
  //Serial.println("Triggered");
  right_enc_pos++;
}


long readEncoder(int motor_idx) {
  
  if (motor_idx == LEFT)
    return left_enc_pos;
  else 
    return right_enc_pos;
  
}

void resetEncoder(int motor_idx) {
  if (motor_idx == LEFT)
    left_enc_pos = 0L;
  else
    right_enc_pos = 0L;
}

void resetEncoders() {
  resetEncoder(LEFT);
  resetEncoder(RIGHT);
}

#else
  #error "No encoder driver selected"
#endif

*/

/* ================= STATE ================= */
volatile long left_enc_pos  = 0L;
volatile long right_enc_pos = 0L;

static uint8_t left_last_state  = HIGH;
static uint8_t right_last_state = HIGH;

/* ================= INIT ================= */
void initEncoders() {
  pinMode(LEFT_ENC_PIN, INPUT_PULLUP);
  pinMode(RIGHT_ENC_PIN, INPUT_PULLUP);

  left_last_state  = digitalRead(LEFT_ENC_PIN);
  right_last_state = digitalRead(RIGHT_ENC_PIN);

  Serial.println("Encoders initialised (polling)");
}

/* ================= POLLING UPDATE ================= */
/* Call this as fast as possible (e.g. every loop()) */
void updateEncoders() {
  uint8_t left_state  = digitalRead(LEFT_ENC_PIN);
  uint8_t right_state = digitalRead(RIGHT_ENC_PIN);

  // Detect falling edge (HIGH -> LOW)
  if (left_last_state == HIGH && left_state == LOW) {
    left_enc_pos++;
  }

  if (right_last_state == HIGH && right_state == LOW) {
    right_enc_pos++;
  }

  left_last_state  = left_state;
  right_last_state = right_state;
}

/* ================= API ================= */
long readEncoder(int motor_idx) {
  if (motor_idx == LEFT)
    return left_enc_pos;
  else
    return right_enc_pos;
}

void resetEncoder(int motor_idx) {
  if (motor_idx == LEFT)
    left_enc_pos = 0L;
  else
    right_enc_pos = 0L;
}

void resetEncoders() {
  resetEncoder(LEFT);
  resetEncoder(RIGHT);
}

#else
  #error "No encoder driver selected"
#endif
