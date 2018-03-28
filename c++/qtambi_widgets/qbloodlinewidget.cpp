
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
    int guy_height = guy->boundingRect().height();
    delete guy;
    
    qDebug() << "############### guy ##############";
    for (int i = 0; i < data.size(); ++i)
    {
        data = processGuy(i, data, guy_width, guy_height);
        
        if (i > 1)
        {
            drawSuccessionLine(i, data);
        }
    }
    //qDebug() << data;
}

void QBloodlineWidget :: searchForSuccession()
{
    
}

QJsonArray QBloodlineWidget :: processGuy(int i, QJsonArray data, int guy_width, int guy_height)
{
    // takeAt, but put back again later ...
    QJsonValue val = data.takeAt(i);
    QJsonObject obj = val.toObject();
    
    int match_x = searchForCoevals(data, obj);
    
    bool good_start = obj.value("good_start").toBool();
    bool good_end = obj.value("good_end").toBool();
    QString name = obj.value("name_de").toString();
    QString name_original = obj.value("name_original").toString();
    
    // INSERT GUY
    QPointF guy_pos;
    if (match_x == -10000)
    {
        guy_pos = QPointF(i*guy_width*1, 0);
    }
    else
    {
        guy_pos = findCollisionFreeYPos(guy_pos, guy_height, match_x);
    }
    
    addGuyItem(guy_pos, good_start, good_end, name, name_original);
    
    // INSERT COORDINATES TO THE QJsonArray
    QJsonValue x_val = QJsonValue(guy_pos.x());
    obj.insert("render_pos_x", x_val);
    QJsonValue y_val = QJsonValue(guy_pos.y());
    obj.insert("render_pos_y", y_val);
    
    data.insert(i, obj);
    
    return data;
}

int QBloodlineWidget :: searchForCoevals(QJsonArray data, QJsonObject guy)
{
    int result;
    
    QJsonArray guy_coevals = guy.value("coevals").toArray();
    foreach(QJsonValue coeval, guy_coevals)
    {
        if (coeval.isString())
        {
            QString co = coeval.toString();
            if (co.length() > 0)
            {
                foreach(QJsonValue d, data)
                {
                    QJsonObject o = d.toObject();
                    QString found_id = o.value("id").toString();
                    if (found_id == co)
                    {
                        result = o.value("render_pos_x").toInt();
                        qDebug() << result;
                        if (result != 0)
                        {
                            //return result;
                        }
                    }
                }
            }
        }
    }
    
    return -10000;
}

QPointF QBloodlineWidget :: findCollisionFreeYPos(QPointF guy_pos, int guy_height, int match_x)
{
    int i = 0;
    bool once_again = true;
    while (once_again)
    {
        i++;
        guy_pos = QPointF(match_x, (10+guy_height)*i);
        
        QGraphicsItem *gitem = scene->itemAt(guy_pos, QTransform());
        if (gitem == 0)
        {
            once_again = false;
        }
    }
    
    return guy_pos;
}

void QBloodlineWidget :: addGuyItem(QPointF pos, bool good_start, bool good_end, QString name, QString name_original)
{
    QGraphicsGuyItem *guy = new QGraphicsGuyItem();
    guy->setGoodness(good_start, good_end);
    guy->setNames(name, name_original);
    guy->setPos(pos);
    scene->addItem(guy);
}

void QBloodlineWidget :: drawSuccessionLine(int i, QJsonArray data)
{
    QJsonValue val_succ = data.at(i-1);
    QJsonObject obj_succ = val_succ.toObject();
    QString succ = obj_succ.value("successor").toString();
    
    QJsonValue val_pred = data.at(i);
    QJsonObject obj_pred = val_pred.toObject();
    QString pred = obj_pred.value("id").toString();
    
    if (pred == succ)
    {
        int x_succ = obj_succ.value("render_pos_x").toInt();
        int y_succ = obj_succ.value("render_pos_y").toInt();
        
        int x_pred = obj_pred.value("render_pos_x").toInt();
        int y_pred = obj_pred.value("render_pos_y").toInt();
        
        scene->addLine(x_succ, y_succ, x_pred, y_pred);
    }
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
