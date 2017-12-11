
#include <unicode_fonts.h>

#include <QFont>
#include <QFontDatabase>

#include <QDebug>

UnicodeFonts::UnicodeFonts(QObject *parent)
{
    /*
    QStringList fonts = {"../assets/fonts/SILEOT.ttf",
        "../assets/fonts/Scheherazade-Regular.ttf",
        "../assets/fonts/EzraSIL2.51/SILEOT.ttf",
        "../assets/fonts/GalSIL21/GalSILR.ttf",
        "../assets/fonts/DoulosSIL-R.ttf",
        "../assets/fonts/Respective.ttf",
    };
    for (int i=0; i<fonts.length(); i++)
    {
        QString font = fonts[i];
        qDebug() << font;
        qDebug() << QFontDatabase::addApplicationFont(font);
    }
    */
}

bool UnicodeFonts::isInUnicodeRange(int start, int end, QString string)
{
    QString::iterator iter;
    for (iter = string.begin(); iter < string.end(); iter++)
    {
        if (iter->unicode() > start and iter->unicode() < end)
        {
            return true;
        }
    }
    
    return false;
}

QFont UnicodeFonts::getFontAndSize(QString string)
{
    QString font_name;
    int font_size;
    
    if (isInUnicodeRange(arabic_block[0], arabic_block[1], string))
    {
        qDebug() << "arabic";
        font_name = arabic_font;
        font_size = arabic_size;
    }
    else if (isInUnicodeRange(hebrew_block[0], hebrew_block[1], string))
    {
        qDebug() << "hebrew";
        font_name = hebrew_font;
        font_size = hebrew_size;
    }
    /*
    else if (isInUnicodeRange(greek_block[0], greek_block[1], string))
    {
        qDebug() << "greek";
        font_name = greek_font;
        font_name = greek_size;
    }
    */
    /*
    else if (isInUnicodeRange(ipa_block[0], ipa_block[1], string))
    {
        qDebug() << "ipa";
        font_name = ipa_font;
        font_size = ipa_size;
    }
    */
    else
    {
        qDebug() << "else";
        font_name = default_font;
        font_size = default_size;
    }
    qDebug() << "FONT NAME:";
    qDebug() << font_name;
    
    QString fontFamily = loadFontFamilyFromTTF(font_name);
    QFont *custom_font = new QFont(fontFamily, font_size, QFont::Normal, false);
    
    return *custom_font;
}

QString UnicodeFonts::loadFontFamilyFromTTF(QString font_name)
{
    QString font;
    bool loaded = false;
    if(!loaded)
    {
        loaded = true;
        int loadedFontID = QFontDatabase::addApplicationFont(font_name);
        QStringList loadedFontFamilies = QFontDatabase::applicationFontFamilies(loadedFontID);
        if(!loadedFontFamilies.empty())
        {
            font = loadedFontFamilies.at(0);
        }
    }
    return font;
}

void UnicodeFonts::setFont(QString font_category, QWidget *widget)
{
    
}

void UnicodeFonts::setFontSize(QWidget *widget, int size, QString font_name = NULL)
{
    
}

void UnicodeFonts::applyFontToQWidget(QString string, QWidget *widget)
{
    
}

QStringList UnicodeFonts::getAvailableFonts(QString filter = "")
{
    QFontDatabase *base = new QFontDatabase();
    QStringList fonts = base->families();//QFontDatabase::Arabic);
    return fonts;
}
