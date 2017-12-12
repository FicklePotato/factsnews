from lxml import etree
import random
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

FOLDER = "folder"
USERAGENT = "useragent"
IGNORE_TAGS = ["separator"]
XML_PATH = "/mnt/c/Projects/Fuse/scraper/userAgents.xml"

class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=""):
        super(RotateUserAgentMiddleware, self).__init__(user_agent)
        self.UA_list = []
        with open(XML_PATH, "rb") as f:
            xml_data = f.read()
        self.root = etree.fromstring(xml_data)
        self._extract_agents(self.root)

    def _extract_agents(self, node):
        children = node.getchildren()
        for child in children:
            if child.tag == FOLDER:
                self._extract_agents(child)
            elif child.tag == USERAGENT:
                self.UA_list.append(child.get(USERAGENT))
            elif child.tag not in IGNORE_TAGS:
                print("Got unknown tag: %s" % child.tag)

    def get_agent(self):
        return random.choice(self.UA_list)

    def process_request(self, request, spider):
        request.headers.setdefault(b'User-Agent', self.get_agent())
