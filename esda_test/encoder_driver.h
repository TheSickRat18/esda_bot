/* *************************************************************
   Encoder driver function definitions - by James Nugen
   ************************************************************ */
#include <Arduino.h>
   
#ifdef A3144_ENC_COUNTER
  const uint8_t LEFT_ENC_PIN = 2;  //pin 4
  
  
  const uint8_t RIGHT_ENC_PIN = 3;  //pin 5
  
#endif
   
long readEncoder(int i);
void resetEncoder(int i);
void resetEncoders();
void initEncoders();
