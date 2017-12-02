
#include <cli_widget.h>

#include <QTableWidget>
#include <QTextEdit>
#include <QGridLayout>
#include <QLineEdit>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonValue>
#include <QJsonArray>

#include <QDebug>

#include <PythonQt.h>
#include <PythonQt_QtAll.h>

QCliWidget::QCliWidget(QWidget *parent)
    : grid(new QGridLayout)
    , input_line(new QInputLine)
{
    grid->setContentsMargins(0, 0, 0, 0);
    setLayout(grid);
    
    input_line->setPlaceholderText("This is the command line. See 'man commandline' for details.");
//     connect(input_line, &QLineEdit::returnPressed, this, &QCliWidget::commandEntered);
    connect(input_line, SIGNAL(returnPressed(QString)), this, SLOT(commandEntered(QString)));
    grid->addWidget(input_line, 1, 0);
    
//     PythonQt::init(PythonQt::IgnoreSiteModule);
//     PythonQt::init();
    PythonQt::init(PythonQt::ExternalHelp);
    
    /*
    QString my_array[3][4] = {
        {"a", "b", "c", "d"} ,
        {"e", "f", "g", "h"} ,
        {"i", "j", "k", "l"}
    };
    QList<int> list_a({1, 2});
//     QList<int><int> list_b({1, 2},{3,4});
    QVector<QStringList> matrix{{"foo", "bar", "baz"}, {"hello", "world", "!"}};
    matrix[1].append("bla");
    matrix[0].append("blubb");
    matrix.append(QStringList {"blaha"});
    */
//     resultInTable(matrix);
//     connectToPython();
}

void QCliWidget::commandEntered(QString command)
{
    qDebug() << command;
    
    PythonQtObjectPtr context = PythonQt::self()->getMainModule();
    context.evalFile("./lib_tambi_interpreter.py");
    
    QVariantList args;
//     args << "bituza 1mose 1 1";
    args << command;
    QVariant result = context.call("interpreter", args);
    
    QString result_str = result.toString();
    QJsonDocument jdoc = QJsonDocument::fromJson(result_str.toUtf8());
    QJsonObject obj;
    
    if (!jdoc.isNull())
    {
        if (jdoc.isObject())
        {
            obj = jdoc.object();
        }
        else
        {
            qDebug() << "Document is not an object";
        }
    }
    else
    {
        qDebug() << "Invalid JSON";
    }
    
//     qDebug() << obj;
    qDebug() << obj["payload"];
    
    QString obj_cat = obj["category"].toString().toUtf8();
    
    if (obj_cat == "text")
    {
        QJsonArray arr = obj["payload"].toArray();
        QString payload = "";
        
        for (int i = 0; i < arr.size(); i++)
        {
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
        
        resultInTextEdit(payload);
    }
    else if (obj_cat == "table")
    {
        QJsonArray arr = obj["payload"].toArray();
        QVector<QStringList> matrix;
        for (int i = 0; i < arr.size(); i++)
        {
            QStringList line;
            for (int j = 0; j < arr[i].toArray().size(); j++)
            {
                QJsonValue val = arr[i].toArray().takeAt(j);
                line.append(val.toString());
            }
            matrix.append(line);
        }
        resultInTable(matrix);
    }
    
}

void QCliWidget::addDisplayWidget()
{
    
}

void QCliWidget::resultInTextEdit(QString text)
{
    QTextEdit *text_edit = new QTextEdit();
    text_edit->setText(text);
    grid->addWidget(text_edit, 0, 0, 1, 0);
}

void QCliWidget::resultInTable(QVector<QStringList> matrix)
{
    QTableWidget *table = new QTableWidget();
    table->setRowCount(matrix.length());
    table->setColumnCount(getMatrixMaxWidth(matrix));
    
    /* for (auto& rows: matrix) */
    for (int i=0; i < matrix.length(); i++)
    {
        for (int j=0; j < matrix[i].length(); j++)
        {
            QTableWidgetItem *table_item = new QTableWidgetItem(matrix[i][j]);
            table->setItem(i, j, table_item);
        }
    }
    table->resizeColumnsToContents();
    grid->addWidget(table, 0, 0, 1, 0);
}

int QCliWidget::getMatrixMaxWidth(QVector<QStringList> matrix)
{
    int max = 0;
    
    for (int i=0; i < matrix.length(); i++)
    {
        if (matrix[i].length() > max)
        {
            max = matrix[i].length();
        }
    }
    
    return max;
}

void QCliWidget::connectToPython()
{
    // init PythonQt and Python itself
    PythonQt::init();
    // enable the Qt-bindings for PythonQt
    PythonQt_QtAll::init();
    
    // get a smart pointer to the __main__ module of the Python interpreter
    PythonQtObjectPtr context = PythonQt::self()->getMainModule();
    
    // do something
    /*
    context.evalScript("def multiply(a,b):\n  return a*b;\n");
    QVariantList args;
    args << 42 << 47;
    QVariant result = context.call("multiply", args);
    qDebug() << result;
    */
    
    /*
    context.evalScript("def say():\n    return 'hallo';\n");
    QVariantList args;
    QVariant result = context.call("say", args);
    qDebug() << result;
    */
    
// //     qDebug() << context.evalScript("return 'hallo'");
// //     QVariantList args;
// //     QVariant result = context.call();
// //     qDebug() << result;
    
    
//     context.evalFile(":/Test.py");
    context.evalFile("./Test.py");
    QVariantList args;
    QVariant result = context.call("say", args);
    qDebug() << result;
    
    
    /*
    QFile file(":/Test.py");
    char *data;
    file.readLine(*data);
    */
}
