
#include <qtambi_widgets/QInputLine.h>

#include <QWidget>
#include <QKeyEvent>
#include <QLineEdit>

// #include <QVariantList>

#include <QDebug>

QInputLine::QInputLine(QLineEdit *parent)
{
    PythonAdapter *py_adapt = new PythonAdapter();
}

void QInputLine::appendText(QString text)
{
    
}

void QInputLine::keyPressEvent(QKeyEvent *event)
{
    switch (event->key())
    {
        case Qt::Key_Return:
        {
            if (text() != "")
            {
                py_adapt->historyWrite(text());
                
                qDebug() << "Return Pressed";
                
                emit returnPressed(text());
                setText("");
                history_counter = 0;
            }
            break;
        }
        case Qt::Key_Enter:
        {
            if (text() != "")
            {
                py_adapt->historyWrite(text());
                qDebug() << "Enter Pressed";
                
                emit returnPressed(text());
                setText("");
                history_counter = 0;
            }
            break;
        }
        case Qt::Key_Up:
        {
            qDebug() << "KEY UP";
            
            int history_size = py_adapt->getHistorySize();
            
            if (history_counter < history_size)
            {
                history_counter++;
            }
            
            if (history_counter == 1)
            {
                search_pattern_prefix = text();
            }
            
            QString entry = "";
            if (text() != "")
            {
                entry = py_adapt->historyReadWithIndexAndPrefix(history_counter, search_pattern_prefix);
                
                if (entry == "")
                {
                    search_pattern_prefix = "";
                    history_counter = 0;
                }
            }
            else
            {
                entry = py_adapt->historyReadAtIndex(history_counter);
            }
            setText(entry);
            
            break;
        }
        case Qt::Key_Down:
        {
            history_counter--;
            if (history_counter < 0)
            {
                history_counter = 0;
            }
            
            QString entry;
            if (search_pattern_prefix != "")
            {
                entry = py_adapt->historyReadWithIndexAndPrefix(history_counter, search_pattern_prefix);
            }
            else
            {
                entry = py_adapt->historyReadAtIndex(history_counter);
            }
            setText(entry);
            
            break;
        }
        default:
        {
            history_counter = 0;
            break;
        }
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
