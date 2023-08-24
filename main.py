import dpkt
import socket
import pygeoip

gi=pygeoip.GeoIP('GeoLiteCity.dat')

def retKML(dstip,srcip):
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name('49.36.99.88')
    try:
        dstlong = dst['longitude']
        dstlat = dst['latitude']
        srclong = src['longitude']
        srclat = src['latitude']
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(dstip, dstlong, dstlat, srclong, srclat)
        return kml
    except:
        return ''

def plotIPs(pcap):
    kmlpts = ''
    for (ts,buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            KML = retKML(dst,src)
            kmlpts = kmlpts + KML
        except:
            pass
    return kmlpts

def main():
    f=open('capture.pcap','rb')
    pcap=dpkt.pcap.Reader(f)
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
    '<Style id="transBluePoly">' \
                '<LineStyle>' \
                '<width>1.5</width>' \
                '<color>501400E6</color>' \
                '</LineStyle>' \
                '</Style>'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader+plotIPs(pcap)+kmlfooter
    print(kmldoc)

if __name__=='__main__':
    main()
