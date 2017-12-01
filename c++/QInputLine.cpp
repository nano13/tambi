
#include <QInputLine.h>

#include <QWidget>
#include <QKeyEvent>
#include <QLineEdit>

#include <QDebug>

QInputLine::QInputLine(QLineEdit *parent)
{
    
}

void QInputLine::appendText(QString text)
{
    
}

void QInputLine::keyPressEvent(QKeyEvent *event)
{
    /*
    if (event->key() == Qt::Key_Return)
    {
        qDebug() << "ENTER";
        
    }
    else if (event->key() == Qt::Key_Enter)
    {
        qDebug() << "Enter";
    }
    else if (event->key() == Qt::Key_Up)
    {
        qDebug() << "UP";
    }
    */
//     case event->key()
    QLineEdit::keyPressEvent(event);
}
