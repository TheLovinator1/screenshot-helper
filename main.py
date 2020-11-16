import argparse
import datetime
import os
import random
import shutil
import subprocess
import webbrowser
from settings import Settings


def upload_file(source_file: str):
    """
    Copy file to location
    """

    file_name: str = os.path.basename(source_file)  # Remove path
    file_destination: str = f"{Settings.file_folder}{file_name}"
    file_url: str = f"{Settings.file_url}{now:%Y}/{now:%m}/{file_name}"

    # Check if path is working.
    try:
        create_folder(path=Settings.file_folder)
    except Exception as e:
        send_desktop_notification(f"Failed to create folder.\n{e}")

    shutil.copy(source_file, file_destination)
    print(f"{file_name} - {source_file} copied to {file_destination}")

    return file_url


def append_url_to_history_file(url: str):
    """
    Append url to file.
    """
    # TODO: Add file type
    append_time = datetime.datetime.now()
    with open(Settings.history_file, "a") as f:
        f.write(f"{append_time} - {url}\n")
        print(f"Appended to file: {append_time} - {url}")


def send_desktop_notification(message: str):
    """
    Send desktop notification. Needs libnotify.
    """
    # TODO: Add support for different levels
    # TODO: Add image in notification
    subprocess.Popen(["notify-send", message])
    print(f"Message sent: {message}")


def random_char(amount: int):
    """
    Generate string from x amount of letters and digits.
    """
    letters_and_digits = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    )
    return "".join(random.choice(letters_and_digits) for x in range(amount))


def create_folder(path: str):
    """
    Check if folder exists. If not, create one.
    """
    try:
        if not os.path.exists(path):
            print(f"Couldn't find path ({path}). Creating!")
            os.makedirs(path)
    except Exception as e:
        print(f"Failed to create folder:\n{e}")
        return 0


def add_to_clipboard(clipboard_string: str):
    """
    Add url to clipboard with xsel.
    """
    subprocess.Popen(
        ("xsel", "--input", "--clipboard"),
        stdin=subprocess.PIPE,
        universal_newlines=True,
    ).communicate(clipboard_string)


def take_screenshot():
    """
    Screenshot and move to folder.
    """
    option = ""
    if args.select:
        option = "--select"
    if args.focused:
        # FIXME: This does not work. Captures whole desktop instead of
        # active window. Could be i3 that fucks.

        output = subprocess.run(
            "xdotool getactivewindow", capture_output=True, shell=True
        )

        # Convert bytes to string
        clean_output = output.stdout.decode()

        # Remove new line
        clean_output = clean_output.strip()

        send_desktop_notification(f"xdotool getactivewindow.\n{clean_output}")
        option = f"-i {clean_output}"

    image_filename: str = random_char(amount=10)
    image_path: str = f"{Settings.image_folder}{now:%Y}/{now:%m}"
    image_url: str = f"{Settings.image_url}{now:%Y}/{now:%m}/{image_filename}.{Settings.file_extension}"

    # Check if path is working.
    try:
        create_folder(path=image_path)
    except Exception as e:
        send_desktop_notification(f"Failed to create folder.\n{e}")

    # Take the actual screenshot
    try:
        command_list = [
            "maim",
            f"{image_path}/{image_filename}.png",
            option,
            "--quality 10",
            "--bordersize=4",
            "--color=255,0,0",
            "--hidecursor",
        ]
        subprocess.run(command_list)

    except Exception as e:
        send_desktop_notification(f"Failed to create folder.\n{e}")

    return image_url


def main():
    # TODO: Only add to clipboard and open url if there actually is a image
    url = ""
    if args.focused or args.select:
        url = take_screenshot()
    if args.upload:
        url = upload_file(source_file=str(args.upload))

    send_desktop_notification(f"URL: {url}")
    append_url_to_history_file(url=url)
    add_to_clipboard(clipboard_string=url)
    webbrowser.open_new_tab(url=url)


if __name__ == "__main__":
    now = datetime.datetime.now()
    parser = argparse.ArgumentParser(description="ShareX but cooler.")

    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument(
        "-s",
        "--select",
        help="interactively choose a window or rectangle with the mouse",
        required=False,
        action="store_true",
    )
    g.add_argument(
        "-f",
        "--focused",
        help="use the currently focused window",
        required=False,
        action="store_true",
    )
    g.add_argument(
        "-u",
        "--upload",
        help="upload a file. File will be replaced if already exist",
        required=False,
        action="store",
        metavar="FILEPATH",
    )
    args = parser.parse_args()

    main()
