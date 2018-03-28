
#include <QWidget>
#include <QGraphicsView>
#include <QGraphicsScene>
#include <QGraphicsItem>
#include <QVBoxLayout>
#include <QDebug>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QJsonValue>

#include <QTransform>

class QBloodlineWidget : public QWidget
{
    Q_OBJECT
    
public:
    QBloodlineWidget(QJsonArray, QWidget *parent = 0);
    
    QJsonArray processGuy(int, QJsonArray, int, int);
    // returns the x-coordinate:
    int searchForCoevals(QJsonArray, QJsonObject);
    QPointF findCollisionFreeYPos(QPointF, int, int);
    void addGuyItem(QPointF, bool, bool, QString, QString);
    void searchForSuccession();
    void drawSuccessionLine(int, QJsonArray);
    
private:
    QGraphicsView *view;
    QGraphicsScene *scene;
    QVBoxLayout *layout;
    
protected:
    
    
private slots:
    
    
signals:
    
    
};
