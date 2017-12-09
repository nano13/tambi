
#ifndef UNICODE_FONTS
#define UNICODE_FONTS

#include <QObject>

class UnicodeFonts : public QObject
{
    Q_OBJECT
    
public:
    UnicodeFonts(QObject *parent = 0);
    
    static void isInUnicodeRange(int, int, QString);
    static void applyFontAndSizeToQWidget(QString, QWidget *widget);
    static void setFont(QString, QWidget *widget);
    static void setFontSize(QWidget *widget, int, QString);
    static void applyFontToQWidget(QString, QWidget *widget);
    
    QString printFonts(QString);
};

#endif
