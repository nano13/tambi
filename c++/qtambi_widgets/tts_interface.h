
#include <QWidget>

#include <string.h>
#include <malloc.h>
#include <speak_lib.h>

class TTSInterface : public QWidget
{
    Q_OBJECT
    
public:
    TTSInterface(QWidget *parent = 0);
    
    void speak(QString);
    void stop();
    
private:
    espeak_POSITION_TYPE position_type;
    espeak_AUDIO_OUTPUT output;
    char *path=NULL;
    int Buflength = 500, Options=0;
    void* user_data;
    t_espeak_callback *SynthCallback;
    espeak_PARAMETER Parm;
    
    
    
    char text[20] = {"Hello World!"};
    unsigned int Size,position=0, end_position=0, flags=espeakCHARS_AUTO, *unique_identifier;
    
    /* char Voice[] = {"default"}; */
};
