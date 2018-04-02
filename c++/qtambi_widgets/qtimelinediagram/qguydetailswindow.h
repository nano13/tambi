
#include <QMainWindow>
#include <QWidget>
#include <QVBoxLayout>
#include <QLineEdit>

class QGuyDetailsWindow : public QMainWindow
{
    Q_OBJECT
    
public:
    QGuyDetailsWindow(QMainWindow *parent = 0);
    
    enum Role { king, king_north, king_south, prophet, prophet_north, prophet_south };
    enum Sex { male, female };

    
private:
    QLineEdit *_id; // [A-Z]*_[0-9]*
    Role _role;
    QLineEdit *_name;
    QLineEdit *_name_original; // greek or hebrew
    QLineEdit *_name_meaning;
    Sex _sex;
    int _age_death;
    int _age_firstson;
    QList<QString> _coevals; // id's of other entities
    QList<QString> _bible_refs;
    bool good_start;
    bool good_end;
    QString _description; // some human-readable infos about this guy
    QString _predecessor; // id's of other entities
    QString _successor; // id's of other entities
    
public:
    void setID(QString);
    void setRole(Role);
    void setNames(QString, QString, QString);
    void setSex(Sex);
    void setAgeDeath(int);
    void setAgeFirstSon(int);
    void setCoevals(QList<QString>);
    void setBibleRefs(QList<QString>);
    void setGoodness(bool, bool);
    void setDescription(QString);
    void setPredecessor(QString);
    void setSuccessor(QString);
    
    QString id();
    Role role();
    QList<QString> names();
    Sex sex();
    int ageDeath();
    int ageFirstSon();
    QList<QString> coevals();
    QList<QString> bibleRefs();
    QList<bool> goodness();
    QString description();
    QString predecessor();
    QString successor();
    
private slots:
    
    
};
