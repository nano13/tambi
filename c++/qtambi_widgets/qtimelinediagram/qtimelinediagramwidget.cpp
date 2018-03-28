
#include <qtambi_widgets/qtimelinediagram/qtimelinediagramwidget.h>

QTimelineDiagramWidget :: QTimelineDiagramWidget (QJsonArray data, QWidget *parent)
    : QWidget (parent)
    , view (new QGraphicsView)
    , scene (new QGraphicsScene)
    , layout (new QVBoxLayout)
{
    view->setScene(scene);
    
    layout->setContentsMargins(0, 0, 0, 0);
    layout->addWidget(view);
    setLayout(layout);
    
    
}







void QTimelineDiagramWidget :: addGuyItem(QPointF pos, bool good_start, bool good_end, QString name, QString name_original)
{
    QGraphicsGuyItem *guy = new QGraphicsGuyItem();
    guy->setGoodness(good_start, good_end);
    guy->setNames(name, name_original);
    guy->setPos(pos);
    scene->addItem(guy);
}
