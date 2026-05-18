# digital-trigger

Easier sending of digital triggers/event markers/TTL signals using the Serial (pySerial) package a Black Box Toolkit USB TTL module in python and PsychoPy.

## Install

```bash
pip install digitaltrigger
```

Requires Python 3.8+ and [`pyserial`](https://pypi.org/project/pyserial/) (installed automatically). 

In PsychoPy you can install packages in the Builder GUI by going to: 
Tools > Plugins and packages manager > Packages > Open PIP terminal, and run  `pip install digital-trigger`

To find COM port number: 
- run the command `python -m serial.tools.list_ports -v`
- On Windows, open Device Manager, expand "Ports (COM & LPT)", unplug and replug to see which is your device
- On Mac run `ls /dev/cu.*` in Terminal and look for something like /dev/cu.usbserial-XXXX or /dev/cu.usbmodemXXXX — use the cu.* name, not tty.*. 
- On Linux, run ls `/dev/ttyUSB* /dev/ttyACM*` — USB-serial adapters are usually `ttyUSB0`
- Arduino-style boards `ttyACM0; dmesg | tail` right after plugging in shows the assigned name, and you may need to add yourself to the dialout group for permission.

## Usage

### PsychoPy

Add the following in a 'custom code block' in the routine where your stimuli are presented. 
Note drag the Code Component so it sits below the stimulus component in the routine view, as PsychoPy runs them top to bottom.
Consider managing the triggers using a 'trigger_line' variable in your conditions file.

#### Before Experiment

```
from digital_trigger import DigitalTrigger
port = DigitalTrigger('COM4', names=['cond_1', 'cond_2', 'stim_1', 'stim_2'])
```

Note you can only do this once per experiment. 
Don't do this in multiple code blocks in different routines or you will get a 'access/permission denied' error. 
Probably best to have a single code block jsut for this in your first routine even.

#### Begin Routine
```
trigger_opened = False
trigger_closed = False
```

#### Each Frame 
```
# Open the line the instant the stimulus is drawn to the screen...
# Change 'image' to the name of your stimulus component
if image.status == STARTED and not trigger_opened:
    win.callOnFlip(port.open, 'stim_1')
    trigger_opened = True

# ...and close it the instant the stimulus is removed.
if image.status == FINISHED and not trigger_closed:
    win.callOnFlip(port.close, 'stim_1')
    trigger_closed = True
```

#### End Routine
```
if not trigger_closed:
    port.close('stim_1')
```

#### End Experiment
```
port.stop()
```

### Python

```python
from digitaltrigger import Trigger

port = Trigger('COM4', names=['cond_1', 'cond_2', 'stim_1', 'stim_2'])

port.open('stim_1')          # turn a line on  (by name)
port.open([1, 'cond_2'])     # turn several on (numbers and names mixed)
port.close('stim_1')         # turn one off
port.close_all()             # turn everything off
port.print_lines()           # -> [2] and prints the bitmask

port.stop()                  # reset all lines and close the port
```

Or as a context manager, which closes the port for you:

```python
with Trigger('COM4', names=['stim_1']) as trig:
    trig.open('stim_1')
```

Resources:
- https://www.blackboxtoolkit.com/support_usb_ttl_module.html
- https://www.blackboxtoolkit.com/docs/pdf/USBTTLv1r19.pdf
- https://psychopy.org/developers/pluginDevGuide.html#plugindevguide