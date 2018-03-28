
#include <qtambi_widgets/qtimelinediagram/qtimelinediagramwidget.h>

QTimelineDiagramWidget::QTimelineDiagramWidget (QJsonArray data, QWidget *parent)
    : QWidget (parent)
    , view (new QGraphicsView)
    , scene (new QGraphicsScene)
    , layout (new QVBoxLayout)
{
    view->setScene(scene);
    
    layout->setContentsMargins(0, 0, 0, 0);
    layout->addWidget(view);
    setLayout(layout);

    foreach (QJsonValue guy_val, data) {
        QJsonObject guy_obj = guy_val.toObject();
        addGuyItem(guy_obj);
    }

    searchFurkationsAndConfluences();
    sortGuys();
}

void QTimelineDiagramWidget::addGuyItem(QJsonObject guy_obj)
{
    QGraphicsGuyItem *guy = new QGraphicsGuyItem();

    // converting QString to Enum
    QString role_string = guy_obj.value("role").toString();
    QGraphicsGuyItem::Role role_enum;
    if (role_string == "king") role_enum = QGraphicsGuyItem::Role::king;
    if (role_string == "king_north") role_enum = QGraphicsGuyItem::Role::king_north;
    if (role_string == "king_south") role_enum = QGraphicsGuyItem::Role::king_south;
    if (role_string == "prophet") role_enum = QGraphicsGuyItem::Role::prophet;
    if (role_string == "prophet_north") role_enum = QGraphicsGuyItem::Role::prophet_north;
    if (role_string == "prophet_south") role_enum = QGraphicsGuyItem::Role::prophet_south;

    // converting QString to Enum
    QString sex_string = guy_obj.value("sex").toString();
    QGraphicsGuyItem::Sex sex_enum = (sex_string == "male") ? QGraphicsGuyItem::Sex::male : QGraphicsGuyItem::Sex::female;

    // converting QJsonArray to QList<QString>
    QJsonArray coevals_array = guy_obj.value("coevals").toArray();
    QList<QString> coevals_list;
    foreach (QJsonValue coeval, coevals_array)
    {
        coevals_list.append(coeval.toString());
    }

    // converting QJsonArray to QList<QString>
    QJsonArray refs_array = guy_obj.value("bible_refs").toArray();
    QList<QString> refs_list;
    foreach (QJsonValue ref, refs_array)
    {
        refs_list.append(ref.toString());
    }

    guy->setID(guy_obj.value("id").toString());
    guy->setRole(role_enum);
    guy->setNames(guy_obj.value("name_de").toString(),
                  guy_obj.value("name_original").toString(),
                  guy_obj.value("name_meaning").toString());
    guy->setSex(sex_enum);
    guy->setAgeDeath(guy_obj.value("age_death").toInt());
    guy->setAgeFirstSon(guy_obj.value("age_first_son").toInt());
    guy->setCoevals(coevals_list);
    guy->setBibleRefs(refs_list);
    guy->setGoodness(guy_obj.value("good_start").toBool(),
                     guy_obj.value("good_end").toBool());
    guy->setDescription(guy_obj.value("description").toString());
    guy->setPredecessor(guy_obj.value("predecessor").toString());
    guy->setSuccessor(guy_obj.value("successor").toString());

    //guy->setPos(pos);
    scene->addItem(guy);
}

void QTimelineDiagramWidget::searchFurkationsAndConfluences()
{
    QList<QGraphicsItem*> items = scene->items();
    foreach (QGraphicsItem* guy, items)
    {
        QGraphicsGuyItem *a = qgraphicsitem_cast<QGraphicsGuyItem*>(guy);
        foreach (QGraphicsItem* another_guy, items)
        {
            QGraphicsGuyItem *b = qgraphicsitem_cast<QGraphicsGuyItem*>(another_guy);

            if (a->id() != b->id())
            {
                qDebug() << "iurtneiartniatreniartnuiarten";
            }
        }
    }
}

void QTimelineDiagramWidget::sortGuys()
{

}


