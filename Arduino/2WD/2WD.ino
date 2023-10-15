#include <AFMotor.h>

AF_DCMotor motor1(3);
AF_DCMotor motor2(4);

int howlong = 300;
int command = 0;
int speed = 0;

void setup() 
{
  Serial.begin(9600);
	motor1.setSpeed(200);
  motor2.setSpeed(200);
	motor1.run(RELEASE);
	motor2.run(RELEASE);
}

void loop() 
{
	uint8_t i;

  if (Serial.available() > 0){

    String toParse = Serial.readStringUntil("\n");
    toParse.trim();

    int colonIndex = toParse.indexOf(":");
    if (colonIndex != -1) {
      command = toParse.substring(0, colonIndex).toInt();
      speed = toParse.substring(colonIndex+1).toInt();
      Serial.print("Command: ");
      Serial.print(command);
      Serial.print("|");
      Serial.print("Speed: ");
      Serial.println(speed);
    }

    if (command == 1) { //forward
      motor1.run(FORWARD);
      motor2.run(FORWARD);
      for (i=0; i<howlong; i++) 
	      {
	      	motor1.setSpeed(speed);
          motor2.setSpeed(speed);
	      	delay(10);
	      }
      motor1.run(RELEASE);
	    motor2.run(RELEASE);
    }
    if (command == 3) { //right
      motor1.run(FORWARD);
      motor2.run(BACKWARD);
      for (i=0; i<howlong; i++) 
	      {
	      	motor1.setSpeed(speed); 
          motor2.setSpeed(speed);
	      	delay(10);
	      }
    	motor1.run(RELEASE);
	    motor2.run(RELEASE);
    }
    if (command == 2) { //left
      motor1.run(FORWARD);
      motor2.run(BACKWARD);
      for (i=0; i<howlong; i++) 
	      {
	      	motor1.setSpeed(speed); 
          motor2.setSpeed(speed);
	      	delay(10);
	      }
      motor1.run(RELEASE);
	    motor2.run(RELEASE);
    }
    else {
      motor1.setSpeed(0);
      motor2.setSpeed(0);
    }
  }  
}
