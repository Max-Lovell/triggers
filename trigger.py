import serial


class Trigger:
    def __init__(self, port='COM3', baudrate=115200, timeout=0, names=None):
        self.bitmask = 0
        self.names = names
        self.port = serial.Serial(port, baudrate, timeout=timeout)
        self.reset()
        self.write()

    # -- line number handling ------------------------------------------

    def name2line(self, name: str):
        return self.names.index(name) + 1

    def line2name(self, line: int):
        if len(self.names) > line: return ''
        return self.names[line]

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

    # -- trigger control -------------------------------------------------

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

    # -- serial I/O ------------------------------------------------------

    def reset(self):
        # b'' is identical to ''.encode() for something this simple.
        self.port.write(b'RR')  # 'RR' is a device-specific command to reset.

    def write(self):
        # See documentation at the bottom here: https://www.blackboxtoolkit.com/support_usb_ttl_module.html
        payload = format(self.bitmask, '02X')
        self.port.write(payload.encode())

    def stop(self):
        print('Shutting down port')
        self.reset()
        self.port.close()
        print('Port is closed: ', not self.port.is_open)

    # -- context manager support ----------------------------------------

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False
