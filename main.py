import datetime
import random
import os
import argparse
import subprocess
import webbrowser


def random_char(amount: int):
    """
    Generate string from x amount of letters and digits.
    """

    letters_and_digits = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    )

    return "".join(random.choice(letters_and_digits) for x in range(amount))


def create_folder():
    """
    Check if folder exists. If not, create one.
    """
    try:
        if not os.path.exists(path):
            print(f"Couldn't find path ({path}). Creating!")
            os.makedirs(path)
    except Exception as e:
        print(f"Something is fucked!\n{e}")
        return 0


def screenshot():
    # TODO: Check if name is already taken
    """
    Screenshot and move to folder.
    """

    # Check if path is working.
    create_folder()

    if args.select:
        option = "--select"
    if args.focused:
        option = "--focused"

    # Take the image
    subprocess.run(["scrot", option, "--freeze", f"{path}/{filename}.png"])

    print(f"URL: {url}")

    # Copy link to clipboard
    clipboard(variable=url)

    # Open link in browser
    webbrowser.open_new_tab(url=url)


def clipboard(variable):
    subprocess.Popen(
        ("xsel", "--input", "--clipboard"),
        stdin=subprocess.PIPE,
        universal_newlines=True,
    ).communicate(variable)


if __name__ == "__main__":

    now = datetime.datetime.now()
    # TODO: Different file types should go to different folders

    # 10 characters in filename
    filename = random_char(amount=10)
    # TODO: Remove trailing slash
    path = f"/mnt/wd_white/Nginx/www.lovinator/i/{now.year}/{now.month}"
    url = f"https://lovinator.xyz/i/{now.year}/{now.month}/{filename}.png"

    # Command-line options, arguments and sub-commands
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
        "-u",
        "--focused",
        help="use the currently focused window",
        required=False,
        action="store_true",
    )
    args = parser.parse_args()

    screenshot()
