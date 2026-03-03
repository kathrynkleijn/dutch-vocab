import random
from dutchvocab import lessons as lessons
import copy
from dutchvocab import vocab_functions as vf
import pandas as pd
from dutchvocab import lesson_objects as lo
from dutchvocab import figure_generator as fg
import inquirer
import time


def run_learning():

    print(
        "\nYou have chosen learning mode. Select a topic and lesson to learn the words and phrases.\n\n"
    )

    time.sleep(1.5)

    topic = vf.select_topic(mode="learning")

    if topic is not None:

        lesson_obj = getattr(lo, topic)

        lesson = vf.select_lesson(lesson_obj, mode="learning")

        print(
            "\nEach word and associated phrase(s) will be presented. Press enter after to see the translation.\n\n"
        )

        vf.flashcards(lesson)

    print("\n")
    mode_choice = [
        inquirer.List(
            "next",
            message="Would you like to continue? Select a mode to continue or exit to end the session.   ",
            choices=["Learning", "Practice", "Test", "Exit"],
        )
    ]
    next_action = inquirer.prompt(mode_choice)["next"]
    if next_action == "Exit":
        return None
    return next_action


def run_practice(log, practice=False):

    if not practice:
        print(
            "\nYou have chosen practice mode. You can now choose from any of the available lessons to practise a mixture of words and phrases.\n\n"
        )
        time.sleep(1.5)
        _ = input("Press Enter to continue")

    topic = vf.select_topic(mode="practice")

    if topic is not None:

        print("\n")
        lesson_types = ["vocabulary", "phrases"]
        lesson_enquiry = [
            inquirer.List(
                "lesson_type",
                message="What type of lesson do you want?",
                choices=lesson_types,
            )
        ]
        selected_type = inquirer.prompt(lesson_enquiry)
        ltype = selected_type["lesson_type"]

        phrases = True if ltype == "phrases" else False

        if topic == "all":
            lesson = lo.all.all
        else:
            lesson_obj = getattr(lo, topic)
            lesson = vf.select_lesson(lesson_obj, mode="practice")

        if lesson:

            questions = vf.select_questions(lesson, ltype)

            correct, questions, asked_questions, eng_typo = (
                vf.randomly_generated_lesson(lesson, questions, phrases=phrases)
            )

            if questions:
                log = vf.update_log(
                    log, topic, lesson.name, questions, correct, ltype, eng_typo
                )

            if topic != "all":
                try:
                    while (correct / questions) * 100 < 50:
                        again = input(
                            "\nScore less than 50% - try again?  (Y/N)       "
                        )
                        print("\n")
                        if again.upper() != "Y":
                            break
                        print(f"Retrying lesson {lesson.number} from {topic} ...\n")

                        lesson = copy.deepcopy(
                            lesson_obj.lessons[int(lesson.number) - 1]
                        )

                        correct, questions, asked_questions, eng_typo = (
                            vf.randomly_generated_lesson(
                                lesson,
                                questions,
                                phrases=phrases,
                                repeat=asked_questions,
                            )
                        )

                        if questions:
                            log = vf.update_log(
                                log,
                                topic,
                                lesson.name,
                                questions,
                                correct,
                                ltype,
                                eng_typo,
                            )

                except ZeroDivisionError:
                    pass

    print("\n")
    mode_choice = [
        inquirer.List(
            "next",
            message="Would you like to continue? Select a mode to continue or exit to end the session.   ",
            choices=["Learning", "Practice", "Test", "Exit"],
        )
    ]
    next_action = inquirer.prompt(mode_choice)["next"]
    if next_action == "Exit":
        return None, log
    return next_action, log


def run_test():

    print(
        "You have chosen test mode. You can choose to be tested on any of the available lessons. You will be given each word or phrase in English to translate first, then each in Dutch.\n\n"  # A report will be given at the end of the test."
    )
    time.sleep(1.5)
    _ = input("\n\nPress Enter to continue")
    print("\n\n")

    topic = vf.select_topic(mode="test")

    if topic is not None:

        lesson_obj = getattr(lo, topic)

        lesson = vf.select_lesson(lesson_obj, mode="test")

        if lesson:
            total = 2 * len(lesson.questions)
            print(
                "\nBeginning test...\nType exit to end the test. All progress will be lost.\n"
            )
            correct, complete, log = vf.test(lesson)

            if complete:
                print(
                    f"Your test score for {topic.capitalize()} lesson {lesson.number} is {correct} out of {total}."
                )
                fg.generate_test_figures(log)

    print("\n")
    mode_choice = [
        inquirer.List(
            "next",
            message="Would you like to continue? Select a mode to continue or exit to end the session.   ",
            choices=["Learning", "Practice", "Test", "Exit"],
        )
    ]
    next_action = inquirer.prompt(mode_choice)["next"]
    if next_action == "Exit":
        return None
    return next_action
