import random
import math
import pandas as pd
from datetime import date
from dutchvocab import lessons
from collections import Counter
import copy
from matplotlib import pyplot as plt
import numpy as np
from fuzzywuzzy import fuzz


def select_lesson(topic, test=False):
    trying = True
    while trying:
        if not test:
            try:
                lesson_enquiry = input(
                    "Select a lesson, choose random for a random choice of lesson, or choose all for an assortment of questions from all lessons          "
                ).lower()
                if lesson_enquiry == "random":
                    lesson_num = random.randrange((len(topic.lessons) - 1))
                    lesson = copy.deepcopy(topic.lessons[int(lesson_num) - 1])
                    print(
                        f"\nYou have chosen lesson {lesson.number} from {topic.name.capitalize()}."
                    )
                elif lesson_enquiry == "all":
                    lesson = copy.deepcopy(topic.all)
                    print(f"\nYou have chosen all of {topic.name.capitalize()}.")
                else:
                    lesson = copy.deepcopy(topic.lessons[int(lesson_enquiry) - 1])
                    print(
                        f"\nYou have chosen lesson {lesson.number} from {topic.name.capitalize()}."
                    )
                trying = False
            except:
                continue
        else:
            try:
                lesson_enquiry = input(
                    "Select a lesson to be tested on         "
                ).lower()

                lesson = copy.deepcopy(topic.lessons[int(lesson_enquiry) - 1])
                print(
                    f"\nYou have chosen lesson {lesson.number} from {topic.name.capitalize()}."
                )
                trying = False
            except:
                continue
    return lesson


def select_questions(lesson):
    questions = input(
        f"\nThere are {len(lesson.questions)} questions available. How many questions would you like?        "
    )
    if questions == "random":
        questions = random.randrange(5, len(lesson.questions))
    else:
        questions = int(questions)
    print(
        f"\nYou will have {questions} questions. Type 'exit' at any time to end the lesson.\n\n"
    )
    return questions


def select_words(lesson):
    questions = input(
        f"\nThere are {len(lesson.words)} words available. How many would you like?        "
    )
    if questions == "random":
        questions = random.randrange(5, len(lesson.words))
    else:
        questions = int(questions)
    print(
        f"\nYou will have {questions} words. Type 'exit' at any time to end the lesson.\n\n"
    )
    return questions


def accept_alternatives(test, answer):
    if "We" in test:
        if "Wij" in answer:
            return answer.replace("Wij", "We")
        else:
            return answer
    elif "Wij" in test:
        if "We" in answer:
            return answer.replace("We", "Wij")
        else:
            return answer
    elif "Ze" in test:
        if "Zij" in answer:
            return answer.replace("Zij", "Ze")
        else:
            return answer
    elif "Zij" in test:
        if "Ze" in answer:
            return answer.replace("Ze", "Zij")
        else:
            return answer
    elif "Je" in test:
        if "Jij" in answer:
            return answer.replace("Jij", "Je")
        else:
            return answer
    elif "Jij" in test:
        if "Je" in answer:
            return answer.replace("Je", "Jij")
        else:
            return answer
    else:
        return answer


def answer_formatting(answer, test, lesson, language, correct_answer=""):
    answer_words = answer.lower().split()

    if language:
        for word in lessons.proper_nouns_ned:
            if word.lower() in answer_words:
                index = answer_words.index(word.lower())
                answer_words[index] = word
        if len(test.split()) > 2 and len(correct_answer.split()) > 2:
            answer_words[0] = answer_words[0].capitalize()

    else:
        for word in lessons.proper_nouns_eng:
            if word.lower() in answer_words:
                index = answer_words.index(word.lower())
                answer_words[index] = word

        answer_words = ["I" if word == "i" else word for word in answer_words]
        if len(test.split()) > 2 and len(lesson.questions[test].split()) > 2:
            answer_words[0] = answer_words[0].capitalize()

    return " ".join(word for word in answer_words)


def typos_and_word_order(answer, test):

    if len(test.split()) != len(answer.split()):
        return False

    score = fuzz.token_sort_ratio(test, answer)
    length = max(len(test), len(answer))

    if length <= 4:
        threshold = 90
    elif length <= 8:
        threshold = 85
    elif length <= 15:
        threshold = 80
    else:
        threshold = 75

    return score >= threshold


def dutch_question(answer, correct, dutch, english, lesson):

    answer_formatted = answer_formatting(answer, dutch, lesson, 0)
    if "I am" in answer_formatted:
        answer_formatted = answer_formatted.replace("I am", "I'm")

    if any(True for char in answer_formatted if char in ","):
        answer_meanings = answer_formatted.split(", ")
        test_meanings = english.split(", ")
        if Counter(answer_meanings) == Counter(test_meanings):
            print("Correct!\n")
            correct += 1
        else:
            print("That's not right!")
            print(f"{english}\n")
    else:
        if answer_formatted == english:
            print("Correct!\n")
            correct += 1
        elif typos_and_word_order(answer_formatted, english):
            print("Correct! (You have a typo or different word order)\n")
            print(f"{english}\n")
            correct += 1
        elif english in lessons.alternatives.keys():
            alternatives = lessons.alternatives[english]
            if isinstance(alternatives, list):
                if answer_formatted in alternatives:
                    print("Correct!\n")
                    correct += 1
                elif any(
                    typos_and_word_order(answer_formatted, alt) for alt in alternatives
                ):
                    print("Correct! (You have a typo or different word order)\n")
                    print(f"{english}\n")
                    correct += 1
                else:
                    print("That's not right!")
                    print(f"{english}\n")
            else:
                if answer_formatted == alternatives:
                    print("Correct!\n")
                    correct += 1
                elif typos_and_word_order(
                    answer_formatted,
                    alternatives,
                ):
                    print("Correct! (You have a typo or different word order)\n")
                    print(f"{english}\n")
                    correct += 1
                else:
                    print("That's not right!")
                    print(f"{english}\n")

        else:
            print("That's not right!")
            print(f"{english}\n")

    return correct


def english_question(answer, correct, dutch, english, lesson):

    answer_formatted = answer_formatting(answer, english, lesson.questions, 1, dutch)

    # check for wij/we, zij/ze, jij/je
    answer = accept_alternatives(dutch, answer_formatted)

    # return answer to user
    if answer == dutch:
        print("Correct!\n")
        correct += 1
    elif dutch in lessons.alternatives.keys():
        if answer in lessons.alternatives[dutch]:
            print("Correct!\n")
            correct += 1
        else:
            print("That's not right!")
            print(f"{dutch}\n")
    else:
        print("That's not right!")
        print(f"{dutch}\n")

    return correct


def dutch_word(answer, correct, english):

    answer_words = answer.lower().split()
    answer_formatted = " ".join(word for word in answer_words)

    if any(True for char in answer_formatted if char in ","):
        answer_meanings = answer_formatted.split(", ")
        test_meanings = english.split(", ")
        if Counter(answer_meanings) == Counter(test_meanings):
            print("Correct!\n")
            correct += 1
        else:
            print("That's not right!")
            print(f"{english}\n")
    else:
        if answer_formatted == english:
            print("Correct!\n")
            correct += 1
        elif typos_and_word_order(answer_formatted, english):
            print("Correct! (You have a typo)\n")
            print(f"{english}\n")
            correct += 1
        elif english in lessons.alternatives.keys():
            alternatives = lessons.alternatives[english]
            if isinstance(alternatives, list):
                if answer_formatted in alternatives:
                    print("Correct!\n")
                    correct += 1
                elif any(
                    typos_and_word_order(answer_formatted, alt) for alt in alternatives
                ):
                    print("Correct! (You have a typo)\n")
                    print(f"{english}\n")
                    correct += 1
                else:
                    print("That's not right!")
                    print(f"{english}\n")
            else:
                if answer_formatted == alternatives:
                    print("Correct!\n")
                    correct += 1
                elif typos_and_word_order(
                    answer_formatted,
                    alternatives,
                ):
                    print("Correct! (You have a typo)\n")
                    print(f"{english}\n")
                    correct += 1
                else:
                    print("That's not right!")
                    print(f"{english}\n")

        else:
            print("That's not right!")
            print(f"{english}\n")

    return correct


def english_word(answer, correct, dutch):

    answer_words = answer.lower().split()
    answer = " ".join(word for word in answer_words)

    # return answer to user
    if answer == dutch:
        print("Correct!\n")
        correct += 1
    elif dutch in lessons.alternatives.keys():
        if answer in lessons.alternatives[dutch]:
            print("Correct!\n")
            correct += 1
        else:
            print("That's not right!")
            print(f"{dutch}\n")
    else:
        print("That's not right!")
        print(f"{dutch}\n")

    return correct


def randomly_generated_lesson(lesson, questions, testing=None):

    all_questions = list(lesson.questions.items())

    random.shuffle(all_questions)

    if questions < len(all_questions):
        all_questions = all_questions[:questions]
    elif questions > len(all_questions):
        extra = math.ceil(questions / len(all_questions)) - 1
        for i in range(extra):
            extra_questions = list(lesson.questions.items())
            all_questions.extend(random.shuffle(extra_questions))

    correct = 0
    question_number = 1
    asked_questions = []
    for dutch, english in all_questions:
        # choose language: 0 = Dutch->English, 1 = English->Dutch
        if testing is None:
            language = random.randrange(2)
        else:
            language = testing

        if language == 0:
            # Dutch question
            answer = input(f"{dutch}         ")
            if answer.lower() == "exit":
                print("Exiting lesson...")
                questions = question_number - 1
                break
            if not answer:
                print("That's not right!")
                print(f"{english}\n")
            else:
                correct = dutch_question(answer, correct, dutch, english, lesson)

            asked_questions.append((0, dutch, english))

        else:
            # English question
            answer = input(f"{english}         ")
            if answer.lower() == "exit":
                print("Exiting lesson...")
                questions = question_number - 1
                break
            if not answer:
                print("That's not right!")
                print(f"{dutch}\n")
            else:
                correct = english_question(answer, correct, dutch, english, lesson)

            asked_questions.append((1, dutch, english))

        # count questions
        question_number += 1

    print(f"Lesson finished. You got {correct}/{questions} correct.")

    return correct, questions, asked_questions


def randomly_generated_vocab_lesson(lesson, words):

    all_questions = list(lesson.words.items())

    random.shuffle(all_questions)

    if words < len(all_questions):
        all_questions = all_questions[:words]
    elif words > len(all_questions):
        extra = math.ceil(words / len(all_questions)) - 1
        for i in range(extra):
            extra_questions = list(lesson.words.items())
            all_questions.extend(random.shuffle(extra_questions))

    correct = 0
    question_number = 1
    asked_questions = []
    for dutch, english in all_questions:
        # choose language: 0 = Dutch->English, 1 = English->Dutch
        language = random.randrange(2)

        if language == 0:
            # Dutch question
            answer = input(f"{dutch}         ")
            if answer.lower() == "exit":
                print("Exiting lesson...")
                words = question_number - 1
                break
            if not answer:
                print("That's not right!")
                print(f"{english}\n")
            else:
                correct = dutch_word(answer, correct, english)

            asked_questions.append((0, dutch, english))

        else:
            # English question
            answer = input(f"{english}         ")
            if answer.lower() == "exit":
                print("Exiting lesson...")
                words = question_number - 1
                break
            if not answer:
                print("That's not right!")
                print(f"{dutch}\n")
            else:
                correct = english_word(answer, correct, dutch)

            asked_questions.append((1, dutch, english))

        # count questions
        question_number += 1

    print(f"Lesson finished. You got {correct}/{words} correct.")

    return correct, words, asked_questions


def repeated_lesson(lesson, questions, all_questions=[]):

    random.shuffle(all_questions)

    correct = 0
    question_number = 1

    for language, dutch, english in all_questions:

        if language == 0:
            # Dutch question
            answer = input(f"{dutch}         ")
            if answer.lower() == "exit":
                print("Exiting lesson...")
                questions = question_number - 1
                break
            if not answer:
                print("That's not right!")
                print(f"{english}\n")
            else:
                correct = dutch_question(answer, correct, dutch, english, lesson)

        else:
            # English question
            answer = input(f"{english}         ")
            if answer.lower() == "exit":
                print("Exiting lesson...")
                questions = question_number - 1
                break
            if not answer:
                print("That's not right!")
                print(f"{dutch}\n")
            else:
                correct = english_question(answer, correct, dutch, english, lesson)

        # count questions
        question_number += 1

    print(f"Lesson finished. You got {correct}/{questions} correct.")

    return correct, questions, all_questions


def test(lesson):

    complete = False

    all_questions = list(lesson.questions.items())

    random.shuffle(all_questions)

    correct = 0

    for dutch, english in all_questions:
        answer = input(f"{english}         ")
        if answer.lower() == "exit":
            exit_confirm = input(
                "\nExiting test. All progress will be lost. Are you sure you wish to exit?   "
            )
            if exit_confirm.strip().lower() != "y":
                print("\nContinuing with test\n")
                continue
            else:
                print("\nExiting...\n")
                return correct, complete
        if not answer:
            print("That's not right!")
            print(f"{dutch}\n")
        else:
            correct = english_question(answer, correct, dutch, english, lesson)

    random.shuffle(all_questions)

    for dutch, english in all_questions:
        answer = input(f"{dutch}         ")
        if answer.lower() == "exit":
            exit_confirm = input(
                "\nExiting test. All progress will be lost. Are you sure you wish to exit?   "
            )
            if exit_confirm.strip().lower() != "y":
                print("\nContinuing with test\n")
                continue
            else:
                print("\nExiting...\n")
                return correct, complete
        if not answer:
            print("That's not right!")
            print(f"{english}\n")
        else:
            correct = dutch_question(answer, correct, dutch, english, lesson)

    complete = True

    return correct, complete


def update_log(log, topic, lesson, questions, correct, ltype):

    log_today = {
        "Module": topic,
        "Lesson": lesson,
        "Questions": questions,
        "Score": correct,
        "Type": ltype,
    }

    return pd.concat([log, pd.DataFrame(log_today, index=pd.Index([date.today()]))])


def visualisation_today(year=False, month=False, day=False):
    if year:
        chosen_date = date(year, month, day)
    else:
        chosen_date = date.today()

    log = pd.read_csv("learning_log.csv")
    log_today = log[log.Date == chosen_date.strftime("%Y-%m-%d")]

    log_today = log_today.groupby(["Type", "Module", "Lesson"]).agg(
        Questions=("Questions", "sum"), Score=("Score", "sum")
    )
    log_today = log_today.reset_index()
    log_today["Percentage"] = log_today.apply(
        lambda row: round(row["Score"] / row["Questions"] * 100, 1), axis=1
    )

    cm = plt.colormaps["tab10"]
    colour_labels = log_today.Module.unique()
    colours = cm(np.linspace(0, 1, len(colour_labels)))
    colour_map = dict(zip(colour_labels, colours))

    phrases = log_today[log_today.Type == "phrases"]
    vocab = log_today[log_today.Type == "vocabulary"]

    types_to_plot = []
    if not phrases.empty:
        types_to_plot.append((phrases, "Phrases"))
    if not vocab.empty:
        types_to_plot.append((vocab, "Vocabulary"))

    n_rows = len(types_to_plot)

    if n_rows == 0:
        pass
    else:
        fig, axes = plt.subplots(n_rows, 2, figsize=(10, 5 * n_rows))
        if n_rows == 1:
            axes = np.array([axes])

        for i, (df, title) in enumerate(types_to_plot):

            axes[i][0].bar(
                df.Lesson,
                df.Questions,
                width=0.5,
                color=df.Module.map(colour_map),
            )
            axes[i][0].set_title(f"{title}: Questions Answered")
            axes[i][0].set_xlabel("Lesson")
            axes[i][0].set_ylabel("Total Questions")

            axes[i][1].bar(
                df.Lesson,
                df.Percentage,
                width=0.5,
                color=df.Module.map(colour_map),
            )
            axes[i][1].set_title(f"{title}: Percentage")
            axes[i][1].set_xlabel("Lesson")
            axes[i][1].set_ylabel("Percentage")
            axes[i][1].set_ylim([0, 100])

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    year = int(input("Year: "))
    month = int(input("Month: "))
    day = int(input("Day: "))

    visualisation_today(year, month, day)
