
#include <qitemizedwidget.h>

#include <QTimer>

#include <QDebug>

QItemizedWidget::QItemizedWidget(QWidget *parent)
    // layout of container widget
    : layout(new QVBoxLayout)
    , vLayout(new QVBoxLayout)
    , scroll(new QScrollArea)
{
    // container widget
    QWidget *widget = new QWidget();
    widget->setLayout(layout);
    layout->setContentsMargins(0, 0, 0, 0);
    
    // scroll area properties
    scroll->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    scroll->setWidgetResizable(true);
    scroll->setWidget(widget);
    
    // scroll area layer add
    vLayout->addWidget(scroll);
    setLayout(vLayout);
}

void QItemizedWidget::showData(QVector<QStringList> payload)
{
    for (int i=0; i < payload.length(); i++)
    {
        QItemWidget *itemWidget = new QItemWidget();
        QStringList line = payload.at(i);
        itemWidget->showData(line);
        layout->addWidget(itemWidget);
    }
}


// new class
QItemWidget::QItemWidget(QWidget *parent)
    : layout(new QVBoxLayout)
{
    layout->setSpacing(0);
    setLayout(layout);
}

void QItemWidget::showData(QStringList line)
{
    for (int i=0; i < line.length(); i++)
    {
        QString column = line.at(i);
        QGrowingTextEdit *textEdit = new QGrowingTextEdit();
        // TODO: unicode fonts
        
        textEdit->setText(column);
//         textEdit->setReadOnly(true);
        layout->addWidget(textEdit);
    }
}

// new class
QGrowingTextEdit::QGrowingTextEdit(QTextEdit *parent)
{
    QTextDocument *doc = document();
    
    connect(doc, SIGNAL(contentsChanged()), this, SLOT(sizeChanged()));
    connect(this, SIGNAL(cursorPositionChanged()), this, SLOT(sizeChanged()));
    connect(this, SIGNAL(textChanged()), this, SLOT(sizeChanged()));
//     connect(this, SIGNAL(resize()), this, SLOT(sizeChanged));
    
    QTimer::singleShot(1, this, SLOT(sizeChanged()));
}

void QGrowingTextEdit::resizeEvent(QResizeEvent *event)
{
    sizeChanged();
    QTextEdit::resizeEvent(event);
}

void QGrowingTextEdit::sizeChanged()
{
    QTextDocument *docu = document();
    qreal docHeight = docu->size().height();
    
    if ((heightMin <= docHeight) <= heightMax)
    {
        setMinimumHeight(docHeight + 2);
    }
}
