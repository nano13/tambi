
#include <qtambi_widgets/qtimelinediagram/qgraphicsguyitem.h>

QGraphicsGuyItem::QGraphicsGuyItem()
{
    mouse_pressed = false;
    setFlag(ItemIsMovable);
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
    painter->drawText(QRect(-45, 40, 100, 12), Qt::AlignCenter, _name);
    
    painter->drawText(QRect(-45, 52, 100, 12), Qt::AlignCenter, _name_original);
    
    // BOUNDING BOX
    QRectF bounding_rect = boundingRect();
    QPen pen_bb(Qt::green, 1);
    painter->setPen(pen_bb);
    painter->setBrush(Qt::NoBrush);
    //painter->drawRect(bounding_rect);
    //painter->drawRect(QRect(-45, 40, 100, 12));
}

void QGraphicsGuyItem::mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event)
{
    showGuyDetailsWindow();
    QGraphicsItem::mouseDoubleClickEvent(event);
}

void QGraphicsGuyItem::showGuyDetailsWindow()
{
    QGuyDetailsWindow *guy_details_window = new QGuyDetailsWindow();
    guy_details_window->setID(_id);
    //guy_details_window->setRole(_role);
    guy_details_window->setNames(_name, _name_original, _name_meaning);
    
    guy_details_window->show();
}

void QGraphicsGuyItem::setID(QString id)
{
    this->_id = id;
}

void QGraphicsGuyItem::setRole(Role role)
{
    this->_role = role;
}

void QGraphicsGuyItem::setNames(QString name, QString name_original, QString name_meaning)
{
    this->_name = name;
    this->_name_original = name_original;
    this->_name_meaning = name_meaning;
}

void QGraphicsGuyItem::setSex(Sex sex)
{
    this->_sex = sex;
}

void QGraphicsGuyItem::setAgeDeath(int age_death)
{
    this->_age_death = age_death;
}

void QGraphicsGuyItem::setAgeFirstSon(int age_firstson)
{
    this->_age_firstson = age_firstson;
}

void QGraphicsGuyItem::setCoevals(QList<QString> coevals)
{
    this->_coevals = coevals;
}

void QGraphicsGuyItem::setBibleRefs(QList<QString> bible_refs)
{
    this->_bible_refs = bible_refs;
}

void QGraphicsGuyItem::setGoodness(bool good_start, bool good_end)
{
    this->good_start = good_start;
    this->good_end = good_end;
}

void QGraphicsGuyItem::setDescription(QString description)
{
    this->_description = description;
}

void QGraphicsGuyItem::setPredecessor(QString predecessor)
{
    this->_predecessor = predecessor;
}

void QGraphicsGuyItem::setSuccessor(QString successor)
{
    this->_successor = successor;
}

QString QGraphicsGuyItem::id()
{
    return _id;
}
QGraphicsGuyItem::Role QGraphicsGuyItem::role()
{
    return _role;
}
QList<QString> QGraphicsGuyItem::names()
{
    QList<QString> ret_list;
    ret_list << _name << _name_original << _name_meaning;
    return ret_list;
}
QGraphicsGuyItem::Sex QGraphicsGuyItem::sex()
{
    return _sex;
}
int QGraphicsGuyItem::ageDeath()
{
    return _age_death;
}
int QGraphicsGuyItem::ageFirstSon()
{
    return _age_firstson;
}
QList<QString> QGraphicsGuyItem::coevals()
{
    return _coevals;
}
QList<QString> QGraphicsGuyItem::bibleRefs()
{
    return _bible_refs;
}
QList<bool> QGraphicsGuyItem::goodness()
{
    QList<bool> ret_list;
    ret_list << good_start << good_end;
    return ret_list;
}
QString QGraphicsGuyItem::description()
{
    return _description;
}
QString QGraphicsGuyItem::predecessor()
{
    return _predecessor;
}
QString QGraphicsGuyItem::successor()
{
    return _successor;
}
