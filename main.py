import serial


class Trigger:
    def __init__(self, port='COM3', baudrate=115200, timeout=0, names=None):
        self.bitmask = 0
        self.names = names
        self.port = serial.Serial(port, baudrate, timeout=timeout)
        self.reset()
        self.write()

    def name2line(self, name: str):
        return self.names.index(name) + 1

    def get_line_numbers(self, lines):
        # Wrap a single item so everything below can assume an iterable.
        if isinstance(lines, (str, int)):
            lines = [lines]

        numbers = []
        for line in lines:
            if isinstance(line, str):
                line = self.name2line(line)
            numbers.append(line)
        return numbers

    def open(self, line):
        for l in self.get_line_numbers(line):
            self.bitmask |= (1 << (l - 1))
        # self.write()

    def close(self, line):
        for l in self.get_line_numbers(line):
            self.bitmask &= ~(1 << (l - 1))
        # self.port.flush()  # blocks until byte is sent - not necessary
        # self.write()

    def close_all(self):
        self.bitmask = 0
        # self.write()

    def print_lines(self):
        # print numbers
        open_lines = []
        for l in range(8):
            new_bitmask = self.bitmask & ~(1 << l)
            if self.bitmask != new_bitmask:
                open_lines.append(l + 1)
        print('Open lines:', open_lines, "{:08b}".format(self.bitmask))
        return open_lines

    def reset(self):
        self.port.write(b'RR')

    def write(self):
        self.port.write(bytes([self.bitmask]))

    def stop(self):
        print('Shutting down port')
        self.reset()
        self.port.close()
        print('Port is closed: ', not self.port.is_open)


if __name__ == '__main__':
    port = Trigger('COM4', names=['condition_1', 'condition_2', 'stim_1', 'stim_2'])
    port.open(['condition_1', 'stim_1'])
    port.close('stim_1')
    port.open('stim_2')
    port.close('stim_1')
    port.open(8)
    port.print_lines()
    port.stop()
