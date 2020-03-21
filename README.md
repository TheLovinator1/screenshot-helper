# screenshot-helper
Screenshot helper application. 


## Getting Started
You will need [Maim](https://github.com/naelstrof/maim), [XSel](http://www.vergenet.net/~conrad/software/xsel/), [libnotify](https://gitlab.gnome.org/GNOME/libnotify) and [Python](https://www.python.org/) to run this program.


## Usage
```
main.py [-h] (-s | -f | -u FILEPATH)
Arguments:
  -h, --help            show this help message and exit
  -s, --select          interactively choose a window or rectangle with the mouse
  -f, --focused         use the currently focused window
  -u FILEPATH, --upload FILEPATH
                        upload a file. File will be replaced if already exist

```


## Built With
* [Maim](https://github.com/naelstrof/maim) - The screen capture application this program built on top of
* [XSel](http://www.vergenet.net/~conrad/software/xsel/) - Clipboard management
* [Python](https://www.python.org/) - The language used to create this program
* [libnotify](https://gitlab.gnome.org/GNOME/libnotify) - Sends notifications to our notification daemon


## Authors
* **Joakim Hellsén** - *Initial work* - [TheLovinator1](https://github.com/TheLovinator1)
See also the list of [contributors](https://github.com/TheLovinator1/scrot-helper/contributors) who participated in this project.


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
