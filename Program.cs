using Terminal.Gui;

class Program {
  static void Main() {
    try {
      Application.Run<Game>();
    } finally {
      Application.Driver.End();
    }
  }
}
