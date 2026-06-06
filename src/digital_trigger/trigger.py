import serial

class Trigger:
    def __init__(self, port='COM3', baudrate=115200, timeout=0, names=None, simulate=False):
        self.bitmask = 0
        self.names = names
        self.simulate = simulate
        if not simulate:
            self.port = serial.Serial(port, baudrate, timeout=timeout)
            self.reset()
            self.write()

    # -- line number handling ------------------------------------------

    def name2line(self, name):
        if self.names is None:
            raise ValueError("No line names were set. Pass names=[...] to Trigger(), or use line numbers.")
        return self.names.index(name) + 1

    def get_line_numbers(self, lines):
        # Wrap a single item so everything below can assume an iterable.
        if isinstance(lines, (str, int)):
            lines = [lines]

        numbers = []
        for line in lines:
            if isinstance(line, str):
                line = self.name2line(line)
            else:
                line = int(line)
            if not 1 <= line <= 8:
                raise ValueError("Line number must be between 1 and 8")
            numbers.append(line)
        return numbers

    # -- trigger control -------------------------------------------------

    def open(self, line):
        for l in self.get_line_numbers(line):
            self.bitmask |= (1 << (l - 1))
        self.write()

    def close(self, line):
        for l in self.get_line_numbers(line):
            self.bitmask &= ~(1 << (l - 1))
        # self.port.flush()  # blocks until byte is sent - not necessary
        self.write()

    def close_all(self):
        self.bitmask = 0
        self.write()

    # -- serial I/O ------------------------------------------------------

    def reset(self):
        self.bitmask = 0
        if not self.simulate:
            # b'' is identical to ''.encode() for something this simple.
            self.port.write(b'RR')  # 'RR' is a device-specific command to reset.
        else:
            print('Port reset')

    def write(self):
        # See documentation at the bottom here: https://www.blackboxtoolkit.com/support_usb_ttl_module.html
        payload = format(self.bitmask, '02X')
        if not self.simulate:
            self.port.write(payload.encode())
        else:
            print('Hex code written: ' + payload)
            # self.open_lines()

    def stop(self):
        if self.simulate or not hasattr(self, 'port') or not self.port.is_open:
            return  # already stopped, or never opened
        print('Shutting down port')
        self.reset()
        self.port.close()
        print('Port is closed: ', not self.port.is_open)

    # -- OPTIONAL EXTRAS -------------------------------------------------
    # -- display -------------------------------------------------

    def is_open(self, lines):
        return all(self.status(lines))

    def is_closed(self, lines):
        return not any(self.status(lines))

    def status(self, lines=None):
        if lines is None:
            lines = range(1, 9)

        matches = []
        for l in self.get_line_numbers(lines): # simplify
            is_open = self.bitmask & (1 << (l - 1))
            matches.append(bool(is_open))  # Unsure if should convert to bool or not?
            # print(f"Line {str(l)} is {'open' if is_open else 'closed'} {self.line2name(l)}")
        return matches

    def open_lines(self):
        lines = []
        for l in range(8):
            if self.bitmask & (1 << l):
                lines.append(l + 1)
        print('Open lines:', lines, "{:08b}".format(self.bitmask))
        return lines

    def line2name(self, line):
        if self.names is None:
            return []
        if isinstance(line, int):
            line = [line]

        line_names = []
        for l in line:
            l = int(l) #just incase it's a numpy int
            if 1 <= l <= len(self.names):
                line_names.append(self.names[l - 1])
            else:
                line_names.append('unnamed')
        return line_names

    def hex(self):
        return f"{self.bitmask:02X}"

    def binary(self):
        return f"{self.bitmask:08b}"

    # -- context manager support ----------------------------------------

    def __repr__(self):
        return f"Trigger(bitmask={self.binary()}, open_lines={self.open_lines()})"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        return False
