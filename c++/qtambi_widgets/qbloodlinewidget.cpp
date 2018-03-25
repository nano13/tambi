
#include <qtambi_widgets/qbloodlinewidget.h>

QBloodlineWidget :: QBloodlineWidget (QVector<QStringList> data, QWidget *parent)
    : QWidget (parent)
    , view (new QGraphicsView)
    , scene (new QGraphicsScene)
    , layout (new QVBoxLayout)
{
    view->setScene(scene);
    
    layout->setContentsMargins(0, 0, 0, 0);
    layout->addWidget(view);
    setLayout(layout);
    
    qDebug() << data;
    for (int i = 0; i < data.length(); ++i)
    {
        //QStringList item = data[i];
        //qDebug() << item;
        
        QGraphicsGuyItem *guy = new QGraphicsGuyItem();
        int width = guy->boundingRect().width();
        addGuy(i*width*2, 0, true, false);
    }
}

void QBloodlineWidget :: addGuy(int x, int y, bool good_start, bool good_end)
{
    QGraphicsGuyItem *guy = new QGraphicsGuyItem();
    guy->setGoodness(true, false);
    guy->setPos(x, y);
    scene->addItem(guy);
}


// %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


QGraphicsGuyItem::QGraphicsGuyItem()
{
    mouse_pressed = false;
    setFlag(ItemIsMovable);
}

void QGraphicsGuyItem::setGoodness(bool good_start, bool good_end)
{
    this->good_start = good_start;
    this->good_end = good_end;
}

QRectF QGraphicsGuyItem::boundingRect() const
{
    // outer most edges
    return QRectF(-5,0,20,40);
}

void QGraphicsGuyItem::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    // HEAD
    painter->setBrush(Qt::SolidPattern);
    painter->drawEllipse(0, 0, 10, 10);
    
    // LEFT BODY
    if (good_start)
    {
        painter->setBrush(Qt::NoBrush);
    }
    else
    {
        painter->setBrush(Qt::SolidPattern);
    }
    QPointF poly_left[3] = {
        QPointF(5, 5), QPointF(-5, 40), QPointF(5, 40)
    };
    painter->drawPolygon(poly_left, 3);
    
    // RIGHT BODY
    if (good_end)
    {
        painter->setBrush(Qt::NoBrush);
    }
    else
    {
        painter->setBrush(Qt::SolidPattern);
    }
    QPointF poly_right[3] = {
        QPointF(5, 5), QPointF(15, 40), QPointF(5, 40)
    };
    painter->drawPolygon(poly_right, 3);
    
    // BOUNDING BOX
    QRectF bounding_rect = boundingRect();
    QPen pen(Qt::green, 1);
    painter->setPen(pen);
    painter->setBrush(Qt::NoBrush);
    painter->drawRect(bounding_rect);
    
    /*
    QRectF rect = boundingRect();
    
    if(mouse_pressed)
    {
        QPen pen(Qt::red, 1);
        painter->setPen(pen);
        painter->drawEllipse(rect);
    }
    else
    {
        QPen pen(Qt::black, 1);
        painter->setPen(pen);
        painter->drawRect(rect);
    }
    */
}

void QGraphicsGuyItem::mousePressEvent(QGraphicsSceneMouseEvent *event)
{
    mouse_pressed = true;
    update();
    QGraphicsItem::mousePressEvent(event);
}

void QGraphicsGuyItem::mouseReleaseEvent(QGraphicsSceneMouseEvent *event)
{
    mouse_pressed = false;
    update();
    QGraphicsItem::mouseReleaseEvent(event);
}
