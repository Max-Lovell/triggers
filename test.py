# For testing locally

from src.digital_trigger.trigger import Trigger

port = Trigger(names=['stim_1', 'stim_2', 'stim_3'], simulate=True)

port.open(1)
port.close([1,2,3])
port.open([2,3])
port.close(3)

port.open(['stim_1', 'stim_2', 'stim_3'])
port.close('stim_3')

port.open_lines()
print(port.status())

print(port.is_open(2))
print(port.is_closed(2))
print(port.is_closed(3))

print(port.is_open('stim_1'))

