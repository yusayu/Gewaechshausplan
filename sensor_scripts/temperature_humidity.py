import RPi.GPIO as GPIO
import dht11
import adafruit_ht16k33.segments as segments
import time
import board
import concurrent.futures
import csv
import datetime as dt

def main():
    i2c = board.I2C()
    #segment der I2C Adresse 0x70 und die Displaydefinition zuweisen
    segment = segments.Seg7x4(i2c, address=0x70) 
    segment.fill(0)
    measurement_delay = 10 # Zeit zwischen Messungen

    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    # DHT11 Objekt anlegen
    instance = dht11.DHT11(pin = 4)
    starting_time = dt.datetime.now()
    csv_filename = f'messdaten_{starting_time.strftime("%Y_%m_%d, %H_%M_%S")}.csv'
    fields = ['Zeit', 'Temperatur', 'Luftfeuchtigkeit'] # csv Feldnamen
    with open(csv_filename, 'a+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader() # csv Header erstellen
    while True: # Dauerbetrieb
        result = instance.read() # Liest die Werte des Sensors in ein Objekt ein
        if result.is_valid():
            # Temperatur und Luftfeuchtigkeit runden
            # Nachkommastellen werden aufgrund der Genauigkeit des Sensors
            # nicht benötigt
            temp = round(result.temperature)
            rh = round(result.humidity)

            print(f'Temperatur: {temp}')
            print(f'Luftfeuchtigkeit: {rh}')
            segment.fill(0)
            
            # Segmente mit jeweils 10er und 1er stelle füllen
            segment[0] = str(temp//10)
            segment[1] = str(temp%10)
            
            # 100 wird als 00 angezeigt
            segment[2] = str(rh//10 if rh < 100 else '0')
            segment[3] = str(rh%10)
            segment.show()
            with open(csv_filename, 'a+') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fields)
                writer.writerow({k: v for k, v in zip(fields, [dt.datetime.now().strftime('%d.%m.%Y %H:%M:%S'), temp, rh])})
            if measurement_delay is not None:
                time.sleep(measurement_delay)


if __name__ == '__main__':
    main()
