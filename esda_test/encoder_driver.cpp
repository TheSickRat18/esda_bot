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

/* ================= STATE ================= */
volatile long left_enc_pos  = 0L;
volatile long right_enc_pos = 0L;

/* ================= ISR DECLS ================= */
void leftEncoderISR();
void rightEncoderISR();

/* ================= INIT ================= */
void initEncoders() {
  pinMode(LEFT_ENC_PIN, INPUT_PULLUP);
  pinMode(RIGHT_ENC_PIN, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(LEFT_ENC_PIN),
                  leftEncoderISR, FALLING);
  attachInterrupt(digitalPinToInterrupt(RIGHT_ENC_PIN),
                  rightEncoderISR, FALLING);
  Serial.println("Encoders initialsed");
}

/* ================= ISR ================= */
void leftEncoderISR() {
  //Serial.println("Triggered");
  left_enc_pos++;
}

void rightEncoderISR() {
  //Serial.println("Triggered");
  right_enc_pos++;
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

