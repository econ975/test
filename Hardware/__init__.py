from Hardware.NI_PCIe_6321.API import ODMR_counter
from Hardware.OpalKelly_XEM3005.API import PulseGenerator
from Hardware.SynthUSB3.API import SynthUSB3


class AllHardware():
    def __init__(self):
        self.trigger_counter = ODMR_counter()
        self.MW_source = SynthUSB3()
        self.pulser = PulseGenerator()
