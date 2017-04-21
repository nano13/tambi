
import mimetypes, os

class MimetypeAnalyzer(object):
    def __init__(self):
        pass
    
    """
    returns one of: ['image', 'text']
    """
    def isImageOrText(self, basepath, filename):
        mime = mimetypes.guess_type(os.path.join(basepath, filename))
        print(mime)
        
        if mime[0] == 'image/jpeg':
            return 'image'
        else:
            return 'text'
