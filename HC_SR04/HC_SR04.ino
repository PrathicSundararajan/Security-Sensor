/*
 * HC-SR04 example sketch
 *
 * https://create.arduino.cc/projecthub/Isaac100/getting-started-with-the-hc-sr04-ultrasonic-sensor-036380
 *
 * by Isaac100
 */
#include "SoftwareSerial.h"
SoftwareSerial serial_connection(0,1);
const int trigPin = 2;
const int echoPin = 3;
String val = "";
const int buttonPin = 4;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status
int currButt = 100;
int prevButt = -100;
int currState = 1;

float duration, distance;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
  serial_connection.begin(9600);
  pinMode(ledPin, OUTPUT);
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
  //Serial.print("Distance: "); cms
  if (currState == 1)
    Serial.println(distance);
    serial_connection.println(distance);  
  //serial_connection.println(distance);
  prevButt = currButt;
  buttonState = digitalRead(buttonPin);
  currButt = buttonState;
  //Serial.println(currButt);
  /*
  if( serial_connection.available() ) // if data is available to read
   {
     val = serial_connection.read(); // read it and store it in 'val'
  }
  if( val.length() > 0) // if 'H' was received
   {
      serial_connection.println(distance);   
      //serial_connection.println("Sending from arduino"); 
  } 
  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  */
  if (buttonState == HIGH) {
    if (currState == 1)
      currState = 0;
    else 
      currState = 1;
    //Serial.println(currState);
    delay(2000);
  } 
} 

/*
#include "SoftwareSerial.h"
SoftwareSerial serial_connection(1,0);
const int trigPin = 3;
const int echoPin = 2;
String val = "";


float duration, distance;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.println("DONNEEEE1");
  Serial.begin(9600);
  Serial.println("DONNEEEE2");
  serial_connection.begin(9600);
  Serial.println("DONNEEEE");
  Serial.println("DONNEEEE");
  Serial.println("DONNEEEE");
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = (duration*.0343)/2;
  //Serial.print("Distance: "); cms
  Serial.println(distance);
  if( serial_connection.available() ) // if data is available to read
   {
     val = serial_connection.read(); // read it and store it in 'val'
  }
  if( val.length() > 0) // if 'H' was received
   {
      serial_connection.println(distance);   
      //serial_connection.println("Sending from arduino"); 
  } 
   delay(100);
   
}
*/
