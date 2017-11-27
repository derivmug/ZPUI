from time import sleep

from skeleton import InputSkeleton

class InputDevice(InputSkeleton):
    """ A driver for pushbuttons attached to Raspberry Pi GPIO. It uses RPi.GPIO library. Button's first pin has to be attached to ground, second pin has to be attached to the GPIO pin and pulled up to 3.3V with a 1-10K resistor."""

    default_mapping = [
    "KEY_UP",
    "KEY_DOWN",
    "KEY_LEFT",
    "KEY_RIGHT",
    "KEY_KPENTER",
    "KEY_DELETE",
    "KEY_HOME",
    "KEY_END"]

    def __init__(self, button_pins=[], **kwargs):
        """Initialises the ``InputDevice`` object. 

        Kwargs:
        
        * ``button_pins``: GPIO mubers which to treat as buttons (GPIO.BCM numbering)
        * ``debug``: enables printing button press and release events when set to True
        """
        self.button_pins = button_pins
        self.init_hw()
        InputSkeleton.__init__(self, **kwargs)

    def init_hw(self):
        import RPi.GPIO as GPIO #Doing that because I couldn't mock it for ReadTheDocs
        self.GPIO = GPIO
        GPIO.setmode(GPIO.BCM) 
        for pin_num in self.button_pins:
            GPIO.setup(pin_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.button_states = []
        for i, pin_num in enumerate(self.button_pins):
            self.button_states.append(GPIO.input(pin_num))

    def runner(self):
        """Polling loop. Stops when ``stop_flag`` is set to True."""
        while not self.stop_flag:
            for i, pin_num in enumerate(self.button_pins):
                button_state = self.GPIO.input(pin_num)
                if button_state != self.button_states[i]:
                    if button_state == False and self.enabled:
                        key = self.mapping[i]
                        self.send_key(key)
                    self.button_states[i] = button_state
            sleep(0.01)



if __name__ == "__main__":
    id = InputDevice(button_pins=[22, 23, 27, 24, 18, 4], threaded=False)
    id.runner()
