  //assign pin number
int m11 = 5;
int m12 = 6;
int m21 = 9;
int m22 = 10;
//int const ENA = 3;  
//int const ENB = 8; 


// initial command
int command = 0;

void setup()

{
  pinMode(m11, OUTPUT);//motor A
  pinMode(m12, OUTPUT);//A
  pinMode(m21, OUTPUT);//B
  pinMode(m22, OUTPUT);//B
//  pinMode(ENA, OUTPUT);   // set all the motor control pins to outputs
//  pinMode(ENB, OUTPUT);

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
    
    digitalWrite(m11, LOW);
    digitalWrite(m12, LOW);
    digitalWrite(m21, HIGH);
    digitalWrite(m22, LOW);   
//    digitalWrite(ENA, HIGH);
//    digitalWrite(ENB, HIGH);
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
 // }

  if (state == 3)
  {
  
    digitalWrite(m11, LOW);
    digitalWrite(m12, HIGH);
    digitalWrite(m21, LOW);
    digitalWrite(m22, LOW);   
//    digitalWrite(ENA, HIGH);
//    digitalWrite(ENB, HIGH);

  Serial.println("Right");
  }
  if (state == 1)
  {
  
    digitalWrite(m11, LOW);
    digitalWrite(m12, HIGH);
    digitalWrite(m21, HIGH);
    digitalWrite(m22, LOW);
//    digitalWrite(ENA, HIGH);
//    digitalWrite(ENB, HIGH);

  Serial.println("On track");
  }
  if (state == 5)
  {
  
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
//    digitalWrite(ENA, LOW);
//    digitalWrite(ENB, LOW);

  Serial.println("Stop");
  }

}

}
