
def say():
    return "It works!";

def addButton():
    from PythonQt.QtWidgets import QPushButton

    button = QPushButton("bla")
    grid.addWidget(button, 1, 0, 1, 1)
