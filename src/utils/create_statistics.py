import json
import re
import os


class StatisticsBox:
    def __init__(self, sheet, question, box, checked):
        self._sheet = sheet
        self._questions = {}
        self.double_checked = []
        self.add_box(question, box, checked)

    def add_box(self, question, box, checked):
        """
            add box to sheet and checks if question has multiple answers

            Args:
                question: question to which the box belongs to
                box: type of box ++, +, 0, -, -- as (1-5)
                checked: bool box checked
        """
        if question not in self._questions:
            self._questions[question] = [(box, checked)]
        else:
            if checked:
                for b, c in self._questions.get(question):
                    if c:
                        self.double_checked.append((question, b))
                        self.double_checked.append((question, box))
            self._questions.get(question).append((box, checked))

    def get_box_statistics(self):
        """
            get lists based on answer type

            Returns:
                pp: list of all questions which are checked ++
                p: list of all questions which are checked +
                neut: list of all questions which are checked 0
                n: list of all questions which are checked -
                nn: list of all questions which are checked --
        """
        pp = [q for q in self._questions if (1, 1) in self._questions.get(q)]
        p = [q for q in self._questions if (2, 1) in self._questions.get(q)]
        neut = [q for q in self._questions if (3, 1) in self._questions.get(q)]
        n = [q for q in self._questions if (4, 1) in self._questions.get(q)]
        nn = [q for q in self._questions if (5, 1) in self._questions.get(q)]
        return pp, p, neut, n, nn

    def get_statistics(self):
        """
            get reference numbers for sheet

            Returns:
                av: average answers of sheet (--:-2, -:-1, 0:0, +:1, ++:2)
                var: get variance of sheet
                size: number of answers on sheet
        """
        pp, p, neut, n, nn = self.get_box_statistics()
        size = len(pp + p + neut + n + nn)
        av = (2 * len(pp) + len(p) + 0 * len(neut) - len(n) - 2 * len(nn)) / size
        # var = (len(pp) * pow(av - 2, 2)
        #       + len(p)  * pow(av - 1, 2)
        #       + len(neut) * pow(av - 0, 2)
        #       + len(n) * pow(av + 1, 2)
        #       + len(nn) * pow(av + 2, 2)) / size
        var = 1
        return av, var, size

    def get_sheet(self):
        return self._sheet

    def get_unanswered(self):
        lst_unanswered = []
        for question in self._questions:
            if not any(check[1] for check in self._questions.get(question)):
                lst_unanswered.append(question)
        return lst_unanswered


def extractPath(path, path_boxes, path_sheet="Bogen", path_question="_question",
                path_box="_box", ext=".jpg"):
    """
        searches for int (.*) in a string
        *root*/*path_boxes*/Bogen(.*)_question(.*)_box(.*).*ext*

        Args:
            path: full path to box
            path_boxes: path to all boxes
            path_sheet: regex path for sheet
            path_question: regex path for question
            path_box: regex path for box
            ext: extension
        Returns:
            sheet: sheet number
            question: question number
            box: box number
    """
    p = path.strip(path_boxes).strip(ext)
    sheet = int(re.search(path_sheet + '(.*)' + path_question, p).group(1))
    question = int(re.search(path_question + '(.*)' + path_box, p).group(1))
    box = int(re.search(path_box + '(.*)', p).group(1))
    return sheet, question, box


def removeDuplicates(lst):
    return sorted([t for t in (set(tuple(i) for i in lst))])


def create_print_statistics(root, path):
    """
        prints statistics in the form
            Sheet number
            Answer types
            Multiple answers
            Unanswered
            Average
            Variance

        Args:
            root: path to root
            path: path of evaluation result for boxes by NN
    """
    print("Create Statistics ...")
    with open(os.path.normpath(os.path.join(root, path))) as box_json:
        data = json.loads(box_json.read())

    lst = []
    for raw_box in data:
        for key in raw_box.keys():
            box = extractPath(key, path_boxes=os.path.normpath(os.path.join(root, "data/boxes/"))) + (raw_box.get(key),)
            lst.append(box)

    sheet_lst = []
    for box in sorted(lst):
        if not box[0] in [sheet.get_sheet() for sheet in sheet_lst]:
            sheet_lst.append(StatisticsBox(box[0], box[1], box[2], box[3]))
        else:
            sheet_lst[len(sheet_lst) - 1].add_box(box[1], box[2], box[3])
    for sheet in sorted(sheet_lst, key=StatisticsBox.get_sheet):
        pp, p, neut, n, nn = sheet.get_box_statistics()
        av, var, size = sheet.get_statistics()
        print('Sheet number: ', sheet.get_sheet())
        print('++(2):', len(pp),
              ', +(1):', len(p),
              ', 0(0):', len(neut),
              ', -(-1):', len(n),
              ', --(-2):', len(nn))
        print('Answered questions:', size, '/ 14')
        if sheet.double_checked:
            print('Question was answered multiple times:', *removeDuplicates(sheet.double_checked))
        if sheet.get_unanswered():
            print('Question was not answered: ', sheet.get_unanswered())
        print('Average:', av)
        print('Variance:', var)
        print('-----------------------')
    print("Create Statistics ... OK")
