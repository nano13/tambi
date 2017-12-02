
#include <QInputLine.h>

#include <QWidget>
#include <QKeyEvent>
#include <QLineEdit>

#include <QDebug>

QInputLine::QInputLine(QLineEdit *parent)
{
    int history_counter = 0;
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
            history_counter = 0;
            break;
            
        case Qt::Key_Enter:
            emit returnPressed(text());
            setText("");
            history_counter = 0;
            break;
            
        case Qt::Key_Up:
            
            break;
            
        case Qt::Key_Down:
            
            break;
    }
    if (event->modifiers() & Qt::ControlModifier)
    {
        if (event->key() == Qt::Key_C)
        {
            history_counter = 0;
            setText("");
        }
    }
    QLineEdit::keyPressEvent(event);
}
