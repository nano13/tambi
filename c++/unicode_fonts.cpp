
#include <unicode_fonts.h>

#include <QFont>

UnicodeFonts::UnicodeFonts(QObject *parent)
{
    
}

bool UnicodeFonts::isInUnicodeRange(int start, int end, QString string)
{
    return true;
}

void UnicodeFonts::applyFontAndSizeToQWidget(QString string, QWidget *widget)
{
    if (isInUnicodeRange(arabic_block[0], arabic_block[1], string))
    {
        
    }
    else if (isInUnicodeRange(hebrew_block[0], hebrew_block[1], string))
    {
        widget->setFont(QFont(hebrew_font));
    }
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
