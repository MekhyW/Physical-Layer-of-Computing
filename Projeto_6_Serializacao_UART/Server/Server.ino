#define baud 9600
#define pin 10

int character = 0;
bool parity = true;

bool readPin() {
  bool reading = digitalRead(pin);
  delayMicroseconds(1000000/baud);
  return reading;
}

void receiveMessage() {
  bool receivedBit;
  for (int i=0; i<=7; i++) {
    receivedBit = readPin();
    character |= (receivedBit << i);
    if (receivedBit) {
      parity = !parity;
    }
  }
  if (readPin() != parity) {
    Serial.println("Erro: Paridade incorreta");
  } else {
    Serial.println(character, HEX);
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
