
#include <QObject>

#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonValue>
#include <QJsonArray>

#include <QVector>

class FormatOutput : public QObject
{
    Q_OBJECT
    
public:
    FormatOutput(QObject *parent = 0);
    
    static QString formatText(QJsonObject);
    static QString formatString(QJsonObject);
    static QVector<QStringList> formatTable(QJsonObject);
};
