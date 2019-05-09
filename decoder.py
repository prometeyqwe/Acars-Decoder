# -*- coding: utf-8 -*-
# from itertools import chain


class Decoder:
    def __init__(self):
        self.table = [
            ["NUL", "DLE", "SP", "0", "@", "P", "`", "p"],
            ["SOH", "DC1", "!", "1", "A", "Q", "a", "q"],
            ["STX", "DC2", "\"", "2", "B", "R", "b", "r"],
            ["ETX", "DC3", "#", "3", "C", "S", "c", "s"],
            ["EOT", "DC4", "$", "4", "D", "T", "d", "t"],
            ["ENQ", "NAK", "%", "5", "E", "U", "e", "u"],
            ["ACK", "SYN", "&", "6", "F", "V", "f", "v"],
            ["BEL", "ETB", "'", "7", "G", "W", "g", "w"],
            ["BS", "CAN", "(", "8", "H", "X", "h", "x"],
            ["HT", "EM", ")", "9", "I", "Y", "i", "y"],
            ["LF", "SUB", "*", ":", "J", "Z", "j", "z"],
            ["VT", "ESC", "+", ";", "K", "[", "k", "{"],
            ["FF", "FS", ",", "<", "L", "\\", "l", "/"],
            ["CR", "GS", "-", "=", "M", "]", "m", "}"],
            ["SO", "RS", ".", ">", "N", "'", "n", "'"],
            ["SI", "US", "/", "?", "O", "_", "o", "DEL"],
        ]
        self.data = ""
        self.arr_data = []

    def read_data(self):
        input_data = open("./result_of_demodulate.txt")
        for i in input_data:
            self.data += str(i)
        self.data = self.data[11:]
        for i in range(len(self.data)//8):
            self.arr_data.append(self.data[0+8*i:8+i*8])

    def fix_parity_bit_error(self):
        count = 0
        for i in range(len(self.arr_data)):
            if (self.arr_data[i][-1] == '*') and (
                    self.arr_data[i].count('*') == 1):
                count += 1
                if self.arr_data.count('1') % 2 == 0:
                    self.arr_data[i] = self.arr_data[i].replace('*', '0')
                else:
                    self.arr_data[i] = self.arr_data[i].replace('*', '1')

    def fix_ones_bit_error(self):
        for i in range(len(self.arr_data)):
            if self.arr_data[i].count('*') == 1:
                if self.arr_data[i].count('1') % 2 == 0:
                    self.arr_data[i] = self.arr_data[i].replace('*', '1')
                else:
                    self.arr_data[i] = self.arr_data[i].replace('*', '0')

    def decode(self):
        pre_result = []
        self.read_data()
        for i in range(len(self.arr_data)):
            if '*' not in self.arr_data[i]:
                pre_result.append((self.table[int(self.arr_data[i][-5::-1], 2)][int(self.arr_data[i][-2:3:-1], 2)]))
            else:
                pre_result.append('*')

        result = "Acars mode: {0}  Aircraft reg: {1} \nMessage label: {2}  Block id: {3}  Msg. no: {4}\nFlight id: {5}\nMessage_content:-\n{6}".format(
            pre_result[5], "".join(pre_result[6:13]), "".join(pre_result[14:16]), pre_result[16], "".join(pre_result[18:22]),
            "".join(pre_result[22:28]), "".join(pre_result[29:pre_result.index('ETX')]))
        print(result)


if __name__ == "__main__":
    decoder = Decoder()
    decoder.decode()
