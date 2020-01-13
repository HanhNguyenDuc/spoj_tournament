import requests 
import lxml.html as lh
# import pandas as pd
url = "https://www.spoj.com/PTIT/users/duchanhctn99/"

class DataProcessor:

    @staticmethod
    def is_invalid_content(content):
        # content : string
        if content == "":
            return True
        if len(content) > 20:
            return True
        return False





    @staticmethod
    def get_solved_problems(url):
        page = requests.get(url)
        doc = lh.fromstring(page.content)
        td_elements = doc.xpath('//td')
        # print(td_elements[0].text_content)

        solved_problems = []

        for T in td_elements:
            content = T.text_content()
            # print(len(content))
            if DataProcessor.is_invalid_content(content):
                continue
            solved_problems.append(content)

        return list(map(str, solved_problems))

    @staticmethod
    def convert_to_url(string):
        return "https://www.spoj.com/PTIT/problems/{}/".format(string)

    @staticmethod
    def convert_list_to_url(li):
        return list(map(convert_to_url, li))

    @staticmethod
    def get_solved_num(url):
        return len(DataProcessor.get_solved_problems(url))

    @staticmethod
    def sort_by_solved_num(ele):
        print(int(ele.solved_num))
        return int(ele.solved_num)

    @staticmethod
    def str_to_list(string):
        return list(string.split(" "))


if __name__ == "__main__":
    print(DataProcessor.get_solved_problems(url))
