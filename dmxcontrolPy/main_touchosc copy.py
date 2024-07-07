# import argparse
# from pythonosc.dispatcher import Dispatcher
# from pythonosc import osc_server
# from DMXEnttecPro import Controller
# from DMXEnttecPro.utils import get_port_by_serial_number

# # Initialize the DMX controller
# my_port = get_port_by_serial_number('EN189424')
# dmx = Controller(my_port)

# # Initialize fixture values
# fixtures_6ch = [{"Dimmer": 0, "R": 0, "G": 0, "B": 0, "Strobe": 0, "Makra": 0} for _ in range(4)]
# fixtures_7ch = [{"Dimmer": 0, "R": 0, "G": 0, "B": 0, "Strobe": 0, "AutoMode": 0, "AutoModeSpeed": 0} for _ in range(4)]

# # Base addresses for fixtures
# base_addresses_6ch = [1, 7, 13, 19]  # Assuming 6 channels each
# base_addresses_7ch = [25, 32, 39, 46]  # Assuming 7 channels each

# # Handlers for OSC messages
# def fixture_6ch_handler(unused_addr, *args):
#     try:
#         fixture_idx = int(args[0])
#         r, g, b, dimmer = map(int, args[1:5])

#         if fixture_idx < 0 or fixture_idx >= len(fixtures_6ch):
#             print(f"Invalid fixture index: {fixture_idx}")
#             return

#         fixtures_6ch[fixture_idx]["R"] = r
#         fixtures_6ch[fixture_idx]["G"] = g
#         fixtures_6ch[fixture_idx]["B"] = b
#         fixtures_6ch[fixture_idx]["Dimmer"] = dimmer

#         print(f"Fixture {fixture_idx} [R] ~ {r}, [G] ~ {g}, [B] ~ {b}, [Dimmer] ~ {dimmer}")
#         update_dmx_fixture_6ch(fixture_idx)
#     except Exception as e:
#         print(f"Error processing message: {e}")

# def fixture_7ch_handler(unused_addr, *args):
#     try:
#         fixture_idx = int(args[0])
#         r, g, b, dimmer = map(int, args[1:5])

#         if fixture_idx < 0 or fixture_idx >= len(fixtures_7ch):
#             print(f"Invalid fixture index: {fixture_idx}")
#             return

#         fixtures_7ch[fixture_idx]["R"] = r
#         fixtures_7ch[fixture_idx]["G"] = g
#         fixtures_7ch[fixture_idx]["B"] = b
#         fixtures_7ch[fixture_idx]["Dimmer"] = dimmer

#         print(f"Fixture {fixture_idx} [R] ~ {r}, [G] ~ {g}, [B] ~ {b}, [Dimmer] ~ {dimmer}")
#         update_dmx_fixture_7ch(fixture_idx)
#     except Exception as e:
#         print(f"Error processing message: {e}")

# def update_dmx_fixture_6ch(fixture_idx):
#     base_address = base_addresses_6ch[fixture_idx]
#     fixture = fixtures_6ch[fixture_idx]
#     dmx.set_channel(base_address, fixture["Dimmer"])
#     dmx.set_channel(base_address + 1, fixture["R"])
#     dmx.set_channel(base_address + 2, fixture["G"])
#     dmx.set_channel(base_address + 3, fixture["B"])
#     dmx.set_channel(base_address + 4, fixture["Strobe"])
#     dmx.set_channel(base_address + 5, fixture["Makra"])
#     dmx.submit()

# def update_dmx_fixture_7ch(fixture_idx):
#     base_address = base_addresses_7ch[fixture_idx]
#     fixture = fixtures_7ch[fixture_idx]
#     dmx.set_channel(base_address, fixture["Dimmer"])
#     dmx.set_channel(base_address + 1, fixture["R"])
#     dmx.set_channel(base_address + 2, fixture["G"])
#     dmx.set_channel(base_address + 3, fixture["B"])
#     dmx.set_channel(base_address + 4, fixture["Strobe"])
#     dmx.set_channel(base_address + 5, fixture["AutoMode"])
#     dmx.set_channel(base_address + 6, fixture["AutoModeSpeed"])
#     dmx.submit()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--ip",
#                         default="0.0.0.0", help="The IP to listen on")
#     parser.add_argument("--port",
#                         type=int, default=10000, help="The port to listen on")
#     args = parser.parse_args()

#     dispatcher = Dispatcher()
#     dispatcher.map("/fixture_6ch", fixture_6ch_handler)
#     dispatcher.map("/fixture_7ch", fixture_7ch_handler)

#     server = osc_server.ThreadingOSCUDPServer(
#         (args.ip, args.port), dispatcher)
#     print("Serving on {}".format(server.server_address))
#     server.serve_forever()

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
    try:
        fixture_idx = int(args[0])
        value = list(args[1:])

        if fixture_idx < 0 or fixture_idx >= len(fixtures_6ch):
            print(f"Invalid fixture index: {fixture_idx}")
            return

        fixtures_6ch[fixture_idx]["R"] = value[0]
        fixtures_6ch[fixture_idx]["G"] = value[1]
        fixtures_6ch[fixture_idx]["B"] = value[2]
        fixtures_6ch[fixture_idx]["Dimmer"] = value[3]
        
        update_dmx_fixture_6ch(fixture_idx)
    except Exception as e:
        print(f"Error processing message: {e}")

def fixture_7ch_handler(unused_addr, *args):
    try:
        fixture_idx = int(args[0])
        value = list(args[1:])

        if fixture_idx < 0 or fixture_idx >= len(fixtures_7ch):
            print(f"Invalid fixture index: {fixture_idx}")
            return

        fixtures_7ch[fixture_idx]["R"] = value[0]
        fixtures_7ch[fixture_idx]["G"] = value[1]
        fixtures_7ch[fixture_idx]["B"] = value[2]
        fixtures_7ch[fixture_idx]["Dimmer"] = value[3]
        
        update_dmx_fixture_7ch(fixture_idx)
    except Exception as e:
        print(f"Error processing message: {e}")

def fixture_all_handler(unused_addr, *args):
    try:
        value = list(args[1:])
        for idx in range(len(fixtures_6ch)):
            fixtures_6ch[idx]["R"] = value[0]
            fixtures_6ch[idx]["G"] = value[1]
            fixtures_6ch[idx]["B"] = value[2]
            fixtures_6ch[idx]["Dimmer"] = value[3]
            update_dmx_fixture_6ch(idx)
        for idx in range(len(fixtures_7ch)):
            fixtures_7ch[idx]["R"] = value[0]
            fixtures_7ch[idx]["G"] = value[1]
            fixtures_7ch[idx]["B"] = value[2]
            fixtures_7ch[idx]["Dimmer"] = value[3]
            update_dmx_fixture_7ch(idx)
    except Exception as e:
        print(f"Error processing message: {e}")

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
                        default="0.0.0.0", help="The IP to listen on")
    parser.add_argument("--port",
                        type=int, default=10000, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/fixture_6ch", fixture_6ch_handler)
    dispatcher.map("/fixture_7ch", fixture_7ch_handler)
    dispatcher.map("/fixture_all", fixture_all_handler)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
