
#include <QWidget>
#include <QGridLayout>
#include <QLineEdit>
#include <QVector>
#include <QStringList>
#include <QGraphicsView>
#include <QGraphicsScene>

#include <QInputLine.h>
#include <python_adapter.h>

class QCliWidget : public QWidget
{
    Q_OBJECT
    
public:
    QCliWidget(QWidget *parent = 0);
    
private:
    QGridLayout *grid;
    QInputLine *input_line;
    QWidget *old_display_widget;
    QGraphicsView *view;
    QGraphicsScene *scene;
    int this_x;
    int this_y;
    float SCALE_FACTOR = 1.15;
    
    PythonAdapter *py_adapt;
    
    int getMatrixMaxWidth(QVector<QStringList>);
    
    void addDisplayWidget(QWidget *display_widget);
    void resizeDisplayWidget();
    
    void clearDisplayWidget();
    void makeSnapshot();
    
    bool isImage();
    bool isAudio();
    
private slots:
    void commandEntered(QString);
    
    void resultInTextEdit(QString);
    void resultInTable(QVector<QStringList>);
    void resultInMultimediaTable(QVector<QStringList>);
    void resultInItemizedWidget();
    void resultInImageWidget();
    void resultInDiagram();
    void showErrorMessage();
    
    void resizeEvent(QResizeEvent *event);
    void onZoomInClicked();
    void onZoomOutClicked();
    void onZoomResetClicked();
};
