
#include <qtambi_widgets/qbloodlinewidget.h>

QBloodlineWidget :: QBloodlineWidget (QJsonArray data, QWidget *parent)
    : QWidget (parent)
    , view (new QGraphicsView)
    , scene (new QGraphicsScene)
    , layout (new QVBoxLayout)
{
    view->setScene(scene);
    
    layout->setContentsMargins(0, 0, 0, 0);
    layout->addWidget(view);
    setLayout(layout);
    
    QGraphicsGuyItem *guy = new QGraphicsGuyItem();
    int guy_width = guy->boundingRect().width();
    delete guy;
    
    qDebug() << "############### guy ##############";
    for (int i = 0; i < data.size(); ++i)
    {
        // takeAt, but put back again later ...
        QJsonValue val = data.takeAt(i);
        QJsonObject obj = val.toObject();
        
        bool good_start = obj.value("good_start").toBool();
        bool good_end = obj.value("good_end").toBool();
        QString name = obj.value("name_de").toString();
        QString name_original = obj.value("name_original").toString();
        
        // INSERT GUY
        QPointF guy_pos = QPointF(i*guy_width*1, 0);
        addGuy(guy_pos, good_start, good_end, name, name_original);
        
        // INSERT COORDINATES TO THE QJsonArray
        QJsonValue x_val = QJsonValue(guy_pos.x());
        obj.insert("render_pos_x", x_val);
        QJsonValue y_val = QJsonValue(guy_pos.y());
        obj.insert("render_pos_y", y_val);
        
        data.insert(i, obj);
    }
}

void QBloodlineWidget :: addGuy(QPointF pos, bool good_start, bool good_end, QString name, QString name_original)
{
    QGraphicsGuyItem *guy = new QGraphicsGuyItem();
    guy->setGoodness(good_start, good_end);
    guy->setNames(name, name_original);
    guy->setPos(pos);
    scene->addItem(guy);
}


// END QBloodlineWidget


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

void QGraphicsGuyItem::setNames(QString name, QString name_original)
{
    this->name = name;
    this->name_original = name_original;
}

QRectF QGraphicsGuyItem::boundingRect() const
{
    // outer most edges
    //return QRectF(-5,0,20,40);
    return QRectF(-45,0,100,64);
}

void QGraphicsGuyItem::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    painter->setRenderHint(QPainter::Antialiasing);
    //painter->setRenderHint(QPainter::HighQualityAntialiasing);
    
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
    
    // LABEL
    QPen pen_label(Qt::black, 1);
    painter->setPen(pen_label);
    painter->setBrush(Qt::NoBrush);
    QFont font_name = painter->font();
    font_name.setPixelSize(12);
    painter->setFont(font_name);
    painter->drawText(QRect(-45, 40, 100, 12), Qt::AlignCenter, name);
    
    painter->drawText(QRect(-45, 52, 100, 12), Qt::AlignCenter, name_original);
    
    // BOUNDING BOX
    QRectF bounding_rect = boundingRect();
    QPen pen_bb(Qt::green, 1);
    painter->setPen(pen_bb);
    painter->setBrush(Qt::NoBrush);
    //painter->drawRect(bounding_rect);
    //painter->drawRect(QRect(-45, 40, 100, 12));
    
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
