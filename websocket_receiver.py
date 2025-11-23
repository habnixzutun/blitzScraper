#!/usr/bin/python

import websocket
import rel
from database_helper import *

def on_message(ws, message):
    print(decode(message))

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("### opened ###")
    ws.send('{"a":111}')

def decode(s: str) -> str:
    # Dictionary für neue Codes
    dictionary = {}

    # Aufspalten in einzelne Zeichen
    chars = list(s)

    # Initialwerte
    c = chars[0]
    prev = c
    output = [c]

    # Startwert für neue Einträge
    next_code = 256

    # Schleife über die restlichen Zeichen
    for i in range(1, len(chars)):
        code = ord(chars[i])

        # Bestimme den aktuellen String 'entry'
        if code < 256:
            entry = chars[i]
        elif code in dictionary:
            entry = dictionary[code]
        else:
            # Sonderfall bei LZW: code noch nicht im Dictionary
            entry = prev + c

        output.append(entry)

        # Erstes Zeichen des aktuellen Eintrags
        c = entry[0]

        # Neuen Eintrag ins Dictionary hinzufügen
        dictionary[next_code] = prev + c
        next_code += 1

        prev = entry

    return "".join(output)


def main():

    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws7.blitzortung.org/",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever(dispatcher=rel,
                   reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()



if __name__ == '__main__':
    main()
