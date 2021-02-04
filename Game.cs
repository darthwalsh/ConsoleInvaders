using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using Terminal.Gui;

sealed class GameView : Toplevel, ISupportInitialize, IDrawGame {
  int count;
  KeyPlayer player;
  World world;

  public GameView() {
    player = new KeyPlayer();
    world = new World(player);
  }
  Dictionary<object, Label> labels = new Dictionary<object, Label>();

  void ISupportInitialize.BeginInit() {
    var fps = TimeSpan.FromSeconds(1) / 60;
    // Don't need to remove the returned token 
    Application.MainLoop.AddTimeout(fps, Update);


    // var label = new Label("Hello World") {
    //   X = Pos.Center(),
    //   Y = Pos.Center(),
    //   Height = 1,
    // };
    // Add(label);

    var label = GetLabel(new object());
    label.Text = "=^=";
    label.X = Pos.Center();
    label.Y = Pos.Center();
    label.Height = 1;

    Add(label);

  }

  bool Update(MainLoop loop) {
    ++count;

    var l = Subviews.Single();
    l.Text = "Count" + count;

    // world.Update();
    // world.Draw(this);

    bool keepGoing = true;
    return keepGoing;
  }

  public override bool OnKeyDown(KeyEvent keyEvent) {
    switch (keyEvent.Key) {
    case Key.CursorUp: player.Up = true; return true;
    case Key.CursorDown: player.Down = true; return true;
    case Key.CursorLeft: player.Left = true; return true;
    case Key.CursorRight: player.Right = true; return true;
    case Key.Space: player.Fire = true; return true;
    }
    return false;
  }

  public override bool OnKeyUp(KeyEvent keyEvent) {
    switch (keyEvent.Key) {
    case Key.CursorUp: player.Up = false; return true;
    case Key.CursorDown: player.Down = false; return true;
    case Key.CursorLeft: player.Left = false; return true;
    case Key.CursorRight: player.Right = false; return true;
    case Key.Space: player.Fire = false; return true;
    }
    return false;
  }

  public override bool ProcessKey(KeyEvent keyEvent) {
    switch (keyEvent.Key) {
    case Key.ControlC:
    case Key.Esc:
      Application.RequestStop();
      return true;
    }
    return false;
  }

  class KeyPlayer : IPlayer {
    public bool Up { get; set; }
    public bool Down { get; set; }
    public bool Left { get; set; }
    public bool Right { get; set; }
    public bool Fire { get; set; }
  }

  public void Draw(Ship ship) {
    var label = GetLabel(ship);
    label.Text = "=^=";
    label.X = ship.X;
    label.Y = ship.Y;
    label.Height = 1;
  }

  Label GetLabel(Object o) {
    if (labels.TryGetValue(o, out var label)) return label;
    label = new Label();
    labels[o] = label;
    Add(label);
    return label;
  }
}

sealed class World {
  Ship ship;

  public World(IPlayer player) {
    ship = new Ship(player);
  }

  public void Update() {

  }

  public void Draw(IDrawGame drawer) {
    drawer.Draw(ship);
  }
}

interface IDrawGame {
  void Draw(Ship ship);
} 

interface IPlayer {
  bool Up { get; }
  bool Down { get; }
  bool Left { get; }
  bool Right { get; }
  bool Fire { get; }
}

sealed class Ship {
  IPlayer player;
  public Ship(IPlayer player) {
    this.player = player;
  }
  public int X => 2;
  public int Y => 3;
}
