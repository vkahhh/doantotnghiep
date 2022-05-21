//assign pin number
int in1 = 2;
int in2 = 3;
int in3 = 4;
int in4 = 7;
int const ENA = 5;  
int const ENB = 6; 


// initial command
int command = 0;

void setup()

{
  pinMode(in1, OUTPUT);//motor A
  pinMode(in2, OUTPUT);//A
  pinMode(in3, OUTPUT);//B
  pinMode(in4, OUTPUT);//B
  pinMode(ENA, OUTPUT);   // set all the motor control pins to outputs
  pinMode(ENB, OUTPUT);

  Serial.begin(115200);
  
  while (!Serial);
  
  Serial.println("DO AN TOT NGHIEP");

}

void loop() {

if (Serial.available())

{
  //int state = Serial.parseInt();
  int state = Serial.read();

  if (state == 4) //turn left
  {
    
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, HIGH);   
    digitalWrite(ENA, HIGH);
    digitalWrite(ENB, HIGH);
    Serial.println("Left");
  }
//
//  if (state == 2)
//  {
//    digitalWrite(in1, LOW);
//    digitalWrite(in2, LOW);
//    digitalWrite(ENA, HIGH);
//    digitalWrite(ENB, HIGH);
//    Serial.println("Right");
//    Serial.println("Reverse");
  //}

  if (state == 3)
  {
  
    digitalWrite(in1, HIGH);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);   
    digitalWrite(ENA, HIGH);
    digitalWrite(ENB, HIGH);

  Serial.println("Right");
  }
  if (state == 1)
  {
  
    digitalWrite(in1, HIGH);
    digitalWrite(in2, HIGH);
    digitalWrite(in3, HIGH);
    digitalWrite(in4, HIGH);
    digitalWrite(ENA, HIGH);
    digitalWrite(ENB, HIGH);

  Serial.println("On track");
  }
  if (state == 5)
  {
  
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
    digitalWrite(ENA, LOW);
    digitalWrite(ENB, LOW);

  Serial.println("Stop");
  }

}

}
