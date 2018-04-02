
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
    
    buildTree();
    traverseTreeForCoevalNodes();
    resolveCollisions();
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
    
    scene->addItem(guy);
}

void QTimelineDiagramWidget::buildTree()
{
    // get the size of the guy
    QGraphicsGuyItem *guy = new QGraphicsGuyItem();
    int guy_width = guy->boundingRect().width();
    int guy_height = guy->boundingRect().height();
    
    QList<QGraphicsItem*> items = scene->items(Qt::AscendingOrder);
    
    // the data has to be preordered!
    // assuming here that the first element is the root-item (or the leftmost to be shown)!
    root_item = items.takeFirst();
    QGraphicsGuyItem *root = qgraphicsitem_cast<QGraphicsGuyItem*>(root_item);
    root_item->setPos(0, 0);
    
    // now we search the whole tree for successor-elements of the root
    //foreach (QGraphicsItem *guy_item, items)
    //for (int i = 0; i < items.length(); ++i)
    while (items.length() > 0)
    {
        bool taken = false;
        for (int j = 0; j < items.length(); ++j)
        {
            QGraphicsItem* guy_item = items.at(j);
            QGraphicsGuyItem* guy = qgraphicsitem_cast<QGraphicsGuyItem*>(guy_item);
            
            bool found = traverseTreeForMatchingNode(root, guy->predecessor());
            if (found)
            {
                guy->setParentItem(found_guy);
                items.removeAt(j);
                guy->setPos(guy_width, 0);
                taken = true;
                
                //drawPredecessionLine(found_guy, guy);
            }
        }
        
        // if none items have a parent in the tree,
        // we reparent the first one to our root element
        // in order to get the items-list emptied never the less
        if (!taken)
        {
            QGraphicsItem *guy_item = items.takeFirst();
            guy_item->setParentItem(root);
            
            guy_item->setPos(guy_width, 100);
        }
    }
}

// DFS for node with given id (iterative implementation)
bool QTimelineDiagramWidget::traverseTreeForMatchingNode(QGraphicsItem* node, QString id)
{
    QStack<QGraphicsItem*> stack;
    stack.push(node);
    
    while (!stack.isEmpty())
    {
        QGraphicsItem* node = stack.pop();
        if (node->type() == QGraphicsItem::UserType + 1) // QGraphicsGuyItem
        {
            QGraphicsGuyItem *guy_node = qgraphicsitem_cast<QGraphicsGuyItem*>(node);
            if (guy_node->id() == id)
            {
                this->found_guy = node;
                return true;
            }
            else
            {
                foreach (QGraphicsItem* guy, node->childItems()) {
                    stack.push(guy);
                }
            }
        }
    }
    
    return false;
}

void QTimelineDiagramWidget::traverseTreeForCoevalNodes()
{
    
}

// traverse tree with dfs for detecting and fixing collisions
void QTimelineDiagramWidget::resolveCollisions()
{
    // get the size of the guy
    QGraphicsGuyItem *guy = new QGraphicsGuyItem();
    int guy_width = guy->boundingRect().width();
    int guy_height = guy->boundingRect().height();
    
    bool once_again = true;
    while (once_again)
    {
        once_again = false; // unless we set this true later ...
        
        // set up for bfs
        QList<QString> visited_items_ids;
        QList<QGraphicsItem*> items_to_visit; // to be used as a queue
        items_to_visit.append(root_item);
        
        QGraphicsGuyItem *root_guy = qgraphicsitem_cast<QGraphicsGuyItem*>(root_item);
        visited_items_ids.append(root_guy->id());
        
        while (! items_to_visit.isEmpty())
        {
            QGraphicsItem* node = items_to_visit.takeLast();
            QGraphicsGuyItem *guy_node = qgraphicsitem_cast<QGraphicsGuyItem*>(node);
            
            // detect for collision for the current node
            QGraphicsItem *gitem = scene->itemAt(node->scenePos(), QTransform());
            if (gitem != 0)
            {
                QGraphicsGuyItem *gitem_guy = qgraphicsitem_cast<QGraphicsGuyItem*>(gitem);
                if (gitem_guy->id() != guy_node->id())
                {
                    QPointF position = node->pos();
                    position.setY(position.y() + 10+guy_height);
                    node->setPos(position);
                    
                    // if we have moved an item, we have to run a sort-iteration again
                    once_again = true;
                }
            }
            
            // append child items to the queue items_to_visit (part of BFS)
            foreach (QGraphicsItem* child, node->childItems())
            {
                QGraphicsGuyItem *child_guy = qgraphicsitem_cast<QGraphicsGuyItem*>(child);
                if (visited_items_ids.indexOf(child_guy->id()) == -1)
                {
                    items_to_visit.append(child);
                    visited_items_ids.append(child_guy->id());
                }
            }
        }
    }
}

void QTimelineDiagramWidget::drawPredecessionLine(QGraphicsItem* parent, QGraphicsItem* child)
{
    qDebug() << "";
    
    QPointF start = parent->mapToScene(parent->pos());
    QPointF end = child->mapToScene(child->pos());
    
    qDebug() << start;
    qDebug() << end;
    
    QLineF line = QLineF(start, end);
    //QGraphicsLineItem* line_item = scene->addLine(line);
    
    //line_item->setParentItem(parent);
}
