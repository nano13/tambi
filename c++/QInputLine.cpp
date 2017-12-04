
#include <QInputLine.h>

#include <QWidget>
#include <QKeyEvent>
#include <QLineEdit>

// #include <QVariantList>

#include <QDebug>

// #include <PythonQt.h>

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
        {
            if (text() != "")
            {
                
                /*
                QVariantList args;
                args << text();
                context.call("historyWrite", args);
                qDebug() << text() << "---";
                */
                
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
//                 PythonQtObjectPtr context = PythonQt::self()->getMainModule();
//                 context.evalFile("./history_adapter.py");
//                 QVariantList args;
//                 args << text();
//                 context.call("historyWrite", args);
                
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
//             PythonQtObjectPtr context = PythonQt::self()->getMainModule();
//             context.evalFile("./history_adapter.py");
//             QVariant result = context.call("getHistorySize");
//             qDebug() << result;
            QVariant result = PythonEval("getHistorySize");
            int history_size = result.toInt();
            
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
//                 PythonQtObjectPtr context = PythonQt::self()->getMainModule();
//                 context.evalFile("./history_adapter.py");
                
                QVariantList args;
                args << history_counter << search_pattern_prefix;
                QVariant result = PythonEval("historyReadWithIndexAndPrefix", args);
//                 QVariant result = context.call("historyReadWithIndexAndPrefix", args);
                entry = result.toString();
                
                if (entry == "")
                {
                    search_pattern_prefix = "";
                    history_counter = 0;
                }
            }
            else
            {
//                 PythonQtObjectPtr context = PythonQt::self()->getMainModule();
//                 context.evalFile("./history_adapter.py");
                QVariantList args;
                args << history_counter;
//                 QVariant result = context.call("historyReadAtIndex", args);
                QVariant result = PythonEval("historyReadAtIndex", args);
                entry = result.toString();
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
//                 PythonQtObjectPtr context = PythonQt::self()->getMainModule();
//                 context.evalFile("./history_adapter.py");
//                 QVariantList args;
//                 args << history_counter << search_pattern_prefix;
//                 QVariant result = context.call("historyReadWithIndexAndPrefix", args);
//                 entry = result.toString();
            }
            else
            {
//                 PythonQtObjectPtr context = PythonQt::self()->getMainModule();
//                 context.evalFile("./history_adapter.py");
//                 QVariantList args;
//                 args << history_counter;
//                 QVariant result = context.call("historyReadAtIndex", args);
//                 entry = result.toString();
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

QVariant QInputLine::PythonEval(QString function)
{
    PythonQtObjectPtr context = PythonQt::self()->getMainModule();
//     context.evalFile("./history_adapter.py");
    context.evalScript(
"import sys, os\n"
"os.chdir('..')\n"
"sys.path.append('.')\n"
"from configs.history import History\n"
"history = History()\n"
"def historyWrite(text):\n"
"    history.historyWrite(text)\n"
"def getHistorySize():\n"
"    return history.getHistorySize()\n"
"def historyReadWithIndexAndPrefix(history_counter, search_pattern_prefix):\n"
"    return history.historyReadWithIndexAndPrefix(history_counter, search_pattern_prefix)\n"
"def historyReadAtIndex(history_counter):\n"
"    return history.historyReadAtIndex(history_counter)");
    QVariant result = context.call(function);
    qDebug() << result;
    
    return result;
}

QVariant QInputLine::PythonEval(QString function, QVariantList args)
{
    PythonQtObjectPtr context = PythonQt::self()->getMainModule();
//     context.evalFile("./history_adapter.py");
    context.evalScript(
"import sys, os\n"
"os.chdir('..')\n"
"sys.path.append('.')\n"
"from configs.history import History\n"
"history = History()\n"
"def historyWrite(text):\n"
"    history.historyWrite(text)\n"
"def getHistorySize():\n"
"    return history.getHistorySize()\n"
"def historyReadWithIndexAndPrefix(history_counter, search_pattern_prefix):\n"
"    return history.historyReadWithIndexAndPrefix(history_counter, search_pattern_prefix)\n"
"def historyReadAtIndex(history_counter):\n"
"    return history.historyReadAtIndex(history_counter)");
    QVariant result = context.call(function, args);
    qDebug() << result;
    
    return result;
}
