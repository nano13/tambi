
#include <qtambi_widgets/qtimelinediagram/qguydetailswindow.h>

QGuyDetailsWindow::QGuyDetailsWindow(QMainWindow *parent)
    : _id (new QLineEdit)
    , _name (new QLineEdit)
    , _name_original (new QLineEdit)
    , _name_meaning (new QLineEdit)
{
    resize(200, 200);
    
    QWidget *central_widget = new QWidget();
    setCentralWidget(central_widget);
    
    QLayout *layout = new QVBoxLayout();
    central_widget->setLayout(layout);
    
    layout->addWidget(_id);
    
    layout->addWidget(_name);
    layout->addWidget(_name_original);
    layout->addWidget(_name_meaning);
    
    
}

void QGuyDetailsWindow::setID(QString id)
{
    this->_id->setText(id);
}

void QGuyDetailsWindow::setRole(Role role)
{
    this->_role = role;
}

void QGuyDetailsWindow::setNames(QString name, QString name_original, QString name_meaning)
{
    this->_name->setText(name);
    this->_name_original->setText(name_original);
    this->_name_meaning->setText(name_meaning);
    
    setWindowTitle("guy details: " + name);
}

void QGuyDetailsWindow::setSex(Sex sex)
{
    this->_sex = sex;
}

void QGuyDetailsWindow::setAgeDeath(int age_death)
{
    this->_age_death = age_death;
}

void QGuyDetailsWindow::setAgeFirstSon(int age_firstson)
{
    this->_age_firstson = age_firstson;
}

void QGuyDetailsWindow::setCoevals(QList<QString> coevals)
{
    this->_coevals = coevals;
}

void QGuyDetailsWindow::setBibleRefs(QList<QString> bible_refs)
{
    this->_bible_refs = bible_refs;
}

void QGuyDetailsWindow::setGoodness(bool good_start, bool good_end)
{
    this->good_start = good_start;
    this->good_end = good_end;
}

void QGuyDetailsWindow::setDescription(QString description)
{
    this->_description = description;
}

void QGuyDetailsWindow::setPredecessor(QString predecessor)
{
    this->_predecessor = predecessor;
}

void QGuyDetailsWindow::setSuccessor(QString successor)
{
    this->_successor = successor;
}

QString QGuyDetailsWindow::id()
{
    return _id->text();
}
QGuyDetailsWindow::Role QGuyDetailsWindow::role()
{
    return _role;
}
QList<QString> QGuyDetailsWindow::names()
{
    QList<QString> ret_list;
    ret_list << _name->text() << _name_original->text() << _name_meaning->text();
    return ret_list;
}
QGuyDetailsWindow::Sex QGuyDetailsWindow::sex()
{
    return _sex;
}
int QGuyDetailsWindow::ageDeath()
{
    return _age_death;
}
int QGuyDetailsWindow::ageFirstSon()
{
    return _age_firstson;
}
QList<QString> QGuyDetailsWindow::coevals()
{
    return _coevals;
}
QList<QString> QGuyDetailsWindow::bibleRefs()
{
    return _bible_refs;
}
QList<bool> QGuyDetailsWindow::goodness()
{
    QList<bool> ret_list;
    ret_list << good_start << good_end;
    return ret_list;
}
QString QGuyDetailsWindow::description()
{
    return _description;
}
QString QGuyDetailsWindow::predecessor()
{
    return _predecessor;
}
QString QGuyDetailsWindow::successor()
{
    return _successor;
}
