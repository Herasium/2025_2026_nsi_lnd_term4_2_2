from modules.ui import Window, EditorView

def start():

    windows = Window()
    view = EditorView()

    windows.display(view)
    windows.run()

if __name__ == "__main__":
    start()