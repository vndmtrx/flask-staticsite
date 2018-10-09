import yaml

def _preload_header(file, encoding):
    shield = '---\n'
    header = {}
    try:
        with open(file) as raw:
            r = raw.readline()
            if r == shield:
                while True:
                    line = raw.readline()
                    if not line: break
                    elif line == shield:
                        #header.append(raw.tell() - len(shield))
                        header['filepos'] = raw.tell()
                        break
                    else: continue
            raw.seek(len(shield), 0)
            header['headers'] = raw.read(header['filepos'] - len(shield))
    except IOError:
        print('Could not read file {0}'.format(file))
        pass
    return header

class Page(object):
    def __new__(cls, path, encoding):
        header = _preload_header(path)
        if len(header) == 2:
            return super(Page, cls).__new__(cls)
        else:
            raise ValueError('File has no headers')

    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding
        self.mtime = os.path.getmtime(path)
