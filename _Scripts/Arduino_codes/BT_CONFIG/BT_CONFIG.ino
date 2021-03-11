// This code was written by TechKrowd and you can find it at https://github.com/TechKrowd/ArduinoBluetooth
// The tutorial video to set up the HC-06 Bluetooth module is also available at https://www.youtube.com/watch?v=M7DTEcdzDTI
// To set up the HC-06 Bluetooth module you first need to plug the VCC into the digital pin 12 from the Arduino
// You need to do this only the first time to set up the module. Then you can connect it at the 5 volts pin
// The TX from the module goes into RX of the Arduino
// The RX from the module goes into the TX of the Arduino
// After load this sketch into the module you can load any skecth into the Arduino
// Just unplug the RX and TX pins to make it possible to connect with the usb to the computer

const int LED = 13;
const int BTPWR = 12; //after load this skecth you need to plug the pin into the VCC pin

char nombreBT[10] = "turtleBT"; //the name of the bluetooth
char velocidad = '4'; //9600
char pin [5]= "0000"; //pasword to acces the bluetooth module


void setup() {
  pinMode(LED, OUTPUT);
  pinMode(BTPWR, OUTPUT);

  digitalWrite(LED, LOW);
  digitalWrite(BTPWR, HIGH);

  Serial.begin(9600); 

  Serial.print("AT");
  delay(1000);

  Serial.print("AT+NAME");
  Serial.print(nombreBT);
  delay(1000);

  Serial.print("AT+BAUD");
  Serial.print(velocidad);
  delay(1000);

  Serial.print("AT+PIN");
  Serial.print(pin);
  delay(1000);

  digitalWrite(LED, HIGH);
}

void loop() {

}
