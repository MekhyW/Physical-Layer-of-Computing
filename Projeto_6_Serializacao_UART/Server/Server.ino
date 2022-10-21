#define baud 9600
#define pin 10

bool readPin() {
  return digitalRead(pin);
}

void receiveMessage() {
  byte character = 0;
  bool receivedBit;
  bool parity = false;
  for (int i=0; i<=7; i++) {
    receivedBit = digitalRead(pin);
    Serial.println(receivedBit);
    character = character + (receivedBit << i);
    if (receivedBit == HIGH) {
      parity = !parity;
    }
  }
  if (digitalRead(pin) != parity) {
    Serial.println("Erro: Paridade incorreta");
  } else {
    Serial.println(receivedBit);
  }
}

void setup() {
  Serial.begin(baud);
  pinMode(pin, INPUT);
  Serial.println("Aguardando sinal LOW");
  while (readPin()) {
  }
  receiveMessage();
}

void loop() {
}
