import argparse
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from DMXEnttecPro import Controller
from DMXEnttecPro.utils import get_port_by_serial_number

# Initialize the DMX controller
my_port = get_port_by_serial_number('EN189424')
dmx = Controller(my_port)

# Initialize fixture values
fixtures_6ch = [{"Dimmer": 0, "R": 0, "G": 0, "B": 0, "Strobe": 0, "Makra": 0} for _ in range(4)]
fixtures_7ch = [{"Dimmer": 0, "R": 0, "G": 0, "B": 0, "Strobe": 0, "AutoMode": 0, "AutoModeSpeed": 0} for _ in range(4)]

# Base addresses for fixtures
base_addresses_6ch = [1, 7, 13, 19]  # Assuming 6 channels each
base_addresses_7ch = [25, 32, 39, 46]  # Assuming 7 channels each

# Handlers for OSC messages
def fixture_6ch_handler(unused_addr, *args):
    fixture_idx = int(args[0])
    channel_name = args[1]
    value = int(args[2])

    if fixture_idx < 0 or fixture_idx >= len(fixtures_6ch):
        print(f"Invalid fixture index: {fixture_idx}")
        return

    if channel_name not in fixtures_6ch[fixture_idx]:
        print(f"Invalid channel name: {channel_name}")
        return

    fixtures_6ch[fixture_idx][channel_name] = value
    print(f"Fixture {fixture_idx} [{channel_name}] ~ {value}")
    update_dmx_fixture_6ch(fixture_idx)

def fixture_7ch_handler(unused_addr, *args):
    fixture_idx = int(args[0])
    channel_name = args[1]
    value = int(args[2])

    if fixture_idx < 0 or fixture_idx >= len(fixtures_7ch):
        print(f"Invalid fixture index: {fixture_idx}")
        return

    if channel_name not in fixtures_7ch[fixture_idx]:
        print(f"Invalid channel name: {channel_name}")
        return

    fixtures_7ch[fixture_idx][channel_name] = value
    print(f"Fixture {fixture_idx} [{channel_name}] ~ {value}")
    update_dmx_fixture_7ch(fixture_idx)

def update_dmx_fixture_6ch(fixture_idx):
    base_address = base_addresses_6ch[fixture_idx]
    fixture = fixtures_6ch[fixture_idx]
    dmx.set_channel(base_address, fixture["Dimmer"])
    dmx.set_channel(base_address + 1, fixture["R"])
    dmx.set_channel(base_address + 2, fixture["G"])
    dmx.set_channel(base_address + 3, fixture["B"])
    dmx.set_channel(base_address + 4, fixture["Strobe"])
    dmx.set_channel(base_address + 5, fixture["Makra"])
    dmx.submit()

def update_dmx_fixture_7ch(fixture_idx):
    base_address = base_addresses_7ch[fixture_idx]
    fixture = fixtures_7ch[fixture_idx]
    dmx.set_channel(base_address, fixture["Dimmer"])
    dmx.set_channel(base_address + 1, fixture["R"])
    dmx.set_channel(base_address + 2, fixture["G"])
    dmx.set_channel(base_address + 3, fixture["B"])
    dmx.set_channel(base_address + 4, fixture["Strobe"])
    dmx.set_channel(base_address + 5, fixture["AutoMode"])
    dmx.set_channel(base_address + 6, fixture["AutoModeSpeed"])
    dmx.submit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="0.0.0.0", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=10000, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/fixture_6ch", fixture_6ch_handler)
    dispatcher.map("/fixture_7ch", fixture_7ch_handler)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
