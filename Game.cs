using System;
using System.ComponentModel;
using System.IO;
using Terminal.Gui;
using GuiAttribute = Terminal.Gui.Attribute;

sealed class GameView : Toplevel, ISupportInitialize {
  int count;
  KeyPlayer player;
  World world;

  public GameView() {
    player = new KeyPlayer();
    world = new World(player);
  }

  void ISupportInitialize.BeginInit() {
    const int fps = 60;
    // Don't need to remove the returned token 
    Application.MainLoop.AddTimeout(TimeSpan.FromSeconds(1) / fps, Update);
  }

  bool Update(MainLoop loop) {
    ++count;

    world.Update();
    Draw();

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

  void Draw() {
    RemoveAll();
    Add(Draw(world.Ship));
  }

  View Draw(Ship ship) => new Label(
      ship.X,
      ship.Y,
      "=^=") {
        Height = 1,
        ColorScheme = new ColorScheme { Normal = GuiAttribute.Make(Color.Green, Color.Black) },
      };
}

sealed class World {
  public Ship Ship { get; private set; }

  public World(IPlayer player) {
    Ship = new Ship(player);
  }

  public void Update() {
    Ship.Update();
  }
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
  public int X { get; set; }
  public int Y { get; set; }

  public void Update() {
    if (this.player.Left) --X;
    if (this.player.Right) ++X;
    if (this.player.Up) --Y;
    if (this.player.Down) ++Y;
  }
}
