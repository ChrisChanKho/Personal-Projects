#include <LedControl.h>
char serialData;
int pin=10;

//Pins
int DIN = 12;
int CS =  11;
int CLK = 10;

//LED combinations
byte smile[8]=   {0x3C,0x42,0xA5,0x81,0xA5,0x99,0x42,0x3C};
byte neutral[8]= {0x3C,0x42,0xA5,0x81,0xBD,0x81,0x42,0x3C};
byte frown[8]=   {0x3C,0x42,0xA5,0x81,0x99,0xA5,0x42,0x3C};
byte thumbsUp[8]= {0x0C,0x14,0x2F,0xC3,0xC3,0xE3,0x1E}; 

LedControl lc=LedControl(DIN,CLK,CS,0);

void setup(){
 lc.shutdown(0,false);       //The MAX72XX is in power-saving mode on startup
 lc.setIntensity(0,15);      // Set the brightness to maximum value
 lc.clearDisplay(0);         // and clear the display
 pinMode(pin, OUTPUT);
 Serial.begin(9600); 
}

void loop(){ 
    
    if(Serial.available())
    serialData = Serial.read();
    Serial.print(serialData);

    //Setting the sensitivity constraints
    if(serialData >= 10){    
      printByte(smile);
      
    }
    else if(serialData < 10){
      lc.clearDisplay(0);  
    }
}

void printByte(byte character [])
{
  int i = 0;
  for(i=0;i<8;i++)
  {
    lc.setRow(0,i,character[i]);
  }
}
