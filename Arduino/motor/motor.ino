#define RPWM1 9
#define LPWM1 10
#define PWM1 11
#define RPWM2 4
#define LPWM2 5
#define PWM2 6

int command = 0;
int speed = 0;

void setup() {

  Serial.begin(9600);

  //Motor1
  pinMode (RPWM1, OUTPUT);
  pinMode (LPWM1, OUTPUT);
  pinMode (PWM1, OUTPUT);

  //Motor2
  pinMode (RPWM2, OUTPUT);
  pinMode (LPWM2, OUTPUT);
  pinMode (PWM2, OUTPUT);

}

void loop() {
  if (Serial.available() > 0){

    String toParse = Serial.readStringUntil("\n");
    toParse.trim();

    int colonIndex = toParse.indexOf(":");
    if (colonIndex != -1) {
      command = toParse.substring(0, colonIndex).toInt();
      speed = toParse.substring(colonIndex+1).toInt();
    }

    if (command == 1){ //Forward

      digitalWrite (LPWM1, HIGH);
      digitalWrite (RPWM1, LOW);
      analogWrite (PWM1, speed);

      digitalWrite (LPWM2, LOW);
      digitalWrite (RPWM2, HIGH);
      analogWrite (PWM2, speed);

    } else if (command == 2){ //Right

      digitalWrite (LPWM1, HIGH);
      digitalWrite (RPWM1, LOW);
      analogWrite (PWM1, speed);

      digitalWrite (LPWM2, HIGH);
      digitalWrite (RPWM2, LOW);
      analogWrite (PWM2, speed);

    } else if (command == 3){ //Left

      digitalWrite (LPWM1, LOW);
      digitalWrite (RPWM1, HIGH);
      analogWrite (PWM1, speed);

      digitalWrite (LPWM2, LOW);
      digitalWrite (RPWM2, HIGH);
      analogWrite (PWM2, speed);

    } else if (command == 4){ //Backward

    } else {

      digitalWrite (LPWM1, LOW);
      digitalWrite (RPWM1, LOW);
      analogWrite (PWM1, 0);

      digitalWrite (LPWM2, LOW);
      digitalWrite (RPWM2, LOW);
      analogWrite (PWM2, 0);

    }
  } 
    
    delay(500);
}