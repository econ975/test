# from Hardware.NI_PCIe_6321.API import ODMR_counter
# from Hardware.OpalKelly_XEM3005.API import PulseGenerator
from Hardware.SynthUSB3.API import SynthUSB3
from Hardware.thorlabs_tsi_sdk.tl_camera import TLCameraSDK
# from thorlabs_tsi_sdk.tl_camera import TLCameraSDK


class AllHardware():
    def __init__(self):
        # self.trigger_counter = ODMR_counter()

        self.MW_source = SynthUSB3()
        self.sdk = TLCameraSDK()
        self.cameras = self.sdk.discover_available_cameras()
        if len(self.cameras) == 0:
            print("Error: no cameras detected!")
        # self.camera = sdk.open_camera(cameras[0])
        # self.pulser = PulseGenerator()


if __name__ == '__main__':
    hardware = AllHardware()

