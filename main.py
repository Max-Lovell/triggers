import serial

class Trigger:
    def __init__(self, port = 3, baudrate = 115200, timeout = None, names = None):
        self.bitmask = 0
        self.names = names
        self.port = 'COM'+str(port)
        self.baudrate = baudrate
        # self.port = serial.Serial(port)
        # self.port.baudrate = baudrate
        #if timeout is not None:
            # self.port.timeout = timeout
        #else:
            #self.port.timeout = 0
        # self.port.write('RR'.encode())
        # self.write()

    def name2line(self, name: str):
        return self.names.index(name)+1

    def open(self, line):
        # Convert name to line number from array
        if isinstance(line, str):
            line = self.name2line(line)

        # if not array, trigger line
        if isinstance(line, int): # if just 1 number
            self.bitmask |= (1 << (line - 1))

        # if array, loop and trigger
        elif hasattr(line, "__len__"):
            for l in line:
                if isinstance(l, str):
                    l = self.name2line(l)
                self.bitmask |= (1 << (l-1))

        # self.write()

    def close(self, line):
        # Convert name to line number from array
        if isinstance(line, str):
            line = self.name2line(line)

        # if not array, trigger line
        if isinstance(line, int):  # if just 1 number
            # ~ = flip all bits in new number, & means keep any 1s and 0 everything else
            self.bitmask &= ~(1 << (line-1))

        # if array, loop and trigger
        elif hasattr(line, "__len__"):
            for l in line:
                if isinstance(l, str):
                    l = self.name2line(l)
                self.bitmask &= ~(1 << (l-1))

        #self.port.flush()  # blocks until byte is sent - not necessary
        #self.write()

    def close_all(self):
        self.bitmask = 0
        #self.write()

    def print_lines(self):
        # print numbers
        open_lines = []
        for l in range(8):
            new_bitmask = self.bitmask & ~(1 << l)
            if self.bitmask != new_bitmask:
                open_lines.append(l+1)
        print('Open lines:', open_lines, "{:08b}".format(self.bitmask))
        return open_lines

    def write(self):
        print(self.bitmask)
        # self.port.write(bytes([self.bitmask]))

    def stop(self):
        print('Shutting down port')
        #self.port.write('RR'.encode())
        #self.port.close()
        #print('Port is closed: ', not self.port.is_open)

if __name__ == '__main__':
    port = Trigger('COM4', names=['condition_1','condition_2','stim_1','stim_2'])
    port.open(['condition_1','stim_1'])
    port.close('stim_1')
    port.open('stim_2')
    port.close('stim_1')
    port.open(8)
    port.print_lines()
    port.stop()