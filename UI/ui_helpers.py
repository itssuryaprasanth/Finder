import re


class Helpers:

    def url_validator(self, url):
        url_pattern = "https:\/\/([a-zA-Z0-9]+\.)?[a-zA-Z0-9]+\.(com|in|co)"
        try:
            pattern_result = re.compile(url_pattern)
            pattern_result.match(url)
            return True
        except:
            raise Exception("Following website patterns are supported!!")
