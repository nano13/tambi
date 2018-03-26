
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

class QBloodlineWidget : public QWidget
{
    Q_OBJECT
    
public:
    QBloodlineWidget(QJsonArray, QWidget *parent = 0);
    
    void addGuy(QPointF, bool, bool, QString, QString);
    
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
    
    bool good_start;
    bool good_end;
    QString name;
    QString name_original;
protected:
    // overriding mouse events
    void mousePressEvent(QGraphicsSceneMouseEvent *event);
    void mouseReleaseEvent(QGraphicsSceneMouseEvent *event);
};

#endif // QGRAPHICSGUYITEM_H
