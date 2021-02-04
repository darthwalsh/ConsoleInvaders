using System;
using Terminal.Gui;

class Program {
  static int Main() {
    try {
      Application.Run<GameView>();
      return 0;
    } catch (Exception e) {
      Application.Driver.End();

      Console.ForegroundColor = ConsoleColor.Red;
      Console.Error.WriteLine(e);
      Console.Error.Flush();
      return 1;
    } finally {
      Application.Driver.End();
    }
  }
}
