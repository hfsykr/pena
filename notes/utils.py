from html.parser import HTMLParser
import json

class HTMLParser(HTMLParser):
    parser_result = []

    def handle_starttag(self, tag, attrs):
        self.parser_result.append({"markup": "<" + tag + ">"})

    def handle_endtag(self, tag):
        self.parser_result.append({"markup": "</" + tag + ">"})

    def handle_data(self, data):
        self.parser_result.append({"text": data})

    def get_result(self):
        return self.parser_result

    def reset(self):
        # Reset parser.feed()
        super().reset()
        self.parser_result = []
    
def html_text_to_json(text):
    parser = HTMLParser()
    parser.feed(text)
    result = json.dumps({"annotation": parser.get_result()})
    # Reset for next parser
    parser.reset()
    return result
