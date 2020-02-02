// The file is used to communicate with arduino through serial port
// send servo rotation data to the arduino to control the servo, and ultrasound will take a distance data and send back

from serial import Serial

def serial_ultrasound_control(input,port):
    ser = Serial(port, 1000000,timeout=2)
    ser.flushInput()
    ser.flushOutput()
    ser.write(bytes(input.encode())
    serial_reading = ser.readline()
    return serial_reading

port ='/dev/cu.usbmodem143401'
input_angle = 20
ultra_reading = serial_ultrasound_control(input_angle,port);
print(ultra_reading)

