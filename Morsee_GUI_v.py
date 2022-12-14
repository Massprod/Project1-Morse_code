from threading import Timer
import tkinter
from tkinter import *
from tkinter import messagebox
from playsound import playsound
import time
import datetime
import json
import os
import tkinter.scrolledtext as scrollbartext

# before OOP implementation (maybe ignore OOP in this one, we'll see)
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
    "/": f"{line} {dot} {dot} {line} {dot}",
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
global SOUND_ON, history_window


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
            replace.append("  ")
    return ''.join(replace)


def encode_button_command():
    if text_to_encode.get("1.0", "end-1c"):
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", END)
        text = text_to_encode.get("1.0", "end-1c")
        encoded_text = encode(text).strip()
        text_encoded.insert("1.0", encoded_text)
        append_history()
        text_encoded.config(state="disabled")
    else:
        messagebox.showinfo(title="Empty",
                            message="There's no Text to Encode.\nPlease fill it.",
                            icon="question",
                            )


def copy_button_command():
    copied_text = text_encoded.get("1.0", "end-1c").strip()
    if copied_text:
        main_window.clipboard_clear()
        main_window.clipboard_append(copied_text)


def clear_button_command():
    text_to_clear = text_encoded.get("1.0", END)
    if text_to_clear:
        text_to_encode.delete("1.0", END)
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", END)
        text_encoded.config(state="disabled")


def decode_button_command():
    if text_to_encode.get("1.0", "end-1c"):  # end-1c, deletes 1 character from end, needed to remove empty line.
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", END)
        text = text_to_encode.get("1.0", "end-1c")
        error = False
        allowed_symbols = [" ", "_", "."]  # tried to use if \letter != " " or letter != "."or letter != "_"/,
        # didn't work. But with checking IN_LIST, all good. hmm
        for letter in text:
            if letter not in allowed_symbols:
                messagebox.showinfo(title="Incorrect Symbols",
                                    message="There's incorrect symbols to Decode."
                                            "\nPlease use Morsee code or try to Convert.",
                                    icon="question",  # removing sound, icons: info, warning - cause warning sound.
                                    )
                error = True
                break
        if not error:
            decoded_text = decode(text)
            text_encoded.insert("1.0", decoded_text)
            append_history()
            text_encoded.config(state="disabled")
    else:
        messagebox.showinfo(title="Empty",
                            message="There's no Morse to Decode.\nPlease fill it.",
                            icon="question",  # removing sound, icons: info, warning - cause warning sound.
                            )


def change_to_convert_command():
    disable_main_window()
    convert_info_window = Toplevel(main_window)
    convert_info_window.title("Converting Info")
    main_x = main_window.winfo_rootx()
    main_y = main_window.winfo_rooty()
    convert_window_x = main_x + 250
    convert_window_y = main_y + 160
    convert_info_window.geometry(f"+{convert_window_x}+{convert_window_y}")
    convert_info_window.resizable(False, False)
    convert_info_window.config(
        bg="#F7F6F2",
    )
    convert_info_window_text = Text(convert_info_window,
                                    height=10,
                                    width=54,
                                    fg="#4B6587",
                                    bg="#F7F6F2",
                                    selectforeground="#4B6587",  # to hide selection, because didn't
                                    selectbackground="#F7F6F2",  # found how to disable it completely
                                    font=("Ariel", 12, "bold"),
                                    state="normal",
                                    relief=tkinter.RIDGE,
                                    )
    convert_info_window_text.insert(1.0,
                                    "  If you want to 'Decode' code which wasn't created in Morsee."
                                    "\n  You can try to 'convert' this code, according to this rules:"
                                    "\n   1.  'DOT' is '.' and 'Line' '-' or '_' "
                                    "\n   2.  No separation for letters in words."
                                    "\n   3.  Word separator can be used as '/' or '|'"
                                    "\n\n  Example of formats to convert:"
                                    "\n     .__ .... . _. / .. _. / _ .... . / "
                                    "_._. ___ .._ ._. ... . / ___ .._. / .... .._ __ ._ _. / "
                                    "\n\n     .-- .... . -. | .. -. | - .... . | "
                                    "-.-. --- ..- .-. ... . | --- ..-. | .... ..- -- .- -. | "
                                    )
    convert_info_window_text.grid(row=0,
                                  columnspan=3,
                                  column=0,
                                  )
    convert_info_window_text.bind("<Control-c>", lambda event: "break")  # disable copying
    convert_info_window_text.bind("<Control-x>", lambda event: "break")
    convert_info_window_text.config(state="disabled")
    convert_info_window_label = Label(convert_info_window,
                                      text="Would you like to try Converting?",
                                      fg="#4B6587",
                                      bg="#F7F6F2",
                                      font=("Ariel", 14, "bold")
                                      )
    convert_info_window_label.grid(row=1,
                                   column=0,
                                   )
    convert_info_window.protocol("WM_DELETE_WINDOW", lambda: (convert_info_window.destroy(), enable_main_window()))

    def convert_info_pressed_yes():
        convert_info_window.withdraw()
        enable_main_window()
        sound_play_button.grid_remove()
        encode_label.config(text="Code Morse to convert")
        encoded_label.config(text="Converted to Morsee")
        if encode_label.cget("text") == "Text to encode":
            encode_button.grid_remove()
            convert_button.grid()
        elif encode_label.cget("text") != "Text to encode":
            decode_button.grid_remove()
            convert_button.grid()
        change_type_button.config(text="CONVERTING",
                                  state="disabled",
                                  )
        change_to_convert_button.config(text="To Encode",
                                        command=change_type_button_command,
                                        )
        text_to_encode.delete("1.0", END)
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", END)
        text_encoded.config(state="disabled")

    convert_info_window_yes_button = Button(convert_info_window,
                                            width=5,
                                            text="YES",
                                            fg="#4B6587",
                                            activeforeground="#4B6587",
                                            bg="#E6E5A3",
                                            activebackground="#E6E5A3",
                                            font=("Ariel", 14, "bold"),
                                            relief=tkinter.FLAT,
                                            command=convert_info_pressed_yes,
                                            )
    convert_info_window_yes_button.grid(row=1,
                                        column=1,
                                        sticky="e",
                                        )

    def convert_info_pressed_no():
        convert_info_window.withdraw()
        enable_main_window()

    convert_info_window_no_button = Button(convert_info_window,
                                           width=5,
                                           text="NO",
                                           fg="#4B6587",
                                           activeforeground="#4B6587",
                                           bg="#F7A4A4",
                                           activebackground="#F7A4A4",
                                           font=("Ariel", 14, "bold"),
                                           relief=tkinter.FLAT,
                                           command=convert_info_pressed_no,
                                           )
    convert_info_window_no_button.grid(row=1,
                                       column=2,
                                       sticky="e",
                                       )


def convert_button_command():
    if text_to_encode.get("1.0", "end-1c"):
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", "end-1c")
        text = text_to_encode.get("1.0", "end-1c")
        if "/" in text or "|" in text:
            converted_text = convert(text)
            text_encoded.insert("1.0", converted_text)
            text_encoded.delete("end-2c", END)  # Prefer to leave to delete extra space from Highlighting with cursor.
            append_history()
            text_encoded.config(state="disabled")
        else:
            messagebox.showinfo(title="Error",
                                message="Dont try to Convert single word or symbol."
                                        "\nThere's no '/' or '|' separators"
                                        "\nPress 'To Convert' button to check Rules for converting.",
                                icon="question",
                                )
    else:
        messagebox.showinfo(title="Empty",
                            message="There's no Morse to Convert.\nPlease fill it.",
                            icon="question",
                            )


def change_type_button_command():
    if encode_label.cget("text") == "Text to encode":
        encode_label.config(text="Code Morse to decode")
        encoded_label.config(text="Decoded text")
        sound_play_button.grid_remove()
        encode_button.grid_remove()
        decode_button.grid()
        change_type_button.config(text="DECODING")
        text_to_encode.delete("1.0", END)
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", END)
        text_encoded.config(state="disabled")
    elif encode_label.cget("text") != "Text to encode":
        change_to_convert_button.config(text="To Convert",
                                        command=change_to_convert_command,
                                        )
        encode_label.config(text="Text to encode")
        encoded_label.config(text="Encoded text")
        sound_play_button.grid()
        convert_button.grid_remove()
        decode_button.grid_remove()
        encode_button.grid()
        change_type_button.config(text="ENCODING",
                                  state="normal",
                                  )
        text_to_encode.delete("1.0", END)
        text_encoded.config(state="normal")
        text_encoded.delete("1.0", END)
        text_encoded.config(state="disabled")


def about_button_command():
    messagebox.showinfo(title="About",
                        message=" Morsee Encodes and Decodes texts according to"
                                " \nITU-R M.1677-1 standard."
                                " If you want to Decode Morse code, which wasn't created in Morsee."
                                " You will need to make sure it matches standard and available symbols."
                                " \nSymbols not included in standard will be ignored!\n\n"
                                " In Morsee length of 'dash' is equal to 'dot'.\n"
                                " The space between:\n -the signals forming the same letters is equal to one dot.\n"
                                " -two letters is equal to three dots.\n"
                                " -two words is equal to seven dots.\n",
                        icon="question",
                        )


def stop_sound():
    global SOUND_ON
    if sound_play_button.cget("text") != " Play":
        sound_play_button.config(text=" Play",
                                 image=sound_play_icon,
                                 state="normal",
                                 command=sound_play_clicked,
                                 bg="#C8C6C6",
                                 activebackground="#C8C6C6",
                                 )
        enable_main_window()
        SOUND_ON = False


# maybe change sound if I find better or cut it from other source, good for now
def sound_play_button_command(morse):
    global SOUND_ON
    if morse:
        SOUND_ON = True
        morse = list(morse)
        dumb_solution = 0
        # dumb_solution - bad solution for breaking loop and enabling buttons,
        # needed to be changed when I learn how to break playsound or use pygame.
        disable_main_window()
        text_to_encode.config(state="normal")
        sound_play_button.config(text=" Cancel",
                                 image=sound_cancel_icon,
                                 state="normal",
                                 command=stop_sound,
                                 bg="#F7A4A4",
                                 activebackground="#F7A4A4",
                                 )
        while dumb_solution < len(morse):
            for element in morse:
                if element == " " and SOUND_ON:
                    dumb_solution += 1
                    time.sleep(0.16)
                elif element == "_" and SOUND_ON:
                    dumb_solution += 1
                    line_path = r"C:\\Users\Pampam\PycharmProjects\StartProject1\media\line_sound_068s.wav"
                    playsound(sound=line_path)
                    # path string to sound need's to be Raw=r
                elif element == "." and SOUND_ON:
                    dumb_solution += 1
                    dot_path = r"C:\\Users\Pampam\PycharmProjects\StartProject1\media\dot_sound_024s.wav"
                    playsound(sound=dot_path)
                else:
                    return
                    # If I need to stop thread (as I understood), just need to get
                    # RETURN(something) from called function
        else:
            sound_play_button.config(text=" Play",
                                     image=sound_play_icon,
                                     state="normal",
                                     command=sound_play_clicked,
                                     bg="#C8C6C6",
                                     activebackground="#C8C6C6",
                                     )
            enable_main_window()
    else:
        pass


def sound_play_clicked():
    morse = text_encoded.get("1.0", "end-1c")
    thread2 = Timer(0.1, sound_play_button_command, args=(morse,))  # prefer to buffer some time
    # thread2 = threading.Thread(target=sound_play_button_command, args=(morse,))
    # [morse] basically to get all characters in ONE_STRING,
    # otherwise text will be changed to # of single strings and put into a tuple one by one
    thread2.start()


# right_click drop menu
def right_click(event):  # event_bind = Button-3 #
    try:
        x, y = main_window.winfo_pointerxy()  # pointer coordinates
        widget = main_window.winfo_containing(x, y)  # widget with mouse_pointer over it
        # used "normal", but there's 3 states, so it's better to exclude
        if widget.winfo_class() == "Text" and widget["state"] != "disabled":
            widget.focus_set()
            menu.tk_popup(event.x_root, event.y_root)
        elif widget.winfo_class() == "Text":  # disabling changes for inactive text_field, only copy_allowed
            menu.entryconfig("Cut", state="disabled")
            menu.entryconfig("Delete", state="disabled")
            menu.entryconfig("Paste", state="disabled")
            menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()
        menu.entryconfig("Cut", state="normal")
        menu.entryconfig("Delete", state="normal")
        menu.entryconfig("Paste", state="active")
    # wanted to hide this options, not found any options for now.
    # make 2 menus and switch between them, but there's only copy from second field
    # it's better, to disable or just make copy_button for this.


# copy command
def right_click_copy():
    try:
        selected_text = main_window.selection_get()
        main_window.clipboard_clear()
        main_window.clipboard_append(selected_text)
    except TclError:
        pass


# cut command
def right_click_cut():
    try:
        widget = main_window.focus_get()
        selected_text = main_window.selection_get()
        main_window.clipboard_clear()
        main_window.clipboard_append(selected_text)
        widget.delete("sel.first", "sel.last")
    except TclError:
        pass


# paste command
def right_click_paste():
    try:
        copied_text = main_window.clipboard_get()
        widget = main_window.focus_get()
        position = widget.index(INSERT)  # INSERT position in text
        if widget.winfo_class() == "Text":
            if widget["state"] != "disabled":
                widget.insert(position, copied_text)
                widget.delete("sel.first", "sel.last")
    except TclError:
        pass


# delete command
def right_click_delete():
    try:
        widget = main_window.focus_get()
        widget.delete("sel.first", "sel.last")
    except TclError:
        pass


# disable main_window buttons/text_fields
def disable_main_window():
    for widget in main_window.winfo_children():
        try:
            widget["state"] = "disabled"
        except TclError:
            pass


def enable_main_window():
    for widget in main_window.winfo_children():
        try:
            widget["state"] = "normal"
        except TclError:
            pass


# history
def append_history():
    timezone = datetime.datetime.now(datetime.timezone.utc).astimezone()
    system_time = timezone.strftime("%Y-%m-%d %H:%M:%S")
    input_text = text_to_encode.get("1.0", "end-1c")
    output_text = text_encoded.get("1.0", "end-1c")
    new_record = {
        system_time: {
            "Input": input_text,
            "Result": output_text,
        }
    }
    if output_text:
        try:
            with open("history.json", "r") as history:
                history_data = json.load(history)
                for key in history_data.copy():
                    if history_data[key]["Input"] == new_record[system_time]["Input"]:
                        history_data.pop(key)
                        history_data.update(new_record)
                        break
                else:
                    history_data.update(new_record)
                # add for loop to check if there was same message Encoded before and change time for it. Better than
                # duplicating it. Wanted to remove duplicates completely, but after checking GChrome history, I prefer
                # to change creation time and make all record's unique.
        except FileNotFoundError:
            with open("history.json", "w") as history:
                json.dump(new_record, history, indent=2)
        except ValueError:
            with open("history.json", "w") as history:
                json.dump(new_record, history, indent=2)
        else:
            with open("history.json", "w") as history:
                json.dump(history_data, history, indent=2)
    else:
        pass


def clear_history_button_command():
    global history_window  # try to use focus after sleep, just wanted to close it with clear
    if os.path.exists("history.json"):
        os.remove("history.json")
        history_window.destroy()
        enable_main_window()
    else:
        pass


def history_button_command():
    global history_window
    try:
        with open("history.json", "r") as history:
            history_data = json.load(history)
            disable_main_window()
            history_window = Toplevel(main_window)
            history_window.title("History")
            history_window.configure(bg="black")
            main_x = history_window.winfo_rootx()
            main_y = history_window.winfo_rooty()
            history_window_x = main_x + 250
            history_window_y = main_y + 160
            history_window.geometry(f"+{history_window_x}+{history_window_y}")
            history_window.geometry("770x700")
            history_window.resizable(False, False)

            def onFrameConfigure(canvas):
                """Reset the scroll region to encompass the inner frame"""
                canvas.configure(scrollregion=canvas.bbox("all"))
                # pathetic stealing, need to learn more about scrollbar attachments and do it myself
                # right now it's not a total ripoff, but I need to do more.

            def on_mousewheel(event):
                try:
                    history_window_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                except TclError:
                    pass

            history_window_canvas = tkinter.Canvas(history_window, borderwidth=0, background="#F0E5CF")
            history_window_frame = tkinter.Frame(history_window_canvas, bg="#F0E5CF", border=0, )
            history_window_scrollbar = tkinter.Scrollbar(history_window, orient="vertical",
                                                         command=history_window_canvas.yview)
            history_window_canvas.configure(yscrollcommand=history_window_scrollbar.set,
                                            height=700,
                                            width=770,
                                            border=0, )
            history_window_scrollbar.grid(row=0, column=0, sticky="nse")
            history_window_canvas.grid(row=0, column=0, sticky="nsew")
            history_window_canvas.create_window((0, 0), window=history_window_frame, anchor="nw")
            history_window_canvas.bind_all("<MouseWheel>", on_mousewheel)
            history_window_frame.bind("<Configure>",
                                      lambda event, canvas=history_window_canvas: onFrameConfigure(history_window_canvas))
            history_window.protocol("WM_DELETE_WINDOW",
                                    lambda: (history_window.destroy(), enable_main_window()))

            time_label_row = 1
            input_label_column = 0
            input_label_row = 0
            input_text_row = 1
            result_label_row = 0
            result_text_row = 1
            for key in history_data:
                # time of record
                time_label = Text(history_window_frame,
                                  height=4,
                                  width=10,
                                  fg="#4B6587",
                                  bg="#F0E5CF",
                                  selectforeground="#4B6587",
                                  selectbackground="#F7F6F2",
                                  font=("Ariel", 14, "bold"),
                                  state="normal",
                                  relief=tkinter.FLAT,
                                  )
                time_label.insert("1.0", f"\n{key}")
                time_label.configure(state="disabled")
                time_label.grid(
                    column=1,
                    row=time_label_row,
                )
                time_label_row += 4
                # input of record
                input_label = Label(history_window_frame,
                                    text="Input",
                                    font=("Ariel", 15, "bold"),
                                    anchor="n",
                                    bg="#F0E5CF",
                                    )
                input_label.grid(
                    column=input_label_column,
                    row=input_label_row,
                    sticky="s",
                    pady=(10, 0)
                )
                input_label_row += 4
                # input record
                input_text = scrollbartext.ScrolledText(history_window_frame,
                                                        height=4,
                                                        width=25,
                                                        fg="#4B6587",
                                                        bg="#C8C6C6",
                                                        font=("Ariel", 14, "bold"),
                                                        state="normal",
                                                        relief=tkinter.SUNKEN,
                                                        wrap="word",

                                                        )
                input_text.insert("1.0", history_data[key]["Input"])
                input_text.configure(state="disabled")
                input_text.grid(row=input_text_row,
                                column=0,
                                padx=15,
                                )
                input_text_row += 4
                # result label
                result_label = Label(history_window_frame,
                                     text="Result",
                                     font=("Ariel", 15, "bold"),
                                     bg="#F0E5CF",
                                     )
                result_label.grid(
                    column=2,
                    row=result_label_row,
                    sticky="s",
                    pady=(10, 0)
                )
                result_label_row += 4
                # result record
                result_text = scrollbartext.ScrolledText(history_window_frame,
                                                         height=4,
                                                         width=25,
                                                         fg="#4B6587",
                                                         bg="#C8C6C6",
                                                         font=("Ariel", 14, "bold"),
                                                         state="normal",
                                                         relief=tkinter.FLAT,
                                                         wrap="word",
                                                         )
                result_text.insert("1.0", history_data[key]["Result"])
                result_text.configure(state="disabled")
                result_text.grid(row=result_text_row,
                                 column=2,
                                 padx=(0, 15),
                                 )
                result_text_row += 4
            clear_history_button = Button(history_window_frame,
                                          width=15,
                                          text="Clear history",
                                          fg="#4B6587",
                                          bg="#F7F6F2",
                                          font=("Ariel", 14, "bold"),
                                          state="normal",
                                          relief=tkinter.FLAT,
                                          command=clear_history_button_command,
                                          )
            clear_history_button.grid(row=(result_text_row + 1),
                                      columnspan=3,
                                      sticky="s",
                                      pady=(40, 20)
                                      )
    except FileNotFoundError:
        messagebox.showinfo(title="Empty",
                            message="There's no History yet.\nTry to use Morsee first.",
                            icon="question",
                            )


# Gui setup
main_window = Tk()
# right click menu
menu = Menu(main_window, tearoff=0)
menu.add_command(label="Copy", command=right_click_copy, )
menu.add_command(label="Paste", command=right_click_paste)
menu.add_separator()
menu.add_command(label="Cut", command=right_click_cut)
menu.add_command(label="Delete", command=right_click_delete)
menu.config(
    bg="#FFF8EA",
    font=("Ariel", 10, "bold"),
    fg="#4B6587"
)
main_window.bind_all("<Button-3>", right_click)

# icon and window setup
icon = tkinter.PhotoImage(file='media/icons/morsee_icon.png')
main_window.iconphoto(True, icon)
main_window.title("Morsee")
main_window.config(padx=50,
                   pady=50,
                   bg="#F0E5CF",
                   )
# Change after all buttons done.
main_window.resizable(False, False)

# input/output frames
encode_label = Label()
encode_label.config(
    text="Text to encode",
    fg="#4B6587",
    font=("Ariel", 16, "bold"),
    anchor="w",
    bg="#F0E5CF",
)
encode_label.grid(
    column=1,
    row=0,
    sticky="w",
    pady=10,
)
text_to_encode = Text()
text_to_encode.config(
    width=75,
    height=10,
    font=("Ariel", 14, "bold"),
    bg="#C8C6C6",
    border=2,
    fg="#4B6587",
    relief=tkinter.FLAT,
    selectforeground="#4B6587",
    selectbackground="#F7F6F2",
    wrap="word",
    undo=True,
)
text_to_encode.grid(
    column=1,
    row=1,
)

encoded_label = Label()
encoded_label.config(
    text="Encoded text",
    fg="#4B6587",
    font=("Ariel", 16, "bold"),
    anchor="w",
    bg="#F0E5CF",
)
encoded_label.grid(
    column=1,
    row=2,
    sticky="w",
    pady=10,
)

text_encoded = Text()
text_encoded.config(
    width=75,
    height=10,
    font=("Ariel", 14, "bold"),
    bg="#C8C6C6",
    border=2,
    fg="#4B6587",
    state="disabled",
    relief=tkinter.FLAT,
    selectforeground="#4B6587",
    selectbackground="#F7F6F2",
)
text_encoded.grid(
    column=1,
    row=3,
)

# encode button #
encode_button = Button()
encode_button.config(
    width=15,
    text="Encode",
    fg="#4B6587",
    font=("Ariel", 15, "bold"),
    command=encode_button_command,
    relief=tkinter.FLAT,
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    activeforeground="#4B6587",
)
encode_button.grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="e",
    pady=5,
)

# copy button #
copy_button = Button()
copy_button.config(
    width=15,
    text="Copy",
    fg="#4B6587",
    activeforeground="#4B6587",
    font=("Ariel", 15, "bold"),
    relief=tkinter.FLAT,
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=copy_button_command,
)
copy_button.grid(
    row=4,
    column=1,
    sticky="e",
    pady=5,
)

# clear button #
clear_button = Button()
clear_button.config(
    width=12,
    text="Clear",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=clear_button_command,
    relief=tkinter.FLAT,
)
clear_button.grid(
    row=4,
    column=0,
    columnspan=2,
    sticky="w",
    pady=5,
)

# change type button #
change_type_button = Button()
change_type_button.config(
    width=12,
    text="ENCODING",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=change_type_button_command,
    relief=tkinter.FLAT,
)
change_type_button.grid(
    row=0,
    column=1,
    sticky="n",
    pady=5,
)

# change to convert button#
change_to_convert_button = Button()
change_to_convert_button.config(
    width=12,
    text="To Convert",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=change_to_convert_command,
    relief=tkinter.FLAT,
)
change_to_convert_button.grid(
    row=0,
    column=1,
    sticky="e",
    pady=5,
)
# decode button #
decode_button = Button()
decode_button.config(
    width=15,
    text="Decode",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=decode_button_command,
    relief=tkinter.FLAT,
)
decode_button.grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="e",
    pady=5,
)
decode_button.grid_remove()

# convert button #
convert_button = Button()
convert_button.config(
    width=15,
    text="Convert",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=convert_button_command,
    relief=tkinter.FLAT,
)
convert_button.grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="e",
    pady=5,
)
convert_button.grid_remove()

# about button #
about_button = Button()
about_button.config(
    width=10,
    text="About",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=about_button_command,
    relief=tkinter.FLAT,
)
about_button.grid(
    row=4,
    column=0,
    columnspan=2,
    sticky="n",
    pady=5,
)

# history button #
history_button = Button()
history_button.config(
    width=10,
    text="History",
    font=("Ariel", 15, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#F7F6F2",
    activebackground="#F7F6F2",
    command=history_button_command,
    relief=tkinter.FLAT,
)
history_button.grid(
    row=2,
    column=0,
    columnspan=2,
    sticky="n",
    pady=5,
)
# sound_play button #
sound_play_button = Button()
sound_play_icon = tkinter.PhotoImage(file="media/icons/play_icon_20px.png")
sound_cancel_icon = tkinter.PhotoImage(file="media/icons/cancel_icon_20px.png")
sound_play_button.config(
    height=20,
    width=75,
    image=sound_play_icon,
    text=" PLAY",
    compound=LEFT,
    font=("Ariel", 10, "bold"),
    fg="#4B6587",
    activeforeground="#4B6587",
    bg="#C8C6C6",
    activebackground="#C8C6C6",
    command=sound_play_clicked,
    relief=tkinter.FLAT,
)
sound_play_button.grid(
    row=3,
    column=1,
    columnspan=1,
    sticky="se",
)

main_window.mainloop()
