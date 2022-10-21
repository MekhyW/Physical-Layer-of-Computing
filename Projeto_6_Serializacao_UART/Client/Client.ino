#define baud 9600
#define pin 10
#define character 'B'

bool message[8] = {0, 0, 0, 0, 0, 0, 0, 0}; //01000010
bool parity = false;
int timeskip = 1000000/baud;

void sendBit(bool Bit) {
  digitalWrite(pin, Bit);
  delayMicroseconds(timeskip);
}

void assembleMessage() {
  int characterInt = int(character);
  for (int i=0; i<=7; i++) {
    message[i] = bitRead(characterInt, i);
    if (message[i]) {
      parity = !parity;
    }
  }
}

void sendMessage() {
  sendBit(LOW); //start bit
  for (int i=0; i<=7; i++) {
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
