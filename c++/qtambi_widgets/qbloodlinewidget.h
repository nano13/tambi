
#include <QWidget>
#include <QGraphicsView>
#include <QGraphicsScene>
#include <QGraphicsItem>
#include <QVBoxLayout>
#include <QDebug>
#include <QJsonObject>

class QBloodlineWidget : public QWidget
{
    Q_OBJECT
    
public:
    QBloodlineWidget(QVector<QStringList>, QWidget *parent = 0);
    
    void addGuy(int x, int y, bool, bool);
    
private:
    QGraphicsView *view;
    QGraphicsScene *scene;
    QVBoxLayout *layout;
    
protected:
    
    
private slots:
    
    
signals:
    
    
};



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
    QRectF boundingRect() const;

    // overriding paint()
    void paint(QPainter * painter,
               const QStyleOptionGraphicsItem * option,
               QWidget * widget);

    // item state
    bool mouse_pressed;
    
    bool good_start;
    bool good_end;
protected:
    // overriding mouse events
    void mousePressEvent(QGraphicsSceneMouseEvent *event);
    void mouseReleaseEvent(QGraphicsSceneMouseEvent *event);
};

#endif // QGRAPHICSGUYITEM_H
