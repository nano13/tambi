
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
    
private:
    int arabic_block[2] = {1536, 1791};
    int hebrew_block[2] = {1424, 1535};
    int greek_block[2] = {880, 1023};
    int ipa_block[2] = {250, 687};
    
    QString arabic_font = "Scheherazade";
    QString hebrew_font = "Ezra SIL";
    QString greek_font = "Galatia SIL";
    QString ipa_font = "Doulos SIL";
    
    int arabic_size = 40;
    int hebrew_size = 20;
    int greek_size = 15;
    int ipa_size = 15;
};

#endif
