
#ifndef PYTHON_ADAPTER
#define PYTHON_ADAPTER

#include <QObject>
#include <QJsonDocument>
#include <QVariantList>

class PythonAdapter : public QObject
{
    Q_OBJECT
    
public:
    PythonAdapter(QObject *parent = 0);
    
    int getHistorySize();
    void historyWrite(QString);
    QString historyReadWithIndexAndPrefix(int, QString);
    QString historyReadAtIndex(int);
    
    QJsonDocument interpreter(QString);
};

#endif
