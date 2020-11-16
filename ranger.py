from ranger.api.commands import Command
import os
import subprocess
from ranger.container.file import File


class screenshothelper(Command):
    """
    :screenshothelper <file>

    Upload files with screenshot-helper
    """

    def execute(self):
        arg = self.rest(1)
        if arg:
            if not os.path.isfile(arg):
                self.fm.notify("{} is not a file.".format(arg))
                return
            file = File(arg)
        else:
            file = self.fm.thisfile
            if not file.is_file:
                self.fm.notify("{} is not a file.".format(file.relative_path))
                return
        relative_path = file.relative_path
        self.fm.notify(f"File: {relative_path}")
        upload_command = [
            "python",
            "/home/lovinator/Repository/screenshot-helper/main.py",
            "--upload",
            arg,
        ]
        subprocess.check_call(upload_command)
        self.fm.notify("Uploaded!")

    def tab(self):
        return self._tab_directory_content()