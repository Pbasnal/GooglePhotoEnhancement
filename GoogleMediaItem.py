from gphotospy.media import MediaItem

class GoogleMediaItem(MediaItem):
   def __init__(self, media_object):
        """ GoogleMediaItem Constructor """
        super().__init__(media_object)

   def id(self):
        """ Gets the MediaItem's id """
        return self.val.get("id")