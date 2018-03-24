
#ifndef UNICODE_FONTS
#define UNICODE_FONTS

#include <QObject>

class UnicodeFonts : public QObject
{
    Q_OBJECT
    
public:
    UnicodeFonts(QObject *parent = 0);
    
    bool isInUnicodeRange(int, int, QString);
    QFont getFontAndSize(QString);
    void setFont(QString, QWidget *widget);
    void setFontSize(QWidget *widget, int, QString);
    void applyFontToQWidget(QString, QWidget *widget);
    
    QStringList getAvailableFonts(QString);
    
    QString loadFontFamilyFromTTF(QString);
    
private:
    int arabic_block[2] = {1536, 1791};
    int hebrew_block[2] = {1424, 1535};
    int greek_block[2] = {880, 1023};
    int ipa_block[2] = {250, 687};
    
    QString arabic_font = ":ttf_sheharazade";
    QString hebrew_font = ":ttf_ezra_sil";
    QString greek_font = ":ttf_galatia_sil";
    QString ipa_font = ":ttf_doulos_sil";
    
    QString default_font = ":ttf_dejavu_sans";
    
    int arabic_size = 40;
    int hebrew_size = 20;
    int greek_size = 15;
    int ipa_size = 15;
    
    int default_size = -1;
};

#endif
