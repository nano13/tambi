
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
    
    int getMatrixMaxWidth(QVector<QStringList>);
    void connectToPython();
    
    void addDisplayWidget(QWidget *display_widget);
    void resizeDisplayWidget();
    
private slots:
    void commandEntered(QString);
    void resultInTextEdit(QString);
    void resultInTable(QVector<QStringList>);
    void resizeEvent(QResizeEvent *event);
    void onZoomInClicked();
    void onZoomOutClicked();
    void onZoomResetClicked();
};
