#!./venv/bin/python
from websocket import create_connection
import json

# The IP address can be retrieved by going to the CNC computer
# and typing "ipconfig" into the command prompt.
# FUTURE: Possibly have a service on the machine that broadcasts/registers the
# cnc machine's IP to make this more robust?
cnc_ws_url = 'ws://10.0.1.14:8989/ws'
cnc_serial_port = 'COM6'
cnc_serial_baud_rate = 115200  # Seems to be default, https://github.com/chilipeppr/widget-spjs/blob/dc6670e/widget.js#L219

__count = 0


def gen_json_str(key=None, value=None, id=None):
    global __count
    if not id:
        id = 'console{}'.format(__count)
        __count += 1
    if key or value:
        data = '${}={}\n'.format(key, value)
    else:
        data = ""
    json_dumps = json.dumps({'P': cnc_serial_port, 'Data': [{'D': data, 'Id': id}]})
    return str(json_dumps)


if __name__ == '__main__':
    print('Connecting to: {}'.format(cnc_ws_url))
    socket = create_connection(cnc_ws_url)


    def send_raw_str(raw_str=None):
        print('<<{}'.format(raw_str))
        socket.send(raw_str)
        while True:
            # When working at this low level of communication, we won't have an actual protocol
            # to facilitate communication. Normally this is terminated in http by closing the
            # connection, or by a content length header or one of the other ways http delimits
            # communication.
            #
            # I've deduced that after sending a command to the serial-port-json-server, the server
            # will send responses, but to indicate it is done it will send back the command you sent
            # first followed by another additional message.
            response = socket.recv()
            if response == raw_str:
                print('>>{}'.format(response))
                print('>>{}\n'.format(socket.recv()))
                break
            print('>>{}'.format(response))


    def send_json(key=None, value=None, id=None):
        json_str = gen_json_str(key, value, id)
        send_raw_str('sendjson {}'.format(json_str))


    send_raw_str('close {}'.format(cnc_serial_port))
    send_raw_str('open {} {} tinygg2'.format(cnc_serial_port, cnc_serial_baud_rate))
    send_json(id='startup0')
    # Start Firmware Instructions
    # Page 1
    send_json('ja', 0.25)
    send_json('ct', 0.0100)
    send_json('sl', 0)
    send_json('lim', 1)
    send_json('saf', 1)
    send_json('mt', 2.00)
    send_json('m48e', 1)
    send_json('mfoe', 0)
    send_json('mfo', 1)
    send_json('spep', 1)
    send_json('spdp', 0)
    send_json('spph', 1)
    send_json('spdw', 1.0)
    send_json('cofp', 1)
    send_json('comp', 1)
    send_json('coph', 0)
    send_json('tv', 1)
    send_json('ej', 0)  # We don't want json mode enabled?
    send_json('jv', 2)  # This doesn't change from 0, probably because ej (enable json mode) is disabled
    send_json('js', 1)
    send_json('sv', 1)
    send_json('si', 250)
    send_json('gpl', 0)
    send_json('gun', 1)
    send_json('gco', 1)
    send_json('gpa', 2)
    send_json('gdi', 0)
    send_json('1ma', 0)
    send_json('1sa', 1.800)
    send_json('1tr', 5)  # The printout shows 40.0000, but 5 is penned in TODO: find out why
    send_json('1mi', 8)
    send_json('1po', 0)
    send_json('1pm', 2)
    send_json('1pl', 0.375)
    send_json('2ma', 1)
    send_json('2sa', 1.800)
    send_json('2tr', 40.0000)  # Why isn't this 5 too? TODO: find out why
    # Page 2
    send_json('2mi', 8)
    send_json('2po', 1)  # 1 is penned in, instead of 0 TODO: find out why
    send_json('2pm', 2)
    send_json('2pl', 0.375)
    send_json('3ma', 2)  # 2 is penned in, instead of 1 TODO: find out why
    send_json('3sa', 1.800)
    send_json('3tr',
              1)  # There is the printed value of 40, then someone penned in 5, then that was scratched out for 1 TODO: find out why
    send_json('3mi', 8)
    send_json('3po', 1)  # not the droid we're looking for
    send_json('3pm', 2)
    send_json('3pl', 0.375)
    send_json('4ma', 2)
    send_json('4sa', 1.800)
    send_json('4tr', 1.2500)
    send_json('4mi', 8)
    send_json('4po', 0)
    send_json('4pm', 2)
    send_json('4pl', 0.750)
    send_json('5ma', 4)
    send_json('5sa', 1.800)
    send_json('5tr', 360.0000)
    send_json('5mi', 8)
    send_json('5po', 0)
    send_json('5pm', 2)
    send_json('5pl', 0.000)
    send_json('6ma', 5)
    send_json('6sa', 1.800)
    send_json('6tr', 360.0000)
    send_json('6mi', 8)
    send_json('6po', 0)
    send_json('6pm', 2)
    send_json('6pl', 0.000)
    send_json('xam', 1)
    send_json('xvm', 50000)
    send_json('xfr', 50000)
    send_json('xtn', 0.000)
    send_json('xtm', 420.000)
    send_json('xjm', 10000)
    send_json('xjh', 20000)
    send_json('xjd', 0)
    send_json('xhi', 1)
    send_json('xhd', 0)
    send_json('xsv', 3000)
    # Page 3
    send_json('xlv', 100.00)
    send_json('xlb', 20.000)
    send_json('xzb', 3.000)
    send_json('yam', 1)
    send_json('yvm', 50000)
    send_json('yfr', 50000)
    send_json('ytn', 0.000)
    send_json('ytm', 420.000)
    send_json('yjm', 10000)
    send_json('yjh', 20000)
    send_json('yjd', 0)
    send_json('yhi', 3)
    send_json('yhd', 0)
    send_json('ysv', 3000)
    send_json('ylv', 100.00)
    send_json('ylb', 20.000)
    send_json('yzb', 3.000)
    send_json('zam', 1)
    send_json('zvm', 1200)
    send_json('zfr', 1200)
    send_json('ztn', -95.000)
    send_json('ztm', 0.000)
    send_json('zjm', 500)
    send_json('zjh', 500)
    send_json('zjd', 0)
    send_json('zhi', 6)
    send_json('zhd', 1)
    send_json('zsv', 800)
    send_json('zlv', 100)
    send_json('zlb', 10.000)
    send_json('zzb', 2.000)
    send_json('aam', 1)
    send_json('avm', 60000)
    send_json('afr', 48000)
    send_json('atn', -1.000)
    send_json('atm', -1.000)
    send_json('ajm', 24000)
    send_json('ajh', 24000)
    send_json('ajd', 0.0000)
    send_json('ara', 1.0000)
    send_json('ahi', 0)
    send_json('ahd', 0)
    send_json('asv', 6000)
    send_json('alv', 1000.00)
    send_json('alb', 5.000)
    send_json('azb', 2.000)
    send_json('bam', 0)
    send_json('bvm', 3600)
    # Page 4
    send_json('bfr', 3600)
    send_json('btn', -1.000)
    send_json('btm', -1.000)
    send_json('bjm', 20)
    send_json('bjh', 20)
    send_json('bjd', 0.0000)
    send_json('bra', 1.0000)
    send_json('bhi', 0)
    send_json('bhd', 0)
    send_json('bsv', 6000)
    send_json('blv', 1000.00)
    send_json('blb', 5.000)
    send_json('bzb', 2.000)
    send_json('cam', 0)
    send_json('cvm', 3600)
    send_json('cfr', 3600)
    send_json('ctn', -1.000)
    send_json('ctm', -1.000)
    send_json('cjm', 20)
    send_json('cjh', 20)
    send_json('cjd', 0.0000)
    send_json('cra', 1.0000)
    send_json('chi', 0)
    send_json('chd', 0)
    send_json('csv', 6000)
    send_json('clv', 1000.00)
    send_json('clb', 5.000)
    send_json('czb', 2.000)
    send_json('p1frq', 100)
    send_json('p1csl', 7900)
    send_json('p1csh', 12800)
    send_json('p1cpl', 0.130)
    send_json('p1cph', 0.170)
    send_json('p1wsl', 0)
    send_json('p1wsh', 0)
    send_json('p1wpl', 0.100)
    send_json('p1wph', 0.100)
    send_json('p1pof', 0.100)
    send_json('chd', 0)
    send_json('csv', 6000)  # Duplicate, see above.
    send_json('clv', 1000.00)  # Duplicate, see above.
    send_json('clb', 5.000)  # Duplicate, see above.
    send_json('czb', 2.000)  # Duplicate, see above.
    send_json('g54x', 0.000)
    send_json('g54y', 0.000)
    send_json('g54z', 0.000)
    send_json('g54a', 0.000)
    send_json('g54b', 0.000)
    # Page 5
    send_json('g54c', 0.000)
    send_json('g55x', 0.000)
    send_json('g55y', 0.000)
    send_json('g55z', 0.000)
    send_json('g55a', 0.000)
    send_json('g55b', 0.000)
    send_json('g55c', 0.000)
    send_json('g56x', 0.000)
    send_json('g56y', 0.000)
    send_json('g56z', 0.000)
    send_json('g56a', 0.000)
    send_json('g56b', 0.000)
    send_json('g56c', 0.000)
    send_json('g57x', 0.000)
    send_json('g57y', 0.000)
    send_json('g57z', 0.000)
    send_json('g57a', 0.000)
    send_json('g57b', 0.000)
    send_json('g57c', 0.000)
    send_json('g58x', 0.000)
    send_json('g58y', 0.000)
    send_json('g58z', 0.000)
    send_json('g58a', 0.000)
    send_json('g58b', 0.000)
    send_json('g58c', 0.000)
    send_json('g59x', 0.000)
    send_json('g59y', 0.000)
    send_json('g59z', 0.000)
    send_json('g59a', 0.000)
    send_json('g59b', 0.000)
    send_json('g59c', 0.000)
    send_json('g92x', 0.000)
    send_json('g92y', 0.000)
    send_json('g92z', 0.000)
    send_json('g92a', 0.000)
    send_json('g92b', 0.000)
    send_json('g92c', 0.000)
    send_json('g28x', 0.000)
    send_json('g28y', 0.000)
    send_json('g28z', 0.000)
    send_json('g28a', 0.000)
    send_json('g28b', 0.000)
    send_json('g28c', 0.000)
    send_json('g30x', 0.000)
    send_json('g30y', 0.000)
    send_json('g30z', 0.000)
    send_json('g30a', 0.000)
    send_json('g30b', 0.000)
    send_json('g30c', 0.000)
    # Paper scrap stapled to the back...
    send_json('2tr', 5)  # This overrides the 40.000 that _wasn'_ set to 5 earlier...
    send_json('3ma', 2)  # This doesn't change the value...

    # End Firmware Instructions
    # TODO: Find out, is flushing the queue the correct action to take here? That's what we're doing, anyway.
    send_raw_str('send {} %'.format(cnc_serial_port))
    socket.close()
    print('Complete')
