
#include <unicode_fonts.h>

#include <QFont>

#include <QDebug>

UnicodeFonts::UnicodeFonts(QObject *parent)
{
    
}

bool UnicodeFonts::isInUnicodeRange(int start, int end, QString string)
{
    QString::iterator iter;
    for (iter = string.begin(); iter < string.end(); iter++)
    {
//         qDebug() << iter->unicode();
        if (iter->unicode() > start and iter->unicode() < end)
        {
            return true;
        }
    }
    
    return false;
}

QFont UnicodeFonts::getFontAndSize(QString string)
{
    QFont font;
    
    if (isInUnicodeRange(arabic_block[0], arabic_block[1], string))
    {
//         qDebug() << "arabic";
        font = QFont(arabic_font);
        font.setPointSize(arabic_size);
    }
    else if (isInUnicodeRange(hebrew_block[0], hebrew_block[1], string))
    {
//         qDebug() << "hebrew";
        font = QFont(hebrew_font);
        font.setPointSize(hebrew_size);
    }
    else if (isInUnicodeRange(greek_block[0], greek_block[1], string))
    {
//         qDebug() << "greek";
        font = QFont(greek_font);
        font.setPointSize(greek_size);
    }
    else if (isInUnicodeRange(ipa_block[0], ipa_block[1], string))
    {
//         qDebug() << "ipa";
        font = QFont(ipa_font);
        font.setPointSize(ipa_size);
    }
    else
    {
//         qDebug() << "else";
        font = QFont(default_font);
        font.setPointSize(default_size);
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

QString UnicodeFonts::printFonts(QString filter)
{
    return "";
}
