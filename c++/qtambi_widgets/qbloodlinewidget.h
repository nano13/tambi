
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

class QBloodlineWidget : public QWidget
{
    Q_OBJECT
    
public:
    QBloodlineWidget(QJsonArray, QWidget *parent = 0);
    
    QJsonArray processGuy(int, QJsonArray, int, int);
    // returns the x-coordinate:
    int searchForCoevals(QJsonArray, QJsonObject);
    QPointF findCollisionFreeYPos(QPointF, int, int);
    void addGuyItem(QPointF, bool, bool, QString, QString);
    void searchForSuccession();
    void drawSuccessionLine(int, QJsonArray);
    
private:
    QGraphicsView *view;
    QGraphicsScene *scene;
    QVBoxLayout *layout;
    
protected:
    
    
private slots:
    
    
signals:
    
    
};

// END QBloodlineWidget

#ifndef QGRAPHICSGUYITEM_H
#define QGRAPHICSGUYITEM_H

#include <QPainter>
#include <QGraphicsItem>
#include <QGraphicsEllipseItem>

class QGraphicsGuyItem : public QGraphicsItem
{
public:
    QGraphicsGuyItem();
    void setGoodness(bool, bool);
    void setNames(QString, QString);
    QRectF boundingRect() const;

    // overriding paint()
    void paint(QPainter * painter,
               const QStyleOptionGraphicsItem * option,
               QWidget * widget);

    // item state
    bool mouse_pressed;
    
    QString id; // [A-Z]*_[0-9]*
    enum role { king, king_north, king_south, prophet, prophet_north, prophet_south };
    QString name;
    QString name_original; // greek or hebrew
    QString name_meaning;
    enum sex { male, female };
    int age_death;
    int age_firstson;
    QList<QString> coevals; // id's of other entities
    QList<QString> bible_refs;
    bool good_start;
    bool good_end;
    QString description; // some human-readable infos about this guy
    QString predecessor; // id's of other entities
    QString successor; // id's of other entities
    
protected:
    // overriding mouse events
    void mousePressEvent(QGraphicsSceneMouseEvent *event);
    void mouseReleaseEvent(QGraphicsSceneMouseEvent *event);
};

#endif // QGRAPHICSGUYITEM_H
