
#include <QWidget>
#include <QGridLayout>
#include <QVector>
#include <QStringList>

class QCliWidget : public QWidget
{
    Q_OBJECT
    
public:
    QCliWidget(QWidget *parent = 0);
    
private:
    QGridLayout *grid;
    
    int getMatrixMaxWidth(QVector<QStringList>);
    void connectToPython();
    
private slots:
    void commandEntered(QString);
    void resultInTable(QVector<QStringList>);
};
