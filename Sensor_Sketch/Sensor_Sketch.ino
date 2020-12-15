/*
 * Security Sensor Sketch
 * by Prathic
 */
#include "SoftwareSerial.h"
SoftwareSerial serial_connection(0,1);
const int trigPin = 2;
const int echoPin = 3;
const int buttonPin = 4;     // the number of the pushbutton pin

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status
int currState = 1;
bool paused= false;

float duration, distance;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
  serial_connection.begin(9600);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);

}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration*.0343)/2;
  if (currState == 1){
    Serial.println(distance);
    serial_connection.println(distance); 
    paused = false; 
  }
  if (currState == 0 && !paused){
    Serial.println(-1000);
    paused = true;
    serial_connection.println(-1000); 
  }
  buttonState = digitalRead(buttonPin);
  if (buttonState == HIGH) {
    if (currState == 1)
      currState = 0;
    else 
      currState = 1;
    delay(2000);
  } 
} 
