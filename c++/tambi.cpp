
#include <QMainWindow>
#include <QApplication>
#include <QDebug>

#include <main_window.h>

#include <PythonQt.h>

int main(int argc, char *argv[])
{
//     PythonQt::init(PythonQt::IgnoreSiteModule);
//     PythonQt::init();
    PythonQt::init(PythonQt::ExternalHelp);
    
    QApplication app(argc, argv);
    
    QApplication::setApplicationName("tambi");
    
    MainWindow mainWin;
    QIcon::setThemeSearchPaths(QStringList("../assets/icons"));
    QIcon::setThemeName("oxygen");
    mainWin.setWindowIcon(QIcon("../assets/icons/logo2.png"));
    mainWin.show();
    return app.exec();
}
