__aps__ = {
    'api':          '1.0.0',
    'version':      '1.0',
    'uri':          None,
    'urimatrix':    None
}
import re
import sys

try:
        import agn
except:
        sys.path.append('/home/openemm/bin/scripts/')
        import agn


def handleOutgoingMail(ctx, mail):
        precedence = __aps__['precedence']
        if precedence:
                found = None
                for line in mail.head:
                        if line.lower().startswith('precedence'):
                                found = line
                                break
        if found is None:
                mail.head.append('Precedence: %s' % precedence)

        domain = mail.sender.rsplit('@', 1)[1]

        re_str = r"Message-ID: <(?P<uidstr>.*)@.*>"
        reg = re.compile(re_str)
        uidstr = None
        uid = None
        for header in mail.head:
                if header.lower().startswith('message-id:'):
                        # print header
                        m = reg.search(header)
                        uidstr = m.group("uidstr")
                        break
        if not uidstr is None:
                uid = agn.UID()
                try:
                        uid.parseUID(uidstr)
                except Exception as ex:
                        print ex

        xjob = __aps__['x-job']
        if not uid is None and xjob:
                if uid.mailingID > 0:
                        mail.head.append('X-job: ' + xjob % str(uid.mailingID))

        listid = __aps__['list-id']
        if not uid is None and listid:
                if uid.mailingID > 0:
                        mail.head.append('List-ID: ' + listid % (
                                         str(uid.companyID), domain))

        abusereports = __aps__['abuse-reports-to']
        if abusereports:
                mail.head.append(
                    'X-Abuse-Reports-To: ' + abusereports % domain)

        urimatrix = __aps__['urimatrix']
        uri = __aps__['uri']
        if urimatrix or uri:
                found = None
                mid = None
                for line in mail.head:
                        if line.lower().startswith('list-unsubscribe:'):
                                found = line
                        elif line.lower().startswith('message-id:'):
                                m = re.search(
                                    'Message-ID: <(?P<mid>.*)@.*>', line)
                                mid = m.group(1)
                if found is None:
                        try:
                                from urllib2 import quote
                        except ImportError:
                                from urllib import quote
                        data = {
                            'sender': mail.sender,
                            'urlsender': quote(mail.sender),
                            'recv': mail.receiver,
                            'urlrecv': quote(mail.receiver),
                            'mid': mid
                        }
                        isInMatrix = False
                        if urimatrix and not mid is None:
                                sDomain = mail.sender.rsplit('@', 1)[1]
                                for cline in urimatrix.split('\n'):
                                        if cline.startswith(sDomain + '|'):
                                                mail.head.append('List-Unsubscribe: <%s>, <%s>' % (
                                                                 cline.split('|')[1] % data, cline.split('|')[2] % data, ))
                                                isInMatrix = True
                                                break

                        if uri and not isInMatrix:
                                mail.head.append(
                                    'List-Unsubscribe: <%s>' % (uri % data, ))

if __name__ == '__main__':
        def _main():
                class struct:
                        pass
                mail = struct()
                mail.head = []
                mail.head.append(
                    'Message-ID: <20130823020049-1.1.h.b.0.pp89lw4y80@news.gnlv.fr>')
                mail.sender = 'news@toto.com'
                mail.receiver = 'someone@somewhere.com'
                __aps__['precedence'] = 'bulk'
                __aps__['x-job'] = '%s'
                __aps__['list-id'] = '<%s.%s>'
                __aps__['abuse-reports-to'] = '<abuse@%s>'
                handleOutgoingMail(None, mail)
                print mail.head[0]
                print mail.head[1]
                print mail.head[2]
                print mail.head[3]
                print mail.head[4]

                mail.head = []
                __aps__['uri'] = 'http://localhost/unsubscribe?%(urlrecv)s'
                handleOutgoingMail(None, mail)
                print mail.head[0]

                mail.head = []
                __aps__['urimatrix'] = 'news.example.com|mailto:DUN-%(urlrecv)s@lu.example.com|http://news.example.com?%(urlrecv)s\nletter.com|mailto:ext-%(urlrecv)s@localhost|http://localhost?%(urlrecv)s'
                handleOutgoingMail(None, mail)

        _main()
