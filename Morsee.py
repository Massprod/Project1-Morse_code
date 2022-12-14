import os
import time
import pyperclip
# Test message to convert: "when in the course of human"
# .-- .... . -.|.. -.|- .... .|-.-. --- ..- .-. ... .|--- ..-.|.... ..- -- .- -.|
# .__ .... . _./.. _./_ .... ./_._. ___ .._ ._. ... ./___ .._./.... .._ __ ._ _./

# International Morse Code
#  1. The length of a dot is one unit
#  2. A dash is three units
#  3. The space between parts of the same letter is one unit
#  4. The space between letters is three units
#  5. The space between words is seven units

option = "menu"
close = False
dot = '.'
line = '_'
morse_encoding = {
    "a": f"{dot} {line}",
    "b": f"{line} {dot} {dot} {dot}",
    "c": f"{line} {dot} {line} {dot}",
    "d": f"{line} {dot} {dot}",
    "e": f"{dot}",
    "f": f"{dot} {dot} {line} {dot}",
    "g": f"{line} {line} {dot}",
    "h": f"{dot} {dot} {dot} {dot}",
    "i": f"{dot} {dot}",
    "j": f"{dot} {line} {line} {line}",
    "k": f"{line} {dot} {line}",
    "l": f"{dot} {line} {dot} {dot}",
    "m": f"{line} {line}",
    "n": f"{line} {dot}",
    "o": f"{line} {line} {line}",
    "p": f"{dot} {line} {line} {dot}",
    "q": f"{line} {line} {dot} {line}",
    "r": f"{dot} {line} {dot}",
    "s": f"{dot} {dot} {dot}",
    "t": f"{line}",
    "u": f"{dot} {dot} {line}",
    "v": f"{dot} {dot} {dot} {line}",
    "w": f"{dot} {line} {line}",
    "x": f"{line} {dot} {dot} {line}",
    "y": f"{line} {dot} {line} {line}",
    "z": f"{line} {line} {dot} {dot}",
    "1": f"{dot} {line} {line} {line} {line}",
    "2": f"{dot} {dot} {line} {line} {line}",
    "3": f"{dot} {dot} {dot} {line} {line}",
    "4": f"{dot} {dot} {dot} {dot} {line}",
    "5": f"{dot} {dot} {dot} {dot} {dot}",
    "6": f"{line} {dot} {dot} {dot} {dot}",
    "7": f"{line} {line} {dot} {dot} {dot}",
    "8": f"{line} {line} {line} {dot} {dot}",
    "9": f"{line} {line} {line} {line} {dot}",
    "0": f"{line} {line} {line} {line} {line}",
    " ": " ",
    ",": f"{line} {line} {dot} {dot} {line} {line}",
    ".": f"{dot} {line} {dot} {line} {dot} {line}",
    "?": f"{dot} {dot} {line} {line} {dot} {dot}",
    "'": f"{dot} {line} {line} {line} {line} {dot}",
    "!": f"{line} {dot} {line} {dot} {line} {line}",
    # "/": f"{line} {dot} {dot} {line} {dot}",
    "(": f"{line} {dot} {line} {line} {dot}",
    ")": f"{line} {dot} {line} {line} {dot} {line}",
    "&": f"{dot} {line} {dot} {dot} {dot}",
    ":": f"{line} {line} {line} {dot} {dot} {dot}",
    ";": f"{line} {dot} {line} {dot} {line} {dot}",
    "=": f"{line} {dot} {dot} {dot} {line}",
    "-": f"{line} {dot} {dot} {dot} {dot} {line}",
    "_": f"{dot} {dot} {line} {line} {dot} {line}",
    '"': f"{dot} {line} {dot} {dot} {line} {dot}",
    "$": f"{dot} {dot} {dot} {line} {dot} {dot} {line}",
    "@": f"{dot} {line} {line} {dot} {line} {dot}",
    "+": f"{dot} {line} {dot} {line} {dot}"
}
morse_decoding = {value: key for key, value in morse_encoding.items()}


def encode(word: str) -> str:
    list_to_encode = list(word.lower())
    list_encoded = []
    for letter in list_to_encode:
        if letter in morse_encoding:
            list_encoded.append(morse_encoding[letter])
    return "   ".join(list_encoded)


def decode(morse: str) -> str:
    morse_list = morse.split("       ")
    list_decoded = []
    for element in morse_list:
        element2 = element.split("   ")
        for letter in element2:
            if letter in morse_decoding:
                list_decoded.append(morse_decoding[letter])
        list_decoded.append(" ")
    return "".join(list_decoded)


def convert(morse: str) -> str:
    replace = []
    for letter in morse:
        if letter == ".":
            replace.append(f"{dot} ")
        elif letter == "-":
            replace.append(f"{line} ")
        elif letter == "_":
            replace.append(f"{line} ")
        elif letter == " ":
            replace.append("  ")
        elif letter == "/" or letter == "|":
            replace.append("      ")
    return ''.join(replace)


commands = ["menu", "symbols", "about", "encode", "decode", "quit", "close", "convert"]
while not close:
    if option == "menu":
        os.system("cls")
        option = input("Welcome to Morsee.\nIf you want to encode text in Morse_code, type: 'Encode'.\n"
                       "If you want to decode text in Morse_code, type: 'Decode'.\n\n"
                       "Morse-code to 'Decode' should be in program style.\n"
                       "Otherwise, first read 'About' and try using 'Convert' to adjust it.\n"
                       "Additional commands: 'About', 'Symbols', 'Convert', 'Close/Quit'.\n").lower()
    elif option == "commands":
        os.system("cls")
        option = input(f"{', '.join(commands).title()}\nUse any of this 'commands':\n")
    elif option not in commands:
        os.system("cls")
        print("There's no such command.\nRedirecting to 'Menu'.")
        time.sleep(2)
        option = "menu"
    elif option == "symbols":
        os.system("cls")
        print("Supported symbols. According to ITU-R M.1677-1 standard.")
        for key, value in morse_encoding.items():
            print(key + ":" + value)
        option = input("\nIf you want to go back into 'menu', type: 'menu'\n")
    elif option == "about":
        os.system("cls")
        print("This is a program which encodes and decodes text by ITU-R M.1677-1 standard.\n"
              "If you want to 'Decode' code which was created outside of this program,\n"
              "you need to 'convert' it and use standard keyboard keys for:\n'DOT' is '.' and for 'Line' '-' or '_',"
              " no separation for letters in words.\n"
              "Word separator can be used as '/' or '|'\n"
              "Available formats to convert:\n"
              "1) .__ .... . _./.. _./_ .... ./_._. ___ .._ ._. ... ./___ .._./.... .._ __ ._ _./\n"
              "2) .-- .... . -.|.. -.|- .... .|-.-. --- ..- .-. ... .|--- ..-.|.... ..- -- .- -.|\n")
        option = input("\nIf you want to go back into 'menu', type: 'menu'\n")
    elif option == "encode":
        os.system("cls")
        print("Write/place text to encode in Morse-code:")
        encode_input = []
        while True:
            input_line = input()
            if input_line:
                encode_input.append(input_line)
            else:
                break
        word_to_encode = ''.join(encode_input)
        os.system("cls")
        encode_result = encode(word_to_encode)
        pyperclip.copy(encode_result)
        option = input(f"Morse code of the text:\n {encode_result}\n"
                       f"Result is saved in clipboard, use Ctrl+v to paste.\n"
                       f"If you want to encode again, type: 'encode'.\n"
                       "For menu, type: 'menu'\n")
    elif option == "decode":
        os.system("cls")
        print("Write/place text to decode in Morse:")
        decode_input = []
        while True:
            input_line = input()
            if input_line:
                decode_input.append(input_line)
            else:
                break
        word_to_decode = ''.join(decode_input)
        os.system("cls")
        decode_result = decode(word_to_decode)
        pyperclip.copy(decode_result)
        option = input(f"Text variant of the code:\n{decode_result}\n\n"
                       f"Result is saved in clipboard, use Ctrl+V to paste.\n"
                       f"If you want to decode again, type: 'decode'\n"
                       "For menu, type: 'menu'\n")
    elif option == "convert":
        os.system("cls")
        print("Format in which going to be converted:\n"
              "ITU-R M.1677-1 standard, which stands for this rules:\n"
              "1) Words should be separated by 7 spaces.\n"
              "2) Letters in words should be separated by 3 spaces.\n"
              "3) 'Dots' and 'Lines' should be separated by 1 space from each other.\n"
              "Use command: 'about' in 'menu'. To see which formats is available to convert.\n"
              "Morse-code to convert:")
        convert_contents = []
        while True:
            input_line = input()
            if input_line:
                convert_contents.append(input_line)
            else:
                break
        string_to_convert = ''.join(convert_contents)
        os.system("cls")
        convert_result = convert(string_to_convert)
        pyperclip.copy(convert_result)
        option = input(f"Converted variant to use:\n{convert_result}\n\n"
                       f"Result is saved in clipboard, use Ctrl+V to paste.\n"
                       f"If you want to convert again, type: 'convert'\n"
                       f"For menu, type: 'menu'\n")
    elif option == "close" or "quit":
        os.system("cls")
        print("Morsee closed")
        close = True
