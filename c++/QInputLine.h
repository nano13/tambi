
#include <QLineEdit>

class QInputLine : public QLineEdit
{
    Q_OBJECT
    
public:
    QInputLine(QLineEdit *parent = 0);
    
private:
    void appendText(QString);
    
private slots:
    
signals:
    void returnPressed(QString);
    
protected:
    void keyPressEvent(QKeyEvent *event);
};
