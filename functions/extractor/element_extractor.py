import boto3
from termcolor import colored

"""
Uses AWS comprehend to extract elements from a document.
"""
class ElementExtractor:
    def __init__(self):
        pass

    def colorize_string(self, string, color, entity, offset=0):
        begin = entity['BeginOffset'] + offset
        end = entity['EndOffset'] + offset
        colored_string = colored(string[begin: end], color=color)
        offset += len(colored_string) - len(string[begin: end])
        return "{}{}{}".format(string[0: begin], colored_string, string[end:]), offset

    def extract_elements(self, text):
        comprehend = boto3.client(service_name='comprehend', region_name='us-east-2')
        entities = comprehend.detect_entities(Text=text, LanguageCode='en')
        result = {}
        colored_str = text
        rep_list = []
        org_list = []
        coloring_buffer = 0
        for entity in entities['Entities']:
            if entity['Type'] == 'ORGANIZATION':
                # print("Organization: {}".format(entity['Text']))
                org_list.append(entity['Text'])
                colored_str, coloring_buffer = self.colorize_string(colored_str, 'red', entity, coloring_buffer)
            elif entity['Type'] == 'DATE':
                begin = entity['BeginOffset']
                if text.find('on', begin - 5, begin) != -1:
                    # print("Execution date:{}".format(entity['Text']))
                    result['Execution Date'] = entity['Text']
                    colored_str, coloring_buffer = self.colorize_string(colored_str, 'green', entity,
                                                                        coloring_buffer)
                elif text.find('from', begin - 5, begin) != -1:
                    # print("Start date:{}".format(entity['Text']))
                    result['Start Date'] = entity['Text']
                    colored_str, coloring_buffer = self.colorize_string(colored_str, 'blue', entity,
                                                                        coloring_buffer)
                elif text.find('to', begin - 5, begin) != -1:
                    # print("End date:{}".format(entity['Text']))
                    result['End Date'] = entity['Text']
                    colored_str, coloring_buffer = self.colorize_string(colored_str, 'cyan', entity,
                                                                        coloring_buffer)
            elif entity['Type'] == 'PERSON':
                # print("Representative: {}".format(entity['Text']))
                rep_list.append(entity['Text'])
                colored_str, coloring_buffer = self.colorize_string(colored_str, 'magenta', entity, coloring_buffer)
        result['Organizations'] = org_list
        result['Representatives'] = rep_list
        return result, colored_str


if __name__ == '__main__':
    text = """
    Exhibit 10.22.

    Supplemental Processing Agreement.

    Client (hereafter “Party A”):	Henan Jianyida Industrial Co., Ltd.

    Contractor (hereafter “Party B”):	Zhongping Energy & Chemical Group Hongrui New Construction Materials Co., Ltd.

    Based on negotiations, the parties hereby supplement the Processing Agreement they entered into on January 8, 2011, as follows:

    1.	On the basis of the above referenced Processing Agreement, the term is extended for one year from
    March 1, 2015 to March 1, 2016.
    2.	All other terms of the Processing Agreement shall remain in effect from the execution of this Supplemental
    Agreement.
    3.	This Agreement is executed into two original duplicates. This Agreement shall take effect upon
    execution of authorized representatives of the parties. Each party shall retain one duplicate.
    4.	The parties shall negotiate to resolve any unsettled matters.

    Party A: [Seal] 	 	Party B: [Seal]
    Signature: /s/ Hui Li	 	Signature: /s/ Qimin Cheng
    Date: February 25, 2015 	 	Date: February 25, 2015
    """

    result, new_text = ElementExtractor().extract_elements(text)
    print(new_text)
