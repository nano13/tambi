
#include <qtambi_widgets/python_adapter.h>

#include <QVariantList>

#include <QJsonDocument>

#include <QDebug>

#include <PythonQt.h>
// #include <PythonQt_QtAll.h>

PythonAdapter::PythonAdapter(QObject *parent)
{
//     PythonQt::init(PythonQt::IgnoreSiteModule);
//     PythonQt::init();
//     PythonQt::init(PythonQt::ExternalHelp);
}

int PythonAdapter::getHistorySize()
{
    PythonQtObjectPtr context = PythonQt::self()->getMainModule();
    context.evalFile("./python_adapter.py");
    QVariant result = context.call("getHistorySize");
//     qDebug() << result;
    int history_size = result.toInt();
    
    return history_size;
}

void PythonAdapter::historyWrite(QString entry)
{
    PythonQtObjectPtr context = PythonQt::self()->getMainModule();
    context.evalFile("./python_adapter.py");
    QVariantList args;
    args << entry;
    context.call("historyWrite", args);
}

QString PythonAdapter::historyReadWithIndexAndPrefix(int history_counter, QString search_pattern_prefix)
{
    PythonQtObjectPtr context = PythonQt::self()->getMainModule();
    context.evalFile("./python_adapter.py");
    QVariantList args;
    args << history_counter << search_pattern_prefix;
    QVariant result = context.call("historyReadWithIndexAndPrefix", args);
    QString entry = result.toString();
    
    return entry;
}

QString PythonAdapter::historyReadAtIndex(int history_counter)
{
    PythonQtObjectPtr context = PythonQt::self()->getMainModule();
    context.evalFile("./python_adapter.py");
    QVariantList args;
    args << history_counter;
    QVariant result = context.call("historyReadAtIndex", args);
    QString entry = result.toString();
    
    return entry;
}

QJsonDocument PythonAdapter::interpreter(QString command)
{
    PythonQtObjectPtr context = PythonQt::self()->getMainModule();
    context.evalFile("./python_adapter.py");
    QVariantList args;
    args << command;
    qDebug() << "ARGS: " << args;
    QVariant result = context.call("interpreter", args);
//     qDebug() << "RESULT: " << result;
    
    QString result_str = result.toString();
    QJsonDocument jdoc = QJsonDocument::fromJson(result_str.toUtf8());
    
    return jdoc;
}
