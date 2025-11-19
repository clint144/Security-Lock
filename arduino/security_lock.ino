const int redLED = 13;

// LED states
enum LedState {
  IDLE,       // off
  SEARCHING,  // slow blink
  APPROVED,   // solid on
  NOFACE      // off for denied / no face
};

LedState state = IDLE;

unsigned long lastToggle = 0;
bool ledOn = false;

void setup() {
  pinMode(redLED, OUTPUT);
  Serial.begin(9600);
  digitalWrite(redLED, LOW);   // start off
}

void loop() {
  // ----- 1. Handle messages from Python -----
  if (Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();

    if (msg == "SEARCH") {
      state = SEARCHING;
      ledOn = false;
      digitalWrite(redLED, LOW);
    }
    else if (msg == "APPROVED") {
      state = APPROVED;
      digitalWrite(redLED, HIGH);   // solid ON
    }
    else if (msg == "DENIED" || msg == "NOFACE") {
      // whether it's "no face" or "access denied",
      // we turn the LED OFF and stop blinking
      state = NOFACE;
      digitalWrite(redLED, LOW);
      ledOn = false;
    }
  }

  // ----- 2. Drive LED pattern based on state -----
  unsigned long now = millis();

  switch (state) {
    case SEARCHING:
      // slow blink while searching
      if (now - lastToggle >= 500) {  // 0.5s
        ledOn = !ledOn;
        digitalWrite(redLED, ledOn ? HIGH : LOW);
        lastToggle = now;
      }
      break;

    case APPROVED:
      // solid on
      digitalWrite(redLED, HIGH);
      break;

    case NOFACE:
    case IDLE:
    default:
      // LED off
      digitalWrite(redLED, LOW);
      break;
  }
}

