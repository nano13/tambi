
#ifndef MENU_BAR
#define MENU_BAR

#include <QMenuBar>

class MenuBar : public QMenuBar
{
    Q_OBJECT
    
public:
    MenuBar(QMenuBar *parent = 0);
    
private:
    void emitNewCliTab();
    void emitNewDualCliTab();
    void quitApplication();
    
    void loadModuleMenus();
    
signals:
    void newCliTab();
    void newDualCliTab();
};

#endif
