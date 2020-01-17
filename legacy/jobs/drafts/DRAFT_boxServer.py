#!/usr/bin/python
from pusher import Pusher
#global pusher
#global serialNumber
serialNumber = "000000002f5683c"

#pusher = Pusher(app_id=u'194337', key=u'57742453ee29b480f091', secret=u'79cb060b2928a442b554')

pusher_client = pusher.Pusher(
  app_id='194895',
  key='f3a6952cc326ee48eb10',
  secret='700363677ba4fd2d6f8c',
  cluster='eu',
  ssl=True
)

pusher_client.trigger('channel_'+str(serialNumber), 'event_'+str(serialNumber), {'message': 'hello world from test'})
