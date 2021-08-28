import json
import re


#TODO: rename Bogen to Sheet
class Box:
    def __init__(self, sheet, question, box, checked):
        self._sheet = sheet
        self._questions = {}
        self.double_checked = []
        self.add_box(question, box, checked)

    def add_box(self, question, box, checked):
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
        pp = [q for q in self._questions if (1, 1) in self._questions.get(q)]
        p = [q for q in self._questions if (2, 1) in self._questions.get(q)]
        neut = [q for q in self._questions if (3, 1) in self._questions.get(q)]
        n = [q for q in self._questions if (4, 1) in self._questions.get(q)]
        nn = [q for q in self._questions if (5, 1) in self._questions.get(q)]
        return pp, p, neut, n, nn

    def get_statistics(self):
        pp, p, neut, n, nn = self.get_box_statistics()
        size = len(pp + p + neut + n + nn)
        av = (2 * len(pp) + len(p) + 0 * len(neut) - len(n) - 2 * len(nn)) / size
        var = (len(pp) * pow(av - 2, 2)
              + len(p)  * pow(av - 1, 2)
              + len(neut) * pow(av - 0, 2)
              + len(n) * pow(av + 1, 2)
              + len(nn) * pow(av + 2, 2)) / size
        return av, var, size

    def get_sheet(self):
        return self._sheet

    def get_unanswered(self):
        lst_unanswered = []
        for question in self._questions:
            if not any(check[1] for check in self._questions.get(question)):
                lst_unanswered.append(question)
        return lst_unanswered


def extractPath(path, src_data="../../data/boxes/", ext=".jpg"):
    if not path.startswith(src_data):
        raise Exception(f"error in json: {path}")
    p = path.strip(src_data).strip(ext)
    sheet = int(re.search('Bogen(.*)_question', p).group(1))
    question = int(re.search('_question(.*)_box', p).group(1))
    box = int(re.search('_box(.*)', p).group(1))
    return sheet, question, box


def removeDuplicates(lst):
    return [t for t in (set(tuple(i) for i in lst))]


def create_print_statistics(path='../../data/box_evaluated.json'):
    with open(path) as box_json:
        data = json.loads(box_json.read())

    lst = []
    for raw_box in data:
        for key in raw_box.keys():
            box = extractPath(key) + (raw_box.get(key),)
            lst.append(box)

    sheet_lst = []
    for box in sorted(lst):
        if not box[0] in [sheet.get_sheet() for sheet in sheet_lst]:
            sheet_lst.append(Box(box[0], box[1], box[2], box[3]))
        else:
            sheet_lst[len(sheet_lst) - 1].add_box(box[1], box[2], box[3])
    for sheet in sorted(sheet_lst, key=Box.get_sheet):
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
        print('-----------------------')





