#define baud 9600
#define pin 10

bool readPin() {
  return digitalRead(pin);
}

void setup() {
  Serial.begin(baud);
  pinMode(pin, INPUT);
}

void loop() {
  Serial.println(readPin());
  //Serial.println("Aguardando sinal LOW");
  //while (readPin()) {
  //}
  //Serial.println("Recebendo mensagem");
}
