import random
from dutchvocab import lessons as lessons
import copy
from dutchvocab import vocab_functions as vf
import pandas as pd
from dutchvocab import lesson_objects as lo
from dutchvocab import figure_generator as fg
import inquirer
import time


def run_practice(log, practice=False):

    if not practice:
        print(
            "\nYou have chosen practice mode. You can now choose from any of the available lessons to practise a mixture of words and phrases.\n\n"
        )
        time.sleep(1.5)
        _ = input("Press Enter to continue")

    playing = True

    topics = [
        "core",
        "fiction",
        "newspapers",
        "spoken",
        "web",
        "general",
        "all",
        "random",
    ]
    choosing = True
    while choosing:
        print("\n\n")
        topic_enquiry = [
            inquirer.List(
                "topic",
                message="Select a topic, choose random for a random choice of topic, or choose all for an assortment of questions from all topics",
                choices=topics,
            )
        ]
        selected = inquirer.prompt(topic_enquiry)

        if selected["topic"] == "random":
            topic = random.choice(lessons.topics)
        else:
            topic = selected["topic"]

        print(f"You have selected {topic.capitalize()}.\n")

        continue_with_topic = [
            inquirer.List(
                "continue",
                message="",
                choices=[
                    "Continue",
                    "Choose different topic",
                    "Exit practice mode",
                ],
            )
        ]
        selected = inquirer.prompt(continue_with_topic)["continue"]

        if selected == "Exit practice mode":
            print("Exiting practice mode...")
            playing = False
            break
        elif selected == "Choose different topic":
            continue
        elif selected == "Continue":
            choosing = False

    if playing:

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
            lesson = vf.select_lesson(lesson_obj)

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
            choices=["Practice", "Test", "Exit"],
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

    is_testing = True
    choosing = True
    while choosing:
        topics = ["core", "fiction", "newspapers", "spoken", "web", "general"]
        topic_enquiry = [
            inquirer.List(
                "topic",
                message="Select a topic",
                choices=topics,
            )
        ]
        topic = inquirer.prompt(topic_enquiry)["topic"]

        print(f"You have selected {topic.capitalize()}.\n")

        continue_with_topic = [
            inquirer.List(
                "continue",
                message="",
                choices=[
                    "Continue",
                    "Choose different topic",
                    "Exit test mode",
                ],
            )
        ]
        selected = inquirer.prompt(continue_with_topic)["continue"]

        if selected == "Exit test mode":
            print("Exiting test mode...")
            is_testing = False
            break
        elif selected == "Choose different topic":
            continue
        elif selected == "Continue":
            choosing = False

    if is_testing:

        lesson_obj = getattr(lo, topic)

        lesson = vf.select_lesson(lesson_obj, test=True)
        total = 2 * len(lesson.questions)
        print(
            "\nBeginning test...\nType exit to end the test. All progress will be lost.\n"
        )
        correct, complete, log = vf.test(lesson)

        if complete:
            print(
                f"Your test score for {topic.capitalize()} lesson {lesson.number} is {correct} out of {total}."
            )
            print(log)
            fg.generate_test_figures(log)

    print("\n")
    mode_choice = [
        inquirer.List(
            "next",
            message="Would you like to continue? Select a mode to continue or exit to end the session.   ",
            choices=["Practice", "Test", "Exit"],
        )
    ]
    next_action = inquirer.prompt(mode_choice)["next"]
    if next_action == "Exit":
        return None
    return next_action
