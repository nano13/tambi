
#include <cli_widget.h>
#include <format_output.h>
#include <qitemizedwidget.h>

#include <unicode_fonts.h>

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

#include <QStandardPaths>
#include <QDir>

#include <QFileDialog>

#include <QDebug>

#include <PythonQt.h>
#include <PythonQt_QtAll.h>

#include <tts_interface.h>

QCliWidget::QCliWidget(QWidget *parent)
    : grid(new QGridLayout)
    , input_line(new QInputLine)
    , old_display_widget(new QWidget)
    , view(new QGraphicsView)
    , scene(new QGraphicsScene)
    , unicodeFonts(new UnicodeFonts)
{
    grid->setContentsMargins(0, 0, 0, 6);
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
}

void QCliWidget::commandEntered(QString command)
{
    emit setTabText(command);
    TTSInterface *tts = new TTSInterface();
    tts->speak(command);
    
    qDebug() << command;
    resize(this_x, this_y);
    
    HandleCommandThread *interpreter_thread = new HandleCommandThread();
    interpreter_thread->setCommand(command);
    
    connect(interpreter_thread, &HandleCommandThread::processResult, this, &QCliWidget::processResult);
    
    interpreter_thread->start();
}

void QCliWidget::processResult(QJsonDocument jdoc)
{
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
//     qDebug() << obj["payload"];
    
    QString exception = obj["exception"].toString().toUtf8();
    if (exception == "clear")
    {
        clearDisplayWidget();
    }
    else if (exception == "snapshot")
    {
        makeSnapshot();
    }
    
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
        QString payload = FormatOutput::formatText(obj);
        resultInTextEdit(payload);
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
        QVector<QStringList> matrix = FormatOutput::formatTable(obj);
        resultInItemizedWidget(matrix);
    }
    else if (obj_cat == "bloodline")
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
    scene->clear();
    
    scene->addWidget(display_widget);
    view->setScene(scene);
    view->setStyleSheet("QGraphicsView { border-style: none; }");
    
    old_display_widget = display_widget;
    grid->addWidget(view, 0, 0, 1, 0);
    resizeDisplayWidget();
    
    this->display_widget = display_widget;
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

void QCliWidget::clearDisplayWidget()
{
    QWidget *empty_widget = new QWidget();
    addDisplayWidget(empty_widget);
}

void QCliWidget::makeSnapshot()
{
    QImage *image = new QImage(this->display_widget->size(), QImage::Format_ARGB32);
    QPainter *painter = new QPainter(image);
    
    if (painter->isActive())
    {
        render(painter);
    }
    painter->end();
    
    QString default_dir = QDir::homePath();
    
    QFileDialog *dialog = new QFileDialog;
    QString filename = dialog->getSaveFileName(this, "Save Snapshot", default_dir);
    
    image->save(filename);
}

void QCliWidget::resultInTextEdit(QString text)
{
    QTextEdit *text_edit = new QTextEdit();
//     qDebug() << unicodeFonts->getAvailableFonts("");
    QFont font = unicodeFonts->getFontAndSize(text);
    text_edit->setFont(font);
    
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
    
    // table->setHorizontalHeaderLabels(result.header);
    // table->setVerticalHeaderLabels(result.header_left);
    
    for (int i=0; i < matrix.length(); i++)
    {
        for (int j=0; j < matrix[i].length(); j++)
        {
            QString item = matrix[i][j];
            QTableWidgetItem *table_item = new QTableWidgetItem(item);
            
//             QFont font = unicodeFonts->getFontAndSize(item);
//             table_item->setFont(font);
            
            table->setItem(i, j, table_item);
        }
    }
    table->resizeColumnsToContents();
    
    addDisplayWidget(table);
}

void QCliWidget::resultInMultimediaTable(QVector<QStringList> matrix)
{
    
}

void QCliWidget::resultInItemizedWidget(QVector<QStringList> payload)
{
    QItemizedWidget *itemizedWidget = new QItemizedWidget();
    itemizedWidget->showData(payload);
    addDisplayWidget(itemizedWidget);
}

void QCliWidget::resultInImageWidget()
{
    
}

void QCliWidget::resultInDiagram()
{
    
}

void QCliWidget::showErrorMessage()
{
    
}

bool isImage()
{
    
}

bool isAudio()
{
    
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


HandleCommandThread::HandleCommandThread(QThread *parent)
{
    PythonAdapter *py_adapt = new PythonAdapter();
}

void HandleCommandThread::setCommand(QString command)
{
    this->command = command;
}

void HandleCommandThread::run()
{
    QJsonDocument jdoc = py_adapt->interpreter(command);
    qDebug() << jdoc;
    emit processResult(jdoc);
}
