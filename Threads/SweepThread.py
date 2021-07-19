from PyQt5 import QtCore
import numpy as np
import sys, numpy


class SweepThread(QtCore.QThread):
    """
    Sweeping module as a thread, based on PyQt5.QtCore.QThread
    parameters:
    @hardware: python object of hardware control
    """

    SIGNAL_update = QtCore.pyqtSignal(list, name='update')

    def __init__(self, hardware=None, parent=None):
        super().__init__(parent)
        self._hardware = hardware
        self.parameters = {'StartFreq': 2.8,
                           'StopFreq': 2.95,
                           'NumOfSteps': 300,
                           'DwellTime': 20,
                           'NumOfAvgs': 50,
                           'Power': 0
                           }

    def run(self):
        self.running = True

        self.start_freq = float(self.parameters['StartFreq']) * 1000.0
        self.stop_freq = float(self.parameters['StopFreq']) * 1000.0
        self.num_of_step = int(self.parameters['NumOfSteps'])
        self.dwell_time = int(self.parameters['DwellTime'])
        self.num_of_ave = int(self.parameters['NumOfAvgs'])
        self.power = float(self.parameters['Power'])

        self._hardware.MW_source.set_power(power=self.power)
        self._hardware.MW_source.switch(state=True)
        self._hardware.trigger_counter.count_freq = int(1000 / self.dwell_time)

        self.freq_points = np.linspace(self.start_freq, self.stop_freq, self.num_of_step, endpoint=False)
        for loop in range(self.num_of_ave):
            data_loop = []
            if self.running is False:
                break
            for freq in self.freq_points:
                try:
                    self._hardware.MW_source.set_freq(freq=freq)
                    self._hardware.trigger_counter.init_task()
                    self._hardware.trigger_counter.counter_start()
                    data_loop.append(self._hardware.trigger_counter.get_counts())
                except BaseException as e:
                    print(e)
                    self._hardware.MW_source.switch(state=False)
                    self._hardware.trigger_counter.close_task()
                    self.running = False
                    return
            self.update.emit(data_loop)

        self.self._hardware.MW_source.switch(state=False)
        self.running = False

    # def run(self):
    #     self.running = True
    #     print('started thread')
    #     self.hardware.pulser.parameters = self.parameters
    #     self.hardware.sweeper.parameters = self.parameters
    #     self.hardware.trigger_counter.parameters = self.parameters
    #
    #     self.hardware.sweeper.sweep_settings()
    #     self.hardware.pulser.setup()
    #
    #     for i in range(self.parameters['NumOfAvgs']):
    #         if not self.running:
    #             break
    #         self.hardware.trigger_counter.init_tasks()
    #         self.hardware.pulser.run_once()
    #         data = self.hardware.trigger_counter.get_counts_array()
    #         self.update.emit(data)
