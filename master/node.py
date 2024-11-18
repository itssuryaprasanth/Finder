import pdb as pd
import sys
import time
import tkinter as tk
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from structure.org_describe import org_describe
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


class ScraperHTML:
    matching_pairs: list = []

    def __init__(self, url):
        # Start a session
        logger.info("Initiating the session")
        self.session = HTMLSession()
        self.url: str = url
        self.org_desc = org_describe
        self.attributes = None

    def get_session(self):
        response = None
        try:
            logger.info("getting the session with the url {}".format(self.url))
            response = self.session.get(self.url)
        finally:
            return response

    def render_response(self, response, tk_instance) -> int:
        try:
            second_label = tk.Label(tk_instance, text="Wait for HTML to Render...")
            second_label.place(x=100, y=250)
            if response is not None:
                response.html.render(sleep=2, timeout=60)
                second_label.destroy()
                logger.info("Rendered successfully")
            else:
                logger.info("Rendering Failed")
                from tkinter import messagebox as msgbox
                msgbox.showerror(message="Rendering Failed..")
                sys.exit(1)
        except Exception as e:
            logger.error("Rendering Failed with an error.. {}".format(e))
            return 0

    def parser_html(self, response, tk_instance) -> None:
        logger.info("Parsing the HTML from response ")
        try:
            third_label = tk.Label(tk_instance, text="Parsing the HTML...")
            third_label.place(x=100, y=250)
            time.sleep(2)
            soup = BeautifulSoup(response.html.html, "html.parser")
            attributes_list = []
            for element in soup.find_all(True):  # True finds all tags
                tag_attributes = {attr: value for attr, value in element.attrs.items()}
                attributes_list.append({
                    'tag': element.name,
                    'attributes': tag_attributes
                })

            self.attributes = attributes_list
            third_label.destroy()
        except Exception as e:
            logger.error("Parser html failed with an error {}".format(e))

    def find_key_value_pair(self, tk_instance) -> [list | None]:
        try:
            fourth_label = tk.Label(tk_instance, text="Gathering all Attributes..")
            fourth_label.place(x=100, y=250)
            time.sleep(2)
            keys_set = set(self.org_desc.keys())
            print(self.attributes)
            if isinstance(self.attributes, list):
                if self.attributes:
                    while self.attributes:
                        matching_set = self.attributes.pop()
                        if matching_set['tag'] in keys_set:
                            ScraperHTML.matching_pairs.append(matching_set)
                else:
                    raise Exception("Error Code: 1002")
            else:
                raise Exception("Error Code: 1001")
            fourth_label.destroy()
        finally:
            return self.matching_pairs


# if __name__ == '__main__':
#     sh = ScraperHTML()
#     sh.return_attributes()
#     print(sh.find_key_value_pair())
#     print(ScraperHTML.matching_pairs)
