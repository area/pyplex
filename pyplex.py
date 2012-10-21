import web
import urllib2
import re
import xml.etree.cElementTree as et
from pyomxplayer import OMXPlayer
from urlparse import urlparse
import avahi
import dbus

__all__ = ["ZeroconfService"]

class ZeroconfService:
    """A simple class to publish a network service with zeroconf using
    avahi.

    """

    def __init__(self, name, port, stype="_plexclient._tcp",
                 domain="", host="", text=""):
        self.name = name
        self.stype = stype
        self.domain = domain
        self.host = host
        self.port = port
        self.text = text

    def publish(self):
        bus = dbus.SystemBus()
        server = dbus.Interface(
                         bus.get_object(
                                 avahi.DBUS_NAME,
                                 avahi.DBUS_PATH_SERVER),
                        avahi.DBUS_INTERFACE_SERVER)

        g = dbus.Interface(
                    bus.get_object(avahi.DBUS_NAME,
                                   server.EntryGroupNew()),
                    avahi.DBUS_INTERFACE_ENTRY_GROUP)

        g.AddService(avahi.IF_UNSPEC, avahi.PROTO_UNSPEC,dbus.UInt32(0),
                     self.name, self.stype, self.domain, self.host,
                     dbus.UInt16(self.port), self.text)

        g.Commit()
        self.group = g
        print 'Service published'

    def unpublish(self):
        self.group.Reset()


        
urls = (
    '/xbmcCmds/xbmcHttp','xbmcCmdsXbmcHttp',
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class hello:        
    def GET(self,name):
        return 'Hello, World'

class xbmcCmdsXbmcHttp:
    def GET(self):
        string= urllib2.unquote(web.ctx.query)
        #Get command
        commandparse = re.search('command=(.*)\(.*', string)
        command = commandparse.group(1)
        #Get the args
	commandparse = re.search('.*\((.*)\).*',string)
        commandargs = commandparse.group(1).split(';')
        print command
        print commandargs	
        result = getattr(xbmcCmmd, command)(*commandargs)
        return 'received'

class xbmcCommands:
    def PlayMedia(self, fullpath, tag, unknown1, unknown2, unknown3):
        print '---'
	print fullpath
        print tag
        f = urllib2.urlopen(fullpath)
        s = f.read()
        f.close()
        print s
	tree = et.fromstring(s)
	#get video
        el = tree.find('./Video/Media/Part')
        print el.attrib['key']
        print 'fullpath', fullpath
        #Construct the path to the media.
        o = urlparse(fullpath)
        mediapath = o.scheme + "://" + o.netloc + el.attrib['key'] 
        print 'mediapath', mediapath
        global omx 
        omx = OMXPlayer(mediapath)
        omx.toggle_pause()
        
xbmcCmmd = xbmcCommands()

if __name__ == "__main__":
    service = ZeroconfService(name="Raspberry Plex", port=3000)
    service.publish()
    app.run()
    #service.unpublish()

