## CNC Firmware Resetter
We have a community CNC machine. This is great, but sometimes various applications will change the values of the firmware or someone might change something on accident. There are many options and settings to keep track of. These two facts in tandem make keeping the machine in a consistent state a difficult thing to maintain. Fortunately, we're using [serial-port-json-server](https://github.com/chilipeppr/serial-port-json-server) to facilitate communication from the computer to the CNC machine.

Because JSON is a fairly easy thing to build and websockets are fairly agnostic we can write a script to automate the process of setting the machine to a given state.

## Running
After cloning the repository, you need to run `initialize-venv.sh` script. This will create a sandboxed python3 instance so we can install dependencies without effecting the system's installed python packages. After that, you can run the `reset-firmware.py` script like any other executable script. If, for whatever reason, the venv python instance isn't running the script; then in bash run `source ./venv/bin/activate`. This will divert python to the venv instance. Run the script with the python command: `python ./reset-firmware`. Afterwards run `deactivate` to leave the venv.
