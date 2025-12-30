#include <WiFi.h>

// ====== Wi-Fi credentials ======
const char* ssid = "Your SSID"; //change to your wifi ssid
const char* password = "87654321"; //change to your wifi password

// ====== Static IP configuration ======
IPAddress local_IP(192, 168, 137, 155);
IPAddress gateway(192, 168, 137, 1);
IPAddress subnet(255, 255, 255, 0);

// ====== TCP server ======
WiFiServer server(8080);
WiFiClient client;

// ====== Motor driver pins ======
const int ENA = 25;   // PWM for Motor A (Left)
const int IN1 = 26;
const int IN2 = 27;

const int ENB = 14;   // PWM for Motor B (Right)
const int IN3 = 12;
const int IN4 = 13;

int motorSpeed = 200; // Default speed (0–255)

// ====== PWM Setup ======
const int freq = 5000;
const int resolution = 8;
const int pwmChannelA = 0;
const int pwmChannelB = 1;

// ====== Watchdog ======
unsigned long lastCommandTime = 0;
const unsigned long COMMAND_TIMEOUT = 800; // ms

void setup() {
  Serial.begin(115200);

  // Setup motor pins
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Setup PWM for ENA & ENB
  ledcSetup(pwmChannelA, freq, resolution);
  ledcSetup(pwmChannelB, freq, resolution);
  ledcAttachPin(ENA, pwmChannelA);
  ledcAttachPin(ENB, pwmChannelB);

  stopMotors();

  // Connect to Wi-Fi
  connectWiFi();

  // Start server
  server.begin();
  Serial.println("🚀 TCP server started.");
}

void loop() {
  maintainWiFi();

  // Accept new client
  if (!client || !client.connected()) {
    client = server.available();
    if (client) {
      Serial.println("📲 Client connected.");
    }
  }

  // Handle incoming commands
  if (client && client.available()) {
    String command = client.readStringUntil('\n');
    command.trim();
    if (command.length() > 0) {
      processCommand(command);
      lastCommandTime = millis();
    }
  }

  // Safety watchdog
  if (millis() - lastCommandTime > COMMAND_TIMEOUT) {
    stopMotors();
  }
}

// ====== Wi-Fi helpers ======
void connectWiFi() {
  Serial.println("Connecting to Wi-Fi...");
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("⚠️ Static IP failed!");
  }
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ Wi-Fi connected!");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void maintainWiFi() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("⚠️ Wi-Fi lost, reconnecting...");
    connectWiFi();
  }
}

// ====== Command handler ======
void processCommand(String command) {
  Serial.print("Received: ");
  Serial.println(command);

  char dir = command.charAt(0);

  int spaceIndex = command.indexOf(' ');
  if (spaceIndex > 0) {
    int spd = command.substring(spaceIndex + 1).toInt();
    motorSpeed = constrain(spd, 0, 255);
  }

  switch (dir) {
    case 'F': moveForward(); break;
    case 'B': moveBackward(); break;
    case 'L': turnLeft(); break;
    case 'R': turnRight(); break;
    case 'S': stopMotors(); break;
    default: Serial.println("❓ Unknown command"); break;
  }
}

// ====== Motor functions (ENA/ENB PWM) ======
void moveForward() {
  // Left motor forward
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  // Right motor forward
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  ledcWrite(pwmChannelA, motorSpeed);
  ledcWrite(pwmChannelB, motorSpeed);

  Serial.println("⬆️ Forward");
}

void moveBackward() {
  // Left motor backward
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  // Right motor backward
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  ledcWrite(pwmChannelA, motorSpeed);
  ledcWrite(pwmChannelB, motorSpeed);

  Serial.println("⬇️ Backward");
}

void turnLeft() {
  // Left motor backward
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  // Right motor forward
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);

  ledcWrite(pwmChannelA, motorSpeed-40);
  ledcWrite(pwmChannelB, motorSpeed);

  Serial.println("⬅️ Left");
}

void turnRight() {
  // Left motor forward
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  // Right motor backward
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);

  ledcWrite(pwmChannelA, motorSpeed);
  ledcWrite(pwmChannelB, motorSpeed-40);

  Serial.println("➡️ Right");
}

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);

  ledcWrite(pwmChannelA, 0);
  ledcWrite(pwmChannelB, 0);

  Serial.println("🛑 Stop");
}
