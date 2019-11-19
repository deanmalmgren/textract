from .utils import ShellParser
from ..exceptions import UnknownMethod, ShellError

class Parser(ShellParser):
    """Extract text from doc files using antiword or abiword.
    """

    def extract(self, filename, method='', **kwargs):
        if method == '' or method == 'antiword':
            try:
                return self.extract_antiword(filename, **kwargs)
            except ShellError as ex:
                # If antiword isn't installed , then gracefully fallback to using
                # abiword instead.
                if method == '' and ex.is_not_installed():
                    return self.extract_abiword(filename, **kwargs)
                else:
                    raise ex

        elif method == 'antiword':
            return self.extract_antiword(filename, **kwargs)
        elif method == 'abiword':
            return self.extract_abiword(filename, **kwargs)
        else:
            raise UnknownMethod(method)

    def extract_abiword(self, filename, **kwargs):
        """Extract text from .doc using abiword. Supports Windows as well. """
        temp_filename = self.temp_filename()

        self.run(['abiword','--to=txt','-o',temp_filename, filename])
        txt = None
        with open(temp_filename,'r',encoding='utf-8') as f:
            txt = f.read()
        try:
            os.remove(temp_filename)
        except:
            pass

        return txt


    def extract_antiword(self, filename, **kwargs):
        stdout, stderr = self.run(['antiword', filename])
        return stdout
