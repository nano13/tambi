
#include <QMainWindow>

#include <menu_bar.h>

class MainWindow : public QMainWindow
{
    Q_OBJECT
    
public:
    MainWindow(QWidget *parent = 0);
//     MainWindow();

private:
    QTabWidget *tab_widget;
    MenuBar *menuBar;
    
    QMap<QString, QString> dual_cli_label;
    
    void addNewDualCliTab();
    void addNewPythonTab();
    
    void activateNewTab();
    void setTabText(QString);
    void setDualTabText(QString, QString);
    
private slots:
    void closeTab(int);
    
    void addNewCliTab();
};
