
#include <QWidget>
#include <QVBoxLayout>
#include <QScrollArea>
#include <QTextEdit>
#include <QVector>
#include <QStringList>

#include <qtambi_widgets/unicode_fonts.h>

class QItemizedWidget : public QWidget
{
    Q_OBJECT
    
public:
    QItemizedWidget(QWidget *parent = 0);
    void showData(QVector<QStringList> payload);
    
private:
    QVBoxLayout *layout;
    QVBoxLayout *vLayout;
    QScrollArea *scroll;
};

class QItemWidget : public QWidget
{
    Q_OBJECT
    
public:
    QItemWidget(QWidget *parent = 0);
    void showData(QStringList);
    
private:
    QVBoxLayout *layout;
    UnicodeFonts *unicodeFonts;
};

class QGrowingTextEdit : public QTextEdit
{
    Q_OBJECT
    
public:
    QGrowingTextEdit(QTextEdit *parent = 0);
    
    void resizeEvent(QResizeEvent *event);
    
private:
    int heightMin = 0;
    int heightMax = 65000;
    
private slots:
    void sizeChanged();
};
