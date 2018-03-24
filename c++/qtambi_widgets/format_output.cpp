
#include <qtambi_widgets/format_output.h>

#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonValue>
#include <QJsonArray>

#include <QDebug>

FormatOutput::FormatOutput(QObject *parent)
{
    
}

QString FormatOutput::formatText(QJsonObject obj)
{
    QString payload = "";
    
    if (obj["payload"].isArray())
    {
        QJsonArray arr = obj["payload"].toArray();
        
        for (int i = 0; i < arr.size(); i++)
        {
            int arr_size = arr[i].toArray().size();
            if (arr_size > 0) {
                QString line_part = "";
                for (int j = 0; j < arr[i].toArray().size(); j++)
                {
    //              line_part.append(arr[i].toArray().takeAt(j).toString());
                    QJsonValue val = arr[i].toArray().takeAt(j);
                    if (val.isString())
                    {
                        line_part.append(val.toString());
                    }
                    else if (val.isDouble())
                    {
                        double dou = val.toDouble();
                        line_part.append(QString::number(dou));
                        line_part.append(" | ");
                    }
                }
                payload.append(line_part);
                payload.append("\n");
            }
            else
            {
                payload.append(arr[i].toString());
                payload.append("\n");
            }
        }
    }
    else if (obj["payload"].isString())
    {
        payload = obj["payload"].toString();
    }
    
    return payload;
}

QString FormatOutput::formatString(QJsonObject obj)
{
    QString payload = obj["payload"].toString();
    return payload;
}

QVector<QStringList> FormatOutput::formatTable(QJsonObject obj)
{
    QJsonArray arr = obj["payload"].toArray();
    QVector<QStringList> matrix;
    for (int i = 0; i < arr.size(); i++)
    {
        QStringList line;
        for (int j = 0; j < arr[i].toArray().size(); j++)
        {
            QJsonValue val = arr[i].toArray().takeAt(j);
            if (val.isString())
            {
                line.append(val.toString());
            }
            else if (val.isDouble())
            {
                double dou = val.toDouble();
                line.append(QString::number(dou));
            }
        }
        matrix.append(line);
    }
    
    return matrix;
}
