import random
import pandas as pd
from datetime import date
from dutchvocab import lessons
from collections import Counter
import copy
from matplotlib import pyplot as plt
import numpy as np


def select_lesson(topic):
    trying = True
    while trying:
        try:
            lesson_enquiry = input(
                "Select a lesson, choose random or choose 'all'          "
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
    return lesson


def select_questions(lesson):
    questions = input(
        f"\nThere are {len(lesson.questions)} questions available. How many questions would you like?        "
    )
    if questions == "random":
        questions = random.randrange(5, len(lesson.questions))
    else:
        questions = int(questions)
    print(f"\nYou will have {questions} questions.\n\n")
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


def randomly_generated_lesson(lesson, questions, testing=None):

    question_number = 1
    correct = 0
    while question_number <= questions:
        # generate random language
        if testing is None:
            language = random.randrange(2)
        else:
            language = testing
        if language == 0:
            test = random.choice(list(lesson.questions.keys()))
            # get answer from user
            answer = input(f"{test}         ")
            if not answer:
                print("That's not right!")
                print(f"{correct_answer}\n")
            else:
                # return answer to user
                answer_formatted = answer_formatting(answer, test, lesson, language)

                if any(True for char in answer_formatted if char in ","):
                    answer_meanings = answer_formatted.split(", ")
                    test_meanings = lesson.questions[test].split(", ")
                    if Counter(answer_meanings) == Counter(test_meanings):
                        print("Correct!\n")
                        correct += 1
                    else:
                        print("That's not right!")
                        print(f"{lesson.questions[test]}\n")
                else:
                    if answer_formatted == lesson.questions[test]:
                        print("Correct!\n")
                        correct += 1
                    elif lesson.questions[test] in lessons.alternatives.keys():
                        if isinstance(lessons.alternatives[lesson.questions[test]], list):
                            if (
                                answer_formatted
                                in lessons.alternatives[lesson.questions[test]]
                            ):
                                print("Correct!\n")
                                correct += 1
                            else:
                                print("That's not right!")
                                print(f"{lesson.questions[test]}\n")
                        else:
                            if (
                                answer_formatted
                                == lessons.alternatives[lesson.questions[test]]
                            ):
                                print("Correct!\n")
                                correct += 1
                            else:
                                print("That's not right!")
                                print(f"{lesson.questions[test]}\n")

                    else:
                        print("That's not right!")
                        print(f"{lesson.questions[test]}\n")
            if not testing:
                lesson.questions.pop(test)

        else:
            correct_answer, test = random.choice(list(lesson.questions.items()))
            # get answer from user
            answer = input(f"{test}         ")
            if not answer:
                print("That's not right!")
                print(f"{correct_answer}\n")
            else:
                answer_formatted = answer_formatting(
                    answer, test, lesson.questions, language, correct_answer
                )
                # check for wij/we, zij/ze, jij/je
                answer = accept_alternatives(correct_answer, answer_formatted)
                # return answer to user
                try:
                    if lesson.questions[answer] == test:
                        print("Correct!\n")
                        correct += 1

                except:
                    if correct_answer in lessons.alternatives.keys():
                        if answer in lessons.alternatives[correct_answer]:
                            print("Correct!\n")
                            correct += 1
                        else:
                            print("That's not right!")
                            print(f"{correct_answer}\n")
                    else:
                        print("That's not right!")
                        print(f"{correct_answer}\n")
            if not testing:
                lesson.questions.pop(correct_answer)

        # repeat until all asked
        question_number += 1

    print(f"Lesson finished. You got {correct}/{questions} correct.")
    return correct


def update_log(log, topic, lesson, questions, correct):

    log_today = {
        "Module": topic,
        "Lesson": lesson,
        "Questions": questions,
        "Score": correct,
    }

    return pd.concat([log, pd.DataFrame(log_today, index=pd.Index([date.today()]))])


def visualisation_today():
    log = pd.read_csv("learning_log.csv")
    log_today = log[log.Date == date.today().strftime("%Y-%m-%d")]

    log_today = log_today.groupby(["Module", "Lesson"]).agg(
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

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].bar(
        log_today.Lesson,
        log_today.Questions,
        width=0.5,
        color=log_today.Module.map(colour_map),
    )
    axes[0].set_xlabel("Lesson")
    axes[0].set_ylabel("Total Questions Answered")

    axes[1].bar(
        log_today.Lesson,
        log_today.Percentage,
        width=0.5,
        color=log_today.Module.map(colour_map),
    )
    axes[1].set_xlabel("Lesson")
    axes[1].set_ylabel("Percentage")
    axes[1].set_ylim([0, 100])

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    visualisation_today()
