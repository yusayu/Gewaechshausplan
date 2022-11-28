# This is a sample Python script.
import RPi.GPIO as GPIO
import dht11
import adafruit_ht16k33.segments as segments
#from adafruit_ht16k33.segments import Seg7x4
import time
import board
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():
    #7-Segment-Display connected to i2c address 0x70
    i2c = board.I2C()
    segment = segments.Seg7x4(i2c, address=0x70) #segment der I2C Adresse 0x70 und die Displaydefinition zuweisen
    segment.fill(0)
    
    # dht11 connected to gpio pin 4
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    instance = dht11.DHT11(pin = 4)
    while True:
        result = instance.read()
        if result.is_valid():
            temp = round(result.temperature)
            rh = round(result.humidity)

            print(f'Temperatur: {temp}')
            print(f'Luftfeuchtigkeit: {rh}')
            
            segment[0] = str(temp//10)
            segment[1] = str(temp%10)
            
            segment[2] = str(rh//10)
            segment[3] = str(rh%10)
            segment.show()
            
        time.sleep(2)
        
    # Use a breakpoint in the code line below to debug your script.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
