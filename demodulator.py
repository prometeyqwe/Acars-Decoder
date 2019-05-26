# -*- coding: utf-8 -*-
import numpy as np
import wave


class Demodulator:
    def __init__(self, path):
        x = np.linspace(-np.pi, np.pi, 20)
        x1 = np.linspace(0, 2*np.pi, 20)

        sin_24_0 = np.sin(x)
        sin_24_1 = - np.sin(x)
        sin_12_0 = np.sin(x1/2)
        sin_12_1 = -np.sin(x1/2)

        self.path = path
        self.channel = []
        self.results = [1, 0, 1, 0]
        self.models = [sin_24_1, sin_24_0, sin_12_1, sin_12_0]

    @staticmethod
    def search_max(a):
        el_max = a[0]
        for elm in a[1:]:
            if elm > el_max:
                el_max = elm
        if el_max == a[0] or el_max == a[-1]:
            return False
        else:
            return True

    @staticmethod
    def search_min(a):
        el_min = a[0]
        for elm in a[1:]:
            if elm < el_min:
                el_min = elm
        if el_min == a[0] or el_min == a[-1]:
            return False
        else:
            return True

    def sub_compare(self, from_signal, pre_res):
        if (self.search_max(from_signal) == self.search_max(pre_res)) and (
                self.search_min(from_signal) == self.search_min(pre_res)):
            return True
        else:
            False

    def compare(self, x):
        res2 = []
        res1 = self.models[:]
        res1.sort(key=(lambda model: (x * model).sum()), reverse=True)

        for i in range(len(res1)):
            for j in range(len(self.models)):
                if all(res1[i] == self.models[j]):
                    res2.append(self.results[j])
                    break

        for i in range(len(res1)):
            if self.sub_compare(x, res1[i]):
                return res2[i]
        return '*'

    def read_wav(self):
        types = {
            1: np.int8,
            2: np.int16,
            4: np.int32
        }

        wav = wave.open(self.path, mode="r")
        (nchannels, sampwidth, framerate, nframes, comptype, compname) = \
            wav.getparams()

        content = wav.readframes(nframes)
        samples = np.fromstring(content, dtype=types[sampwidth])
        self.channel = samples[::1]
        self.channel = self.channel[30543:]

        print("Число каналов: {}".format(nchannels))
        print("Число байт на сэмпл: {}".format(sampwidth))
        print("Число фреймов в секунду: {}".format(framerate))
        print("Общее число фреймов: {}".format(nframes))
        print("Тип сжатия: {}".format(comptype))
        print("Имя типа сжатия: {}".format(compname))

    def demodulate(self):
        self.read_wav()
        res = []
        for i in range(len(self.channel) / 20):
            x = self.channel[i * 20:(i + 1) * 20]
            res.append(self.compare(x))
        f = open('result_of_demodulate.txt', 'w')
        for i in res:
            f.write(str(i))

        f.close()


if __name__ == "__main__":
    demodulator = Demodulator(path='rec1_8bits.wav')
    demodulator.demodulate()
