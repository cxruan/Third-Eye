#include <Servo.h>

int triggerPin = 7; //triggering on pin 7
int echoPin = 8;    //echo on pin 8
int info = 20;
int old_info = 20;
Servo myservo;


void setup() { //we will be combinig both setups from the codes

  Serial.begin(9600);  //we'll start serial comunication, so we can see the distance on the serial monitor

  pinMode(triggerPin, OUTPUT); //defining pins
  pinMode(echoPin, INPUT);
  myservo.attach(9);
}

void loop() { 
  sensor();
}


void sensor() { //loop from the sensor code is renamed to the "sensor" void
  info = Serial.read();
  int duration, distance;    //Adding duration and distance
  if (info != old_info) {
    myservo.write(info);                  // sets the servo position according to the scaled value
    delayMicroseconds(300);
    digitalWrite(triggerPin, HIGH); //triggering the wave(like blinking an LED)
    delayMicroseconds(200);
    digitalWrite(triggerPin, LOW);
    duration = pulseIn(echoPin, HIGH); //a special function for listening and waiting for the wave
    distance = (duration / 2) / 29.1; 
    Serial.print(distance); 
    Serial.print('cm'); 
    Serial.print('\n'); 
    myservo.write(info);
    delayMicroseconds(300);
    old_info = info;
  }
}
