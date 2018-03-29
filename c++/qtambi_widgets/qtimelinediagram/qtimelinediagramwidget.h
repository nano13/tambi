
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
    void searchFurkationsAndConfluences();
    void sortGuys();
    
    void buildTree();
    QGraphicsItem* traverseTreeForMatchingNode(QGraphicsGuyItem *node, QString id);

    
private:
    QGraphicsView *view;
    QGraphicsScene *scene;
    QVBoxLayout *layout;

    // list of all found furcations and confluences
    // saved as a list of the according items
    QList<QList<QGraphicsItem*>> furcations;
    QList<QList<QGraphicsItem*>> confluences;
    
    QGraphicsItem *root_item;
    bool traverse_found_sth = false;
    
protected:
    
    
private slots:
    //void traverseFoundNothing();
    
signals:
    
    
};
