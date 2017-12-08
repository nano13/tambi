
#ifndef UNICODE_FONTS
#define UNICODE_FONTS

#include <QObject>

class UnicodeFonts : public QObject
{
    Q_OBJECT
    
public:
    UnicodeFonts(QObject *parent = 0);
    
    void isInUnicodeRange(int, int, QString);
    void applyFontAndSizeToQWidget(QString, QWidget *widget);
    void setFont(QString, QWidget *widget);
    void setFontSize(QWidget *widget, int, QString);
    void applyFontToQWidget(QString, QWidget *widget);
    
    QString printFonts(QString);
};

#endif
