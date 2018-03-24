
#include <qtambi_widgets/menu_bar.h>

#include <QAction>
#include <QMenuBar>
#include <QApplication>
#include <QKeySequence>

MenuBar::MenuBar(QMenuBar *parent)
{
    QAction *exitAction = new QAction(QIcon::fromTheme("application-exit"), "&Exit");
    exitAction->setShortcut(QKeySequence::fromString("Ctrl+Q"));
    exitAction->setStatusTip("Exit application");
    connect(exitAction, &QAction::triggered, this, &MenuBar::quitApplication);
    
    QAction *newCliTabAction = new QAction(QIcon::fromTheme("utilities-terminal"), "&New Command Line Tab");
    newCliTabAction->setShortcut(QKeySequence::fromString("Ctrl+T"));
    newCliTabAction->setStatusTip("Open new CLI Tab");
    connect(newCliTabAction, &QAction::triggered, this, &MenuBar::emitNewCliTab);
    
    QAction *newDualCliTabAction = new QAction(QIcon::fromTheme("utilities-terminal"), "&New Dual Command Line Tab");
    newDualCliTabAction->setShortcut(QKeySequence::fromString("Ctrl+D"));
    newDualCliTabAction->setStatusTip("Open new Dual Command Line Tab");
    connect(newDualCliTabAction, &QAction::triggered, this, &MenuBar::emitNewDualCliTab);
    
    QMenu *fileMenu = addMenu("&File");
    fileMenu->addAction(newCliTabAction);
    fileMenu->addAction(newDualCliTabAction);
    fileMenu->addSeparator();
    fileMenu->addAction(exitAction);
}

void MenuBar::loadModuleMenus()
{
    
}

void MenuBar::emitNewCliTab()
{
    emit newCliTab();
}

void MenuBar::emitNewDualCliTab()
{
    emit newDualCliTab();
}

void MenuBar::quitApplication()
{
    QApplication::quit();
}
