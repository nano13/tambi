
#include <QLineEdit>

#include <PythonQt.h>

class QInputLine : public QLineEdit
{
    Q_OBJECT
    
public:
    QInputLine(QLineEdit *parent = 0);
    
private:
    int history_counter = 0;
    QString search_pattern_prefix = "";
    PythonQtObjectPtr context;
    
    void appendText(QString);
    
private slots:
    
signals:
    void returnPressed(QString);
    
protected:
    void keyPressEvent(QKeyEvent *event);
};
