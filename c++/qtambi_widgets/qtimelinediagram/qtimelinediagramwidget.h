
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

#include <qtambi_widgets/qtimelinediagram/qgraphicsguyitem.h>

class QTimelineDiagramWidget : public QWidget
{
    Q_OBJECT
    
public:
    QTimelineDiagramWidget(QJsonArray, QWidget *parent = 0);
    
    void addGuyItem(QJsonObject);
    void sortGuys();
    
private:
    QGraphicsView *view;
    QGraphicsScene *scene;
    QVBoxLayout *layout;
    
protected:
    
    
private slots:
    
    
signals:
    
    
};
