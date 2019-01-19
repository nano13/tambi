
#include <QWidget>
#include <QGridLayout>
#include <QLineEdit>
#include <QVector>
#include <QStringList>
#include <QGraphicsView>
#include <QGraphicsScene>

#include <QThread>

#include <QTableWidget>
#include <QTextEdit>
#include <QGridLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QIcon>

#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonValue>
#include <QJsonArray>

#include <QGraphicsView>
#include <QGraphicsScene>

#include <QStandardPaths>
#include <QDir>

#include <QFileDialog>

#include <QDebug>

#include <PythonQt.h>
#include <PythonQt_QtAll.h>

#include "qinputline.h"
#include "python_adapter.h"
#include "unicode_fonts.h"
#include "format_output.h"
#include "qitemizedwidget.h"
#include "qtimelinediagram/qtimelinediagramwidget.h"

//#include <tts_interface.h>


class QCliWidget : public QWidget
{
    Q_OBJECT
    
public:
    QCliWidget(QWidget *parent = 0);
    
private:
    QGridLayout *grid;
    QInputLine *input_line;
    QWidget *old_display_widget;
    QWidget *display_widget;
    QGraphicsView *view;
    QGraphicsScene *scene;
    int this_x;
    int this_y;
    float SCALE_FACTOR = 1.15;
    
    UnicodeFonts *unicodeFonts;
    
    int getMatrixMaxWidth(QVector<QStringList>);
    
    void addDisplayWidget(QWidget *display_widget);
    void resizeDisplayWidget();
    
    void clearDisplayWidget();
    void makeSnapshot();
    
    bool isImage();
    bool isAudio();
    
private slots:
    void commandEntered(QString);
    void processResult(QJsonDocument);
    
    void resultInTextEdit(QString);
    void resultInTable(QVector<QStringList>);
    void resultInMultimediaTable(QVector<QStringList>);
    void resultInItemizedWidget(QVector<QStringList>);
    void resultInTimelineDiagramWidget(QJsonObject);
    void resultInImageWidget();
    void resultInDiagram();
    void showErrorMessage();
    
    void resizeEvent(QResizeEvent *event);
    void onZoomInClicked();
    void onZoomOutClicked();
    void onZoomResetClicked();
    
signals:
    void setTabText(QString);
};


class HandleCommandThread : public QThread
{
    Q_OBJECT

public:
    HandleCommandThread(QThread *parent = 0);
    void setCommand(QString);
    
protected:
    void run();
    
private:
    PythonAdapter *py_adapt;
    QString command;
    
signals:
    void processResult(QJsonDocument);
};
