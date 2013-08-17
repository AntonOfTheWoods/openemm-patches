__aps__ = {
        'api':          '1.0.0',
        'version':      '1.0',
        'uri':          None,
        'urimatrix':    None
}
#
def handleOutgoingMail (ctx, mail):
        urimatrix = __aps__['urimatrix']
        uri = __aps__['uri']
        if urimatrix or uri:
                found = None
                for line in mail.head:
                        if line.lower ().startswith ('list-unsubscribe:'):
                                found = line
                                break
                if found is None:
                        try:
                                from urllib2 import quote
                        except ImportError:
                                from urllib import quote
                        data = {
                                'sender': mail.sender,
                                'urlsender': quote (mail.sender),
                                'recv': mail.receiver,
                                'urlrecv': quote (mail.receiver)
                        }
                        isInMatrix = False
                        if urimatrix:
                                sDomain = mail.sender.rsplit('@', 1)[1]
                                for cline in urimatrix.split('\n'):
                                        if cline.startswith(sDomain + '|'):
                                                mail.head.append('List-Unsubscribe: <%s>, <%s>' % (cline.split('|')[1] % data, cline.split('|')[2] % data, ))
                                                isInMatrix = True
                                                break

                        if not isInMatrix:
                                mail.head.append ('List-Unsubscribe: <%s>' % (uri % data, ))

if __name__ == '__main__':
        def _main ():
                class struct:
                        pass
                mail = struct ()
                mail.head = []
                mail.sender = 'news@toto.com'
                mail.receiver = 'someone@somewhere.com'
                __aps__['uri'] = 'http://localhost/unsubscribe?%(urlrecv)s'
                handleOutgoingMail (None, mail)
                print mail.head[0]
                
                mail.head = []
                __aps__['urimatrix'] = 'news.example.com|mailto:DUN-%(urlrecv)s@lu.example.com|http://news.example.com?%(urlrecv)s\nletter.com|mailto:ext-%(urlrecv)s@localhost|http://localhost?%(urlrecv)s'
                handleOutgoingMail (None, mail)
                print mail.head[0]

        _main ()


