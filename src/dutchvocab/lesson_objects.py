from dutchvocab import lessons
from dutchvocab import vocab_functions as vf
from collections import OrderedDict


class Lesson:

    def __init__(self, number, topic):
        self.number = number
        self.name = topic + str(number)
        self.questions = OrderedDict()
        self.words = OrderedDict()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}:\n\t{self.questions}"

    def add_question(self, question, answer):
        self.questions[question] = answer

    def add_questions(self, **kwargs):
        for question, answer in kwargs.items():
            self.questions[question] = answer

    def add_word(self, dutch, english):
        self.words[dutch] = english

    def add_words(self, **kwargs):
        for dutch, english in kwargs.items():
            self.words[dutch] = english


class Topic:

    def __init__(self, name):
        self.name = name
        self.lessons = []
        self.all = Lesson("all", self.name)
        self.vocab_lessons = []

    def __str__(self):
        return ", ".join(str(lesson) for lesson in self.lessons)

    def add_lesson(self, lesson):
        self.lessons.append(lesson)
        self.all.add_questions(**lesson.questions)
        self.all.add_words(**lesson.words)
        return f"Lesson {str(lesson)} added to {self.name}"


core = Topic("core")
fiction = Topic("fiction")
newspapers = Topic("newspapers")
spoken = Topic("spoken")
web = Topic("web")
general = Topic("general")
all = Topic("all")

topics = [core, fiction, newspapers, spoken, web, general]


for topic in topics:
    phrase_lessons = lessons.available_lessons[topic.name][0]
    vocab_lessons = lessons.available_lessons[topic.name][1]
    zipped_lessons = [(a, b) for a, b in zip(phrase_lessons, vocab_lessons)]
    for value, lesson in enumerate(zipped_lessons):
        phrases, words = lesson
        new_lesson = Lesson(value + 1, topic.name)
        new_lesson.add_questions(**phrases)
        new_lesson.add_words(**words)
        topic.add_lesson(new_lesson)
    all.add_lesson(topic.all)

available = ""
for num, topic in enumerate(topics):
    if len(topic.lessons) == 0:
        pass
    else:
        available += f"{num+1}. {topic.name.capitalize()}:\n\t\t1-{len(topic.lessons)}\n\t\tAll\n"
available += "All"


topics_all = [core, fiction, newspapers, spoken, web, general, all]


if __name__ == "__main__":
    print(available)
    print("\n\n")
    vf.slow_print(available, char_delay=0)
