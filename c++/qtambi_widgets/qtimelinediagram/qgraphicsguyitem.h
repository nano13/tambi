
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
    
    QString _id;
    //Q_PROPERTY(QString id_private READ id WRITE setID) // [A-Z]*_[0-9]*
    Role _role;
    //Q_PROPERTY(Role role READ role WRITE setRole)
    QString _name;
    QString _name_original; // greek or hebrew
    QString _name_meaning;
    Sex _sex;
    //Q_PROPERTY(Sex sex READ sex WRITE setSex)
    int _age_death;
    //Q_PROPERTY(int age_death READ ageDeath WRITE setAgeDeath)
    int _age_firstson;
    //Q_PROPERTY(int age_firstson READ ageDeath WRITE setAgeDeath)
    QList<QString> _coevals;
    //Q_PROPERTY(QList<QString> coevals READ coevals WRITE setCoevals) // id's of other entities
    QList<QString> _bible_refs;
    //Q_PROPERTY(QList<QString> bible_refs READ bibleRefs WRITE setBibleRefs)
    bool good_start;
    bool good_end;
    QString _description;
    //Q_PROPERTY(QString description READ description WRITE setDescription) // some human-readable infos about this guy
    QString _predecessor;
    //Q_PROPERTY(QString predecessor READ predecessor WRITE setPredecessor) // id's of other entities
    QString _successor;
    //Q_PROPERTY(QString successor READ successor WRITE setSuccessor) // id's of other entities
    
public:
    QGraphicsGuyItem();
    
    QRectF boundingRect() const;
    
    // overriding type()
    enum { Type = UserType + 1 };
    int type() const
    {
        return Type;
    }
    
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

public Q_SLOTS:
    QString id();
    Role role();
    QList<QString> names();
    Sex sex();
    int ageDeath();
    int ageFirstSon();
    QList<QString> coevals();
    QList<QString> bibleRefs();
    QList<bool> goodness();
    QString description();
    QString predecessor();
    QString successor();

protected:
    // overriding mouse events
    void mousePressEvent(QGraphicsSceneMouseEvent *event);
    void mouseReleaseEvent(QGraphicsSceneMouseEvent *event);
};

#endif // QGRAPHICSGUYITEM_H
