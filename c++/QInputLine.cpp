
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
    switch (event->key())
    {
        case Qt::Key_Return:
            emit returnPressed(text());
            setText("");
            break;
            
        case Qt::Key_Enter:
            emit returnPressed(text());
            setText("");
            break;
            
        case Qt::Key_Up:
            
            break;
            
        case Qt::Key_Down:
            
            break;
    }
    QLineEdit::keyPressEvent(event);
}
