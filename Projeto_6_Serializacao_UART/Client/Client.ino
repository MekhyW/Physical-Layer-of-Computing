#define baud 9600
#define pin 10
#define character 'B' //01000010

bool message[8] = {0, 0, 0, 0, 0, 0, 0, 0};
bool parity = true;

void sendBit(bool Bit) {
  digitalWrite(pin, Bit);
  Serial.print(Bit);
  delayMicroseconds(1000000/baud);
}

void assembleMessage() {
  int characterInt = int(character);
  for (int i=7; i>=0; i--) {
    message[i] = bitRead(characterInt, i);
    if (bitRead(characterInt, i) == HIGH) {
      parity = !parity;
    }
  }
}

void sendMessage() {
  sendBit(LOW); //start bit
  for (int i=7; i>=0; i--) {
    sendBit(message[i]);
  }
  sendBit(parity);
  sendBit(HIGH); //stop bit
}

void setup() {
  assembleMessage();
  Serial.begin(baud);
  pinMode(pin, OUTPUT);
  sendMessage();
  Serial.println("\nMensagem enviada");
}

void loop() {
}
