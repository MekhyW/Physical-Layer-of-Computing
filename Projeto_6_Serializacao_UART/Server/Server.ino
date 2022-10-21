#define baud 9600
#define pin 10

int character = 0;
bool parity = false;
int timeskip = 1000000/baud;

bool readPin() {
  bool reading = digitalRead(pin);
  delayMicroseconds(timeskip);
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
    Serial.println(char(character));
  }
}

void setup() {
  Serial.begin(baud);
  pinMode(pin, INPUT);
  Serial.println("Aguardando sinal LOW");
  while (readPin()) {
  }
  delayMicroseconds(timeskip/2);
  receiveMessage();
}

void loop() {
}
