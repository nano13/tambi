
#include <cli_widget.h>
#include <format_output.h>

#include <QTableWidget>
#include <QTextEdit>
#include <QGridLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QIcon>

#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonValue>
#include <QJsonArray>

#include <QGraphicsView>
#include <QGraphicsScene>

#include <QDebug>

#include <PythonQt.h>
#include <PythonQt_QtAll.h>

QCliWidget::QCliWidget(QWidget *parent)
    : grid(new QGridLayout)
    , input_line(new QInputLine)
    , old_display_widget(new QWidget)
    , view(new QGraphicsView)
    , scene(new QGraphicsScene)
{
    grid->setContentsMargins(0, 0, 0, 0);
    setLayout(grid);
    
    QTextEdit *text_edit = new QTextEdit();
    text_edit->setText("type in the command 'man' down there in the command line for getting started ...");
    text_edit->setReadOnly(true);
    addDisplayWidget(text_edit);
    
    input_line->setPlaceholderText("This is the command line. See 'man commandline' for details.");
    connect(input_line, SIGNAL(returnPressed(QString)), this, SLOT(commandEntered(QString)));
    grid->addWidget(input_line, 1, 0);
    
    QPushButton *zoomOutButton = new QPushButton();
    zoomOutButton->setIcon(QIcon::fromTheme("zoom-out"));
    connect(zoomOutButton, &QPushButton::clicked, this, &QCliWidget::onZoomOutClicked);
    grid->addWidget(zoomOutButton, 1, 2);
    
    QPushButton *zoomResetButton = new QPushButton();
    zoomResetButton->setIcon(QIcon::fromTheme("zoom-original"));
    connect(zoomResetButton, &QPushButton::clicked, this, &QCliWidget::onZoomResetClicked);
    grid->addWidget(zoomResetButton, 1, 3);
    
    QPushButton *zoomInButton = new QPushButton();
    zoomInButton->setIcon(QIcon::fromTheme("zoom-in"));
    connect(zoomInButton, &QPushButton::clicked, this, &QCliWidget::onZoomInClicked);
    grid->addWidget(zoomInButton, 1, 4);
    
    
    
//     PythonQt::init(PythonQt::IgnoreSiteModule);
//     PythonQt::init();
//     PythonQt::init(PythonQt::ExternalHelp);
    
    /*
    QVector<QStringList> matrix{{"foo", "bar", "baz"}, {"hello", "world", "!"}};
    matrix[1].append("bla");
    matrix[0].append("blubb");
    matrix.append(QStringList {"blaha"});
    */
}

void QCliWidget::commandEntered(QString command)
{
//     qDebug() << command;
    resize(this_x, this_y);
    
    PythonQtObjectPtr context = PythonQt::self()->getMainModule();
    context.evalFile("./lib_tambi_interpreter.py");
    QVariantList args;
    args << command;
    qDebug() << "ARGS: " << args;
    QVariant result = context.call("interpreter", args);
    qDebug() << "RESULT: " << result;
    
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
    
    qDebug() << obj;
    qDebug() << obj["payload"];
    
    QString obj_cat = obj["category"].toString().toUtf8();
    
    if (obj_cat == "table")
    {
        QVector<QStringList> matrix = FormatOutput::formatTable(obj);
        resultInTable(matrix);
    }
    
    else if (obj_cat == "multimedia_table")
    {
        
    }
    
    else if (obj_cat == "list")
    {
        
    }
    
    else if (obj_cat == "text")
    {
        QString payload = FormatOutput::formatText(obj);
        resultInTextEdit(payload);
    }
    
    else if (obj_cat == "string" || obj_cat == "html")
    {
        QString payload = FormatOutput::formatString(obj);
        resultInTextEdit(payload);
    }
    
    else if (obj_cat == "itemized")
    {
        
    }
    
    else if (obj_cat == "image")
    {
        
    }
    
    else if (obj_cat == "diagram")
    {
        
    }
    
    else if (obj_cat == "command")
    {
        
    }
}

void QCliWidget::addDisplayWidget(QWidget *display_widget)
{
    old_display_widget->deleteLater();
    
    scene->addWidget(display_widget);
    view->setScene(scene);
    view->setStyleSheet("QGraphicsView { border-style: none; }");
    
    old_display_widget = display_widget;
    grid->addWidget(view, 0, 0, 1, 0);
    resizeDisplayWidget();
}

void QCliWidget::resizeDisplayWidget()
{
    // the magick numbers are for keeping the size of the view allways small enough not to spawn an outer set of scrollbars:
    int x = view->width() - 2.1;
    int y = view->height() - 2.1;
    this_x = x;
    this_y = y;
    
    QRectF mapped_rect = view->mapToScene(QRect(0, 0, x, y)).boundingRect();
    old_display_widget->setFixedSize(mapped_rect.width(), mapped_rect.height());
    scene->setSceneRect(0, 0, mapped_rect.width(), mapped_rect.height());
}

void QCliWidget::resizeEvent(QResizeEvent *event)
{
    resizeDisplayWidget();
}

void QCliWidget::resultInTextEdit(QString text)
{
    QTextEdit *text_edit = new QTextEdit();
    text_edit->setText(text);
    text_edit->setReadOnly(true);
    text_edit->setAcceptRichText(true);
    
    addDisplayWidget(text_edit);
}

void QCliWidget::resultInTable(QVector<QStringList> matrix)
{
    QTableWidget *table = new QTableWidget();
    table->setRowCount(matrix.length());
    table->setColumnCount(getMatrixMaxWidth(matrix));
    
    for (int i=0; i < matrix.length(); i++)
    {
        for (int j=0; j < matrix[i].length(); j++)
        {
            QTableWidgetItem *table_item = new QTableWidgetItem(matrix[i][j]);
            table->setItem(i, j, table_item);
        }
    }
    table->resizeColumnsToContents();
    
    addDisplayWidget(table);
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

void QCliWidget::onZoomInClicked()
{
    view->scale(SCALE_FACTOR, SCALE_FACTOR);
    resizeDisplayWidget();
}

void QCliWidget::onZoomOutClicked()
{
    view->scale(1 / SCALE_FACTOR, 1 / SCALE_FACTOR);
    resizeDisplayWidget();
}

void QCliWidget::onZoomResetClicked()
{
    view->resetTransform();
    resizeDisplayWidget();
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
