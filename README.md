# Console Invaders

Goal: Implement a text-mode space invaders game based on https://web.eecs.utk.edu/~azh/blog/challengingprojects.html

## Setup

```shell
git clone https://github.com/darthwalsh/ConsoleInvaders.git
cd ConsoleInvaders
python3 -m venv env   # Or on Windows, use python
. env/bin/activate    # Or on Windows, use Activate.ps1
pip install -r requirements.txt
```

## Play

Run `python3 ./app.py`.

Arrow keys to move, left shift to shoot, ESC to quit.

## Platform setup

### MacOS

In order to detect keyboard state, your terminal needs [Input Monitoring](https://support.apple.com/guide/mac-help/control-access-to-input-monitoring-on-mac-mchl4cedafb6/mac) permission.

For some reason, when using iTerm2 the keyboard state doesn't work if iTerm2 is selected. Click to focus a different app, or use a different terminal.
