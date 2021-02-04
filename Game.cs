using System;
using System.ComponentModel;
using Terminal.Gui;

class Game : Toplevel, ISupportInitialize {
  int count;
  Window win;

  void ISupportInitialize.BeginInit() {
    win = new Window("Hello") {
      X = 0,
      Y = 1,
      Width = Dim.Fill(),
      Height = Dim.Fill() - 1
    };

    this.Add(win);

    var fps = TimeSpan.FromSeconds(1) / 60;
    // Don't need to remove the returned token 
    Application.MainLoop.AddTimeout(fps, Update);
  }

  bool Update(MainLoop loop) {
    ++count;
    win.Title = "Time" + count;

    bool keepGoing = count < 300;

    if (!keepGoing) {
      Application.RequestStop();
    }
    return keepGoing;
  }
}
