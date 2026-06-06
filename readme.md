# digital-trigger

Easier sending of digital triggers/event markers/TTL signals using the Serial (pySerial) package with a Black Box Toolkit USB TTL module in Python and PsychoPy.

## Install

```bash
pip install digital_trigger
```

Requires Python 3.8+ and [`pyserial`](https://pypi.org/project/pyserial/) (installed automatically). 

In PsychoPy you can install packages in the Builder GUI by going to: 
Tools > Plugins and packages manager > Packages > Open PIP terminal, and run  `pip install digital-trigger`


## Usage

### PsychoPy

Add the following in a 'custom code block' in the routine where your stimuli are presented. 
Note drag the Code Component so it sits below the stimulus component in the routine view, as PsychoPy runs them top to bottom.
Consider managing the triggers using a 'trigger_line' variable in your conditions file.

#### Before Experiment

```
from digital_trigger import Trigger
port = Trigger('COM4', names=['cond_1', 'cond_2', 'stim_1', 'stim_2'])
```

Note you can only do this once per experiment or you will get an 'access/permission denied' error.
Watch out if you insert the same routine twice as a copy.

#### Each Frame 
```
if image.status == STARTED and port.is_closed(condition):
    win.callOnFlip(port.open, condition)

if image.status == FINISHED and port.is_open(condition):
    win.callOnFlip(port.close, condition)
```

OR, more simply:
```
port.sync_to_component(condition, image, win)
```

#### End Experiment
```
port.stop()
```

### Python

```python
from digital_trigger import Trigger

port = Trigger('COM4', names=['cond_1', 'cond_2', 'stim_1', 'stim_2'])

port.open('stim_1')          # turn a line on  (by name)
port.open([1, 'cond_2'])     # turn several on (numbers and names mixed)
port.close('stim_1')         # turn one off
port.close_all()             # turn everything off
port.open_lines()            # index of open lines and prints the bitmask
port.status()                # list of bools for each port if open or closed

port.stop()                  # reset all lines and close the port
```

Or as a context manager, which closes the port for you:

```python
with Trigger('COM4', names=['stim_1']) as port:
    port.open('stim_1')
```

## Issues

### Finding COM port number
To find COM port number: 
- run the command `python -m serial.tools.list_ports -v`
- On Windows, open Device Manager, expand "Ports (COM & LPT)", unplug and replug to see which is your device
- On Mac run `ls /dev/cu.*` in Terminal and look for something like /dev/cu.usbserial-XXXX or /dev/cu.usbmodemXXXX — use the cu.* name, not tty.*. 
- On Linux, run ls `/dev/ttyUSB* /dev/ttyACM*` — USB-serial adapters are usually `ttyUSB0`
- Arduino-style boards `ttyACM0; dmesg | tail` right after plugging in shows the assigned name, and you may need to add yourself to the dialout group for permission.

Make sure your COM port is set up with a latency of 1ms (or lower) and Baudrate of 115200. This can be done under Device Manager > COM port > Advanced on Windows.

### Module not found on Mac
`ModuleNotFoundError: No module named 'digital_trigger'` error on Mac: PsychoPy 2025 issue with install path typo.
Confirm by running this inside a code component in psychopy: 
```
import sys
print(sys.executable)
for p in sys.path:
    print("  ", p)
```
see if package is installed to python3.1 instead of python3.10.
- also `show digital-trigger` in PsychoPy's pip terminal (after running `install digital-trigger`) should also state that the package is installed.
- try `find ~/.psychopy3 /Applications/PsychoPy.app -name "digital_trigger*" 2>/dev/null` in terminal

Either install directly using `/Applications/PsychoPy.app/Contents/MacOS/python -m pip install \
    --target ~/.psychopy3/packages/lib/python/site-packages \
    digital-trigger`
or move the directory by running this in a terminal:
```
mv /Applications/PsychoPy.app/Contents/Resources/lib/python3.10/site-packages/digital_trigger \
   ~/.psychopy3/packages/lib/python/site-packages/

mv /Applications/PsychoPy.app/Contents/Resources/lib/python3.10/site-packages/digital_trigger-0.1.2.dist-info \
   ~/.psychopy3/packages/lib/python/site-packages/
```

## Resources:
- https://www.blackboxtoolkit.com/support_usb_ttl_module.html
- https://www.blackboxtoolkit.com/docs/pdf/USBTTLv1r19.pdf
- https://psychopy.org/developers/pluginDevGuide.html#plugindevguide

# Dev notes

#### build & upload
Setup venv:
```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip build twine pytest
```

re-run build:
```
rm -rf dist                # clear old builds so nothing stale is uploaded
python3 -m build
ls dist                    # confirm the new version number is shown
```

Push to PyPi test with `twine upload --repository testpypi dist/*`
Push to PyPi with `twine upload dist/*`

#### test

```
cd /tmp
rm -rf testenv
python3 -m venv testenv
source testenv/bin/activate
pip install -i https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    digital-trigger==0.1.2          # match the version
python -c "from digital_trigger import Trigger; t = Trigger(simulate=True, names=['stim_1']); t.open('stim_1'); print('ok', t.bitmask)"
deactivate
```

To install from the test repo on a new computer:
```
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ digital-trigger==0.1.2
```

Small script to check:
```
from digital_trigger import Trigger
t = Trigger(simulate=True, names=['stim_1'])
t.open('stim_1')
print('ok', t.bitmask)
```

#### release
```
cd /path/to/project         # back to the project folder
twine upload dist/*         # no --repository = real PyPI
```