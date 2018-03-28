
#ifndef QGRAPHICSGUYITEM_H
#define QGRAPHICSGUYITEM_H

#include <QPainter>
#include <QGraphicsItem>
#include <QGraphicsEllipseItem>

class QGraphicsGuyItem : public QGraphicsItem
{
public:
    enum Role { king, king_north, king_south, prophet, prophet_north, prophet_south };
    enum Sex { male, female };

private:
    // item state
    bool mouse_pressed;
    
    QString id; // [A-Z]*_[0-9]*
    Role role;
    QString name;
    QString name_original; // greek or hebrew
    QString name_meaning;
    Sex sex;
    int age_death;
    int age_firstson;
    QList<QString> coevals; // id's of other entities
    QList<QString> bible_refs;
    bool good_start;
    bool good_end;
    QString description; // some human-readable infos about this guy
    QString predecessor; // id's of other entities
    QString successor; // id's of other entities
    
public:
    QGraphicsGuyItem();
    
    QRectF boundingRect() const;

    // overriding paint()
    void paint(QPainter *painter,
               const QStyleOptionGraphicsItem *option,
               QWidget *widget);
    
    void setID(QString);
    void setRole(Role);
    void setNames(QString, QString, QString);
    void setSex(Sex);
    void setAgeDeath(int);
    void setAgeFirstSon(int);
    void setCoevals(QList<QString>);
    void setBibleRefs(QList<QString>);
    void setGoodness(bool, bool);
    void setDescription(QString);
    void setPredecessor(QString);
    void setSuccessor(QString);
    
    
protected:
    // overriding mouse events
    void mousePressEvent(QGraphicsSceneMouseEvent *event);
    void mouseReleaseEvent(QGraphicsSceneMouseEvent *event);
};

#endif // QGRAPHICSGUYITEM_H
