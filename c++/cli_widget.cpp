
#include <cli_widget.h>

#include <QTableWidget>
#include <QGridLayout>
#include <QPushButton>

#include <QDebug>

#include <PythonQt.h>
#include <PythonQt_QtAll.h>

QCliWidget::QCliWidget(QWidget *parent)
    : grid(new QGridLayout)
{
    grid->setContentsMargins(0, 0, 0, 0);
    setLayout(grid);
    
    //qDebug() << "TEST";
    
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
    
//     qDebug() << matrix;
    
    resultInTable(matrix);
    connectToPython();
}

void QCliWidget::commandEntered(QString command)
{
    
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
    
    
    context.evalFile(":/Test.py");
    QVariantList args;
    QVariant result = context.call("say", args);
    qDebug() << result;
    
    
    /*
    QFile file(":/Test.py");
    char *data;
    file.readLine(*data);
    */
}
