'''
Contains parser to deal with currencies data
'''
import datetime
import re
from lxml import etree


class CentralBankXMLParser:
    '''
    Implements xml file parser for European Central Bank currencies data
    '''
    regex_for_tagnames_cleanup = r'(?P<prefix>\{.*\})(?P<tagname>\w+)'

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self._root = None
        self._content = None
        self._initialize()

    def _initialize(self):
        '''Initialize parser'''
        self._content = self._get_file_content()
        parser = self._get_etree_parser()
        self._root = self._get_etree_root(
            self._content, parser)

    def _get_file_content(self) -> str:
        '''Get xml file content'''
        content = ''
        with open(self.filename, 'r') as input_file:
            content = input_file.read().encode()
        return content

    @staticmethod
    def _get_etree_parser(
            ns_clean=True, remove_comments=True, remove_blank_text=True):
        '''Configure XMLParser'''
        return etree.XMLParser(
            ns_clean=ns_clean,
            remove_comments=remove_comments,
            remove_blank_text=remove_blank_text)

    def _get_etree_root(
            self, content: str,
            parser: etree.XMLParser=None) -> etree.ElementTree:
        '''Get lxml element tree'''
        return etree.fromstring(content, parser=parser)

    def _get_cleaned_tagname(self, tagname: str) -> str:
        '''Clean tagname from unneed data'''
        return re.sub(
            self.regex_for_tagnames_cleanup, r'\g<tagname>', tagname)

    def _get_parent_cube(self) -> etree.ElementTree:
        '''
        Get parent tree object used for currency rates.
        "Cube" means <Cube> tag
        '''
        for node in self._root.getchildren():
            tagname = self._get_cleaned_tagname(node.tag)
            if tagname == 'Cube':
                return node

    def _get_newest_cube(self) -> etree.ElementTree:
        '''
        Get upper child tree object used for currency rates.
        "Cube" means <Cube> tag
        '''
        parent_cube = self._get_parent_cube()
        children = parent_cube.getchildren()
        if len(children) == 0:
            return None
        return children[0]

    def _get_currencies_data(self) -> dict:
        '''
        Extract currencies data from <Cube>
        '''
        newest_cube = self._get_newest_cube()
        if newest_cube is None:
            return {}

        time = datetime.datetime.strptime(
            newest_cube.attrib.get('time'), '%Y-%m-%d')
        currencies = {}
        for child in newest_cube.getchildren():
            currency_name =\
                child.attrib.get('currency').upper()
            currency_rate = child.attrib.get('rate')
            currencies[currency_name] =\
                float(currency_rate)
        return {
            'date': time,
            'currencies': currencies
        }

    def get_currencies_data(self) -> dict:
        '''Get extracted currencies data from xml file'''
        return self._get_currencies_data()
