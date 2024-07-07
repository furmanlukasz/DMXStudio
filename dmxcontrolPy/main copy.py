import argparse
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from DMXEnttecPro import Controller
from DMXEnttecPro.utils import get_port_by_serial_number

# Initialize the DMX controller
my_port = get_port_by_serial_number('EN189424')
dmx = Controller(my_port)

# Initialize color values
colors = {"R": 0, "G": 0, "B": 0}

# Handlers for OSC messages
def samplerate_handler(unused_addr, *args):
    samplerate = args[0]
    print("[Samplerate] ~ Samplerate: {0}".format(samplerate))
    # You can handle samplerate changes here

def dimmer_handler(unused_addr, *args):
    dimmer = int(args[0])  # Convert to integer
    print("[Dimmer] ~ Dimmer: {0}".format(dimmer))
    dmx.set_channel(1, dimmer)
    dmx.submit()

def red_handler(unused_addr, *args):
    r = int(args[0])  # Convert to integer
    colors["R"] = r
    print("[Color] ~ R: {0}".format(r))
    update_dmx_colors()

def green_handler(unused_addr, *args):
    g = int(args[0])  # Convert to integer
    colors["G"] = g
    print("[Color] ~ G: {0}".format(g))
    update_dmx_colors()

def blue_handler(unused_addr, *args):
    b = int(args[0])  # Convert to integer
    colors["B"] = b
    print("[Color] ~ B: {0}".format(b))
    update_dmx_colors()

def strobo_handler(unused_addr, *args):
    strobo = int(args[0])  # Convert to integer
    print("[Strobo] ~ Strobo: {0}".format(strobo))
    # Handle strobo changes here

def makra_handler(unused_addr, *args):
    makra = int(args[0])  # Convert to integer
    print("[Makra] ~ Makra: {0}".format(makra))
    # Handle makra changes here

def update_dmx_colors():
    dmx.set_channel(2, colors["R"])
    dmx.set_channel(3, colors["G"])
    dmx.set_channel(4, colors["B"])
    dmx.submit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=10000, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/_samplerate", samplerate_handler)
    dispatcher.map("/Dimmer", dimmer_handler)
    dispatcher.map("/R", red_handler)
    dispatcher.map("/G", green_handler)
    dispatcher.map("/B", blue_handler)
    dispatcher.map("/Strobo", strobo_handler)
    dispatcher.map("/Makra", makra_handler)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
