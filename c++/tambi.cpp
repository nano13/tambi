
#include <QMainWindow>
#include <QApplication>
#include <QDebug>

#include "main_window.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    /*qDebug() << "Hello World";*/
    
    QApplication::setApplicationName("tambi");
    
    MainWindow mainWin;
    
    mainWin.show();
    return app.exec();
}
