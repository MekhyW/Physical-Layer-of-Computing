#define baud 9600
#define pin 10
#define character 'B'

void sendBit(bool Bit) {
  digitalWrite(pin, Bit);
  delayMicroseconds(1000000/baud);
}

void sendMessage() {
  sendBit(LOW);
  int characterint = stoi(character);
  bool parity = true;
  for (int i=7; i>=0; i--) {
    sendBit(bitRead(characterint, i);
    if (bitRead(characterint, i) == HIGH) {
      parity = !parity;
    }
  }
  sendBit(parity);
  sendBit(HIGH);
}

void setup() {
  Serial.begin(baud);
  pinMode(pin, OUTPUT);
  sendMessage();
  Serial.println("Mensagem enviada");
}

void loop() {
}
