
#include <QtWidgets>

#include <main_window.h>
#include <cli_widget.h>
#include <menu_bar.h>

#include <QHBoxLayout>
#include <QMap>

// MainWindow::MainWindow()
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , tab_widget(new QTabWidget)
    , menuBar(new MenuBar)
{
    resize(825, 670);
    
    tab_widget->setTabsClosable(true);
    tab_widget->setMovable(true);
//     tab_widget->setDocumentMode(true);
    
    connect(tab_widget, &QTabWidget::tabCloseRequested, this, &MainWindow::closeTab);
    addNewCliTab();
    
    setCentralWidget(tab_widget);
    setMenuBar(menuBar);
    
    connect(menuBar, &MenuBar::newCliTab, this, &MainWindow::addNewCliTab);
    connect(menuBar, &MenuBar::newDualCliTab, this, &MainWindow::addNewDualCliTab);
}

void MainWindow::closeTab(int tab_id)
{
    tab_widget->removeTab(tab_id);
    dual_cli_label.remove(QString::number(tab_id)+"_"+"left");
    dual_cli_label.remove(QString::number(tab_id)+"_"+"right");
}

void MainWindow::addNewCliTab()
{
    QCliWidget *cli = new QCliWidget();
    tab_widget->addTab(cli, "cli");
    connect(cli, &QCliWidget::setTabText, this, &MainWindow::setTabText);
    
    activateNewTab();
}

void MainWindow::addNewDualCliTab()
{
    QCliWidget *cli_left = new QCliWidget();
    QCliWidget *cli_right = new QCliWidget();
    
    connect(cli_left, &QCliWidget::setTabText, [=](const QString &command) { this->setDualTabText("left", command); });
    connect(cli_right, &QCliWidget::setTabText, [=](const QString &command) { this->setDualTabText("right", command); });
    
    QSizePolicy policy(QSizePolicy::Preferred, QSizePolicy::Preferred);
    policy.setHorizontalStretch(1);
    cli_left->setSizePolicy(policy);
    cli_right->setSizePolicy(policy);
    
    QHBoxLayout *layout = new QHBoxLayout();
    layout->addWidget(cli_left);
    layout->addWidget(cli_right);
    QWidget *dualCliWidget = new QWidget();
    dualCliWidget->setLayout(layout);

    tab_widget->addTab(dualCliWidget, "dual cli");
    activateNewTab();
}

void MainWindow::activateNewTab()
{
    tab_widget->setCurrentIndex(tab_widget->count()-1);
}

void MainWindow::setTabText(QString text)
{
    int tab_id = tab_widget->currentIndex();
    tab_widget->setTabText(tab_id, text);
}

void MainWindow::setDualTabText(QString position, QString text)
{
    // we need "tab_id" and "position" together as the key
    QString tab_id = QString::number(tab_widget->currentIndex());
    dual_cli_label.insert(tab_id +"_"+position, text);
    
    QString label = dual_cli_label.value(tab_id+"_"+"left") + " | " + dual_cli_label.value(tab_id+"_"+"right");
    setTabText(label);
}
