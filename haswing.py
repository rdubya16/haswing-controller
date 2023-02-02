import serial
import time

class Haswing:
    # Commands
    RIGHT_TURN = 0x52
    LEFT_TURN = 0x4c
    INCREASE_SPEED = 0x55
    DECREASE_SPEED = 0x44
    TOGGLE_MOTOR = 0x53
    DONE = 0x4e
    # Statuses
    MOTOR_ON = 0x00
    MOTOR_OFF = 0xff

    def __init__(self, ser_port='/dev/serial0', start_bit=0x23, device_id=0x54, stop_bit=0x80):
        self.ser = serial.Serial(
            port=ser_port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self._start_bit = start_bit
        self._stop_bit = stop_bit
        self._device_id = device_id
        self._motor_status = None
        self._motor_speed = None
        self._battery_level = None

        self.done()

    def done(self):
        self._send_command(self.DONE)

    def toggle_motor(self):
        self._send_command(self.TOGGLE_MOTOR)
        self.done()

    def right(self, steps=1):
        for _ in range(steps):
            self._send_command(self.RIGHT_TURN)
        self.done()

    def left(self, steps=1):
        for _ in range(steps):
            self._send_command(self.LEFT_TURN)
        self.done()

    def set_speed(self, speed):
        current_speed = self.motor_speed
        if current_speed < speed:
            while current_speed < speed:
                self._send_command(self.INCREASE_SPEED)
                current_speed = self.motor_speed
        elif current_speed > speed:
            while current_speed > speed:
                self._send_command(self.DECREASE_SPEED)
                current_speed = self.motor_speed
        self.done()

    def _build_command(self, command):
        return bytearray([self._start_bit, self._device_id, command, self._stop_bit])

    def _parse_response(self, command, resp):
        print(resp.hex())
        if len(resp) != 6 or resp[0] != self._start_bit or resp[1] != command:
          print ("Error: Corrupted response from motor.")
          return

        self._motor_status = resp[2]
        self._motor_speed = resp[3]
        self._battery_level = resp[4]

    def _send_command(self, command):
        run_cmd = self._build_command(command)
        self.ser.write(run_cmd)
        resp = self.ser.read(6)
        self._parse_response(command,resp)

    @property
    def motor_status(self):
        return self._motor_status

    @property
    def motor_speed(self):
        return self._motor_speed

    @property
    def battery_level(self):
        return self._battery_level

# testing
t = Haswing()
t.set_speed(5)
t.toggle_motor()
time.sleep(1)
t.toggle_motor()
t.right(100)
time.sleep(1)
t.left(100)
time.sleep(1)
t.set_speed(1)
