
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
#include <QStack>
#include <QTransform>

#include <qtambi_widgets/qtimelinediagram/qgraphicsguyitem.h>

class QTimelineDiagramWidget : public QWidget
{
    Q_OBJECT
    
public:
    QTimelineDiagramWidget(QJsonArray, QWidget* parent = 0);
    
    void addGuyItem(QJsonObject);
    void searchFurkationsAndConfluences();
    void sortGuys();
    
    void buildTree();
    bool traverseTreeForMatchingNode(QGraphicsItem* node, QString id);

    
private:
    QGraphicsView* view;
    QGraphicsScene* scene;
    QVBoxLayout* layout;

    // list of all found furcations and confluences
    // saved as a list of the according items
    QList<QList<QGraphicsItem*>> furcations;
    QList<QList<QGraphicsItem*>> confluences;
    
    QGraphicsItem* root_item;
    QGraphicsItem* found_guy;
    
protected:
    
    
private slots:
    
signals:
    
    
};
