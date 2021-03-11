// This code is based on the code from https://github.com/aspro648/OSTR
// The modification that was made has the objective of controlling the TurtleBot through the Serial Monitor
// The code to read the Serial Monitor it is based in the code from https://www.automatizacionparatodos.com/puerto-serie-arduino/
// instead of writing all the instructions for the turtle in this sketch
// The instructions that can be sent through the Serial Monitor can be:
// 'U' for penup
// 'D' for pendown
// 'F100' for move forward 100 mm or any number
// 'B100' for move backward 100 mm or any number 
// 'R45' to rotate right 45 degrees or any number
// 'L45' to rotate right 45 degrees or any number
// only capitals letters


#include <Servo.h>

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// STRING DESCRIPTION
String entradaSerial = "";     // String for the instruction
bool entradaCompleta = false;  // 
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// SETUP SERVO
int servoPin = 8;
int PEN_DOWN = 80; // angle of servo when pen is down
int PEN_UP = 20;   // angle of servo when pen is up
Servo penServo;
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// CALIBRATION OF WHEELS
float wheel_dia = 62; //    # mm (increase = spiral out)
float wheel_base = 115; //    # mm (increase = spiral in, ccw)
int steps_rev = 512; //        # 512 for 64x gearbox, 128 for 16x gearbox
int delay_time = 6; //         # time between steps in ms
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// STEPPER SEQUENCE org->pink->blue->yel
int L_stepper_pins[] = {12, 10, 9, 11};
int R_stepper_pins[] = {4, 6, 7, 5};
int fwd_mask[][4] =  {{1, 0, 1, 0},
  {0, 1, 1, 0},
  {0, 1, 0, 1},
  {1, 0, 0, 1}
};
int rev_mask[][4] =  {{1, 0, 0, 1},
  {0, 1, 0, 1},
  {0, 1, 1, 0},
  {1, 0, 1, 0}
};
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


void setup() {
  
  randomSeed(analogRead(1));
  Serial.begin(9600);
  for (int pin = 0; pin < 4; pin++) {
    pinMode(L_stepper_pins[pin], OUTPUT);
    digitalWrite(L_stepper_pins[pin], LOW);
    pinMode(R_stepper_pins[pin], OUTPUT);
    digitalWrite(R_stepper_pins[pin], LOW);
  }
  penServo.attach(servoPin);
  Serial.println("setup ready... waiting for instructions");
  Serial.println(entradaSerial);
  penup();
  delay(1000);
}

void loop()
{

   String a = entradaSerial;
   int searchF = a.indexOf('F');
   int d = a.charAt(0);
   int b = a.toInt();
   String w = "waiting for instruction like F100; R20; L45; B200..."; 
 
   if (entradaCompleta) {
    if (entradaSerial == "\n") {
      Serial.print("write instruction. No data received after return\n");
      penup();
      Serial.flush();
    } 
      else if (a.charAt(0) == 'F') {
      a.remove(0, 1);
      int f = a.toInt(); 
      Serial.println("ACK");
      forward(f);
      Serial.flush();
      Serial.println("DONE");
      Serial.flush();
    } 
      else if (a.charAt(0) == 'B') {
      a.remove(0, 1);
      int b = a.toInt();
      Serial.println("ACK");
      backward(b);
      Serial.flush();
      Serial.println("DONE");
      Serial.flush();
    }
      else if (a.charAt(0) == 'R') {
      a.remove(0, 1);
      int r = a.toInt();
      Serial.println("ACK");
      right(r);
      Serial.flush();
      Serial.println("DONE");
      Serial.flush();
    }     
      else if (a.charAt(0) == 'L') {
      a.remove(0, 1);
      int l = a.toInt();
      Serial.println("ACK");
      left(l);
      Serial.flush();
      Serial.println("DONE");
      Serial.flush();
    } 
      else if (a.charAt(0) == 'U') {
      a.remove(0, 1);
      int u = a.toInt();
      Serial.println("ACK");
      penup();
      Serial.flush();
      Serial.println("DONE");
      Serial.flush();
    }
      else if (a.charAt(0) == 'D') {
      a.remove(0, 1);
      int u = a.toInt();
      Serial.println("ACK");
      pendown();
      Serial.flush();
      Serial.println("DONE");
      Serial.flush();
    }             
      else {
      Serial.println(w); 
    }
      entradaCompleta = false;
      entradaSerial = "";
}
}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// HELPER FUNCTIONS
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
int step(float distance) {
  int steps = distance * steps_rev / (wheel_dia * 3.1412); //24.61
  /*
    Serial.print(distance);
    Serial.print(" ");
    Serial.print(steps_rev);
    Serial.print(" ");
    Serial.print(wheel_dia);
    Serial.print(" ");
    Serial.println(steps);
    delay(1000);*/
  return steps;
}
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// HELPER FUNCTIONS - TURTLE INSTRUCTIONS
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

void forward(float distance) {
  int steps = step(distance);
  //Serial.println(steps);
  for (int step = 0; step < steps; step++) {
    for (int mask = 0; mask < 4; mask++) {
      for (int pin = 0; pin < 4; pin++) {
        digitalWrite(L_stepper_pins[pin], rev_mask[mask][pin]);
        digitalWrite(R_stepper_pins[pin], fwd_mask[mask][pin]);
      }
      delay(delay_time);
    }
  }
}


void backward(float distance) {
  int steps = step(distance);
  for (int step = 0; step < steps; step++) {
    for (int mask = 0; mask < 4; mask++) {
      for (int pin = 0; pin < 4; pin++) {
        digitalWrite(L_stepper_pins[pin], fwd_mask[mask][pin]);
        digitalWrite(R_stepper_pins[pin], rev_mask[mask][pin]);
      }
      delay(delay_time);
    }
  }
}


void right(float degrees) {
  float rotation = degrees / 360.0;
  float distance = wheel_base * 3.1412 * rotation;
  int steps = step(distance);
  for (int step = 0; step < steps; step++) {
    for (int mask = 0; mask < 4; mask++) {
      for (int pin = 0; pin < 4; pin++) {
        digitalWrite(R_stepper_pins[pin], rev_mask[mask][pin]);
        digitalWrite(L_stepper_pins[pin], rev_mask[mask][pin]);
      }
      delay(delay_time);
    }
  }
}


void left(float degrees) {
  float rotation = degrees / 360.0;
  float distance = wheel_base * 3.1412 * rotation;
  int steps = step(distance);
  for (int step = 0; step < steps; step++) {
    for (int mask = 0; mask < 4; mask++) {
      for (int pin = 0; pin < 4; pin++) {
        digitalWrite(R_stepper_pins[pin], fwd_mask[mask][pin]);
        digitalWrite(L_stepper_pins[pin], fwd_mask[mask][pin]);
      }
      delay(delay_time);
    }
  }
}


void done() { // unlock stepper to save battery
  for (int mask = 0; mask < 4; mask++) {
    for (int pin = 0; pin < 4; pin++) {
      digitalWrite(R_stepper_pins[pin], LOW);
      digitalWrite(L_stepper_pins[pin], LOW);
    }
    delay(delay_time);
  }
}


void penup() {
  delay(250);
  penServo.write(PEN_UP);
  delay(250);
}


void pendown() {
  delay(250);
  penServo.write(PEN_DOWN);
  delay(250);
}


void serialEvent() {
  while (Serial.available()) {
    // Obtener bytes de entrada:
    char inChar = (char)Serial.read();
    // Agregar al String de entrada:
    entradaSerial += inChar;
    // Para saber si el string está completo, se detendrá al recibir
    // el caracter de retorno de línea ENTER \n
    if (inChar == '\n') {
      entradaCompleta = true;
    }
  }
}
