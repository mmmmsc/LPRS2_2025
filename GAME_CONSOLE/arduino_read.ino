#define BUTTON_A 2
#define BUTTON_B 3
#define BUTTON_C 4
#define BUTTON_D 5
#define BUTTON_E 6
#define BUTTON_F 7

#define JOYSTICK_X A0
#define JOYSTICK_Y A1
#define JOYSTICK_SW 8

// Joystick parametri
const int JOY_CENTER = 330;
const int DEADZONE = 100; 

void setup() {
  Serial.begin(9600);

  pinMode(BUTTON_A, INPUT_PULLUP);
  pinMode(BUTTON_B, INPUT_PULLUP);
  pinMode(BUTTON_C, INPUT_PULLUP);
  pinMode(BUTTON_D, INPUT_PULLUP);
  pinMode(BUTTON_E, INPUT_PULLUP);
  pinMode(BUTTON_F, INPUT_PULLUP);
  pinMode(JOYSTICK_SW, INPUT_PULLUP);
}

void loop() {
  // Dugmad A-F
  if (digitalRead(BUTTON_A) == LOW) Serial.println("BTN_A");
  if (digitalRead(BUTTON_B) == LOW) Serial.println("BTN_B");
  if (digitalRead(BUTTON_C) == LOW) Serial.println("BTN_C");
  if (digitalRead(BUTTON_D) == LOW) Serial.println("BTN_D");
  if (digitalRead(BUTTON_E) == LOW) Serial.println("BTN_E");
  if (digitalRead(BUTTON_F) == LOW) Serial.println("BTN_F");

  // Joystick
  int joyX = analogRead(JOYSTICK_X);
  int joyY = analogRead(JOYSTICK_Y);

  // X osa
  if (joyX < (JOY_CENTER - DEADZONE)) {
    Serial.println("JOY_LEFT");
  } else if (joyX > (JOY_CENTER + DEADZONE)) {
    Serial.println("JOY_RIGHT");
  }

  // Y osa
  if (joyY < (JOY_CENTER - DEADZONE)) {
    Serial.println("JOY_DOWN");
  } else if (joyY > (JOY_CENTER + DEADZONE)) {
    Serial.println("JOY_UP");
  }

  // Pritiskanje joystick dugmeta
  if (digitalRead(JOYSTICK_SW) == LOW) {
    Serial.println("JOY_PRESS");
  }

  delay(150); 
}
