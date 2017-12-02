
#include <QWidget>
#include <QGridLayout>
#include <QLineEdit>
#include <QVector>
#include <QStringList>

#include <QInputLine.h>

class QCliWidget : public QWidget
{
    Q_OBJECT
    
public:
    QCliWidget(QWidget *parent = 0);
    
private:
    QGridLayout *grid;
    QInputLine *input_line;
    
    int getMatrixMaxWidth(QVector<QStringList>);
    void connectToPython();
    
private slots:
    void commandEntered(QString);
    void resultInTextEdit(QString);
    void resultInTable(QVector<QStringList>);
};
