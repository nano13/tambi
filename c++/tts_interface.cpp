
#include <string.h>
#include <malloc.h>

#include <tts_interface.h>
#include <speak_lib.h>

TTSInterface :: TTSInterface(QWidget *parent)
{
    /*
    espeak_POSITION_TYPE position_type;
    espeak_AUDIO_OUTPUT output;
    char *path=NULL;
    int Buflength = 500, Options=0;
    void* user_data;
    t_espeak_callback *SynthCallback;
    espeak_PARAMETER Parm;
    
    char Voice[] = {"default"};
    
    char text[20] = {"Hello World!"};
    unsigned int Size,position=0, end_position=0, flags=espeakCHARS_AUTO, *unique_identifier;
    */
}

void TTSInterface :: speak(QString speak_string)
{
    
    /* output = AUDIO_OUTPUT_PLAYBACK; */
    int I, Run = 1, L;
    /* espeak_Initialize(output, Buflength, path, Options ); */
    espeak_Initialize(AUDIO_OUTPUT_PLAYBACK, 500, NULL, 0);
    espeak_SetVoiceByName("default");
    Size = strlen(text)+1;
    printf("Saying  '%s'",text);
    espeak_Synth( text, Size, position, position_type, end_position, flags,
    unique_identifier, user_data );
    espeak_Synchronize( );
    printf("\n:Done\n");
}

void TTSInterface :: stop()
{
    
}
