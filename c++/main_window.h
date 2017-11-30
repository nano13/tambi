
#include <QMainWindow>

class MainWindow : public QMainWindow
{
    Q_OBJECT
    
public:
    MainWindow();

private:
    QTabWidget *tab_widget;
    
    void addNewCliTab();
    void addNewDualCliTab();
    void activateNewTab();
    void setTabText(int, QString);
    
private slots:
    void closeTab(int);
};
