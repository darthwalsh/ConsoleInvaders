# Console Invaders

A text-mode space invaders game (suggested from [Austin Z. Henley's blog](https://web.eecs.utk.edu/~azh/blog/challengingprojects.html)).

## Install

Install by runing:

```shell
pip install consoleinvaders
```

Uses `pynput` and `windows-curses` dependencies.

## Run

To play the game use arrow keys to move, and hold Left Shift to shoot, run on a terminal:

```shell
consoleinvaders
```

The game is over if you destroy all aliens or an alien destroys you or reaches the bottom.

Press ESC or Ctrl+C to quit.

### Windows

The Windows Terminal doesn't seem to handle resizing while the game is running: microsoft/terminal#5094 

### MacOS

In order to [detect keyboard state](https://pynput.readthedocs.io/en/latest/limitations.html), your terminal needs [Input Monitoring](https://support.apple.com/guide/mac-help/control-access-to-input-monitoring-on-mac-mchl4cedafb6/mac) permission.

For some reason, when using iTerm2 the keyboard state doesn't work if iTerm2 is selected. Click to focus a different app and then play the game, or use a different terminal.


## Developing

```shell
git clone https://github.com/darthwalsh/ConsoleInvaders.git
cd ConsoleInvaders
python3 -m venv env   # Or on Windows, use python
. env/bin/activate    # Or on Windows, use Activate.ps1
pip install -r requirements.txt

# On Windows: pip install windows-curses
```

Run with:

```shell
python3 -c "import consoleinvaders.app; consoleinvaders.app.main()"
```

