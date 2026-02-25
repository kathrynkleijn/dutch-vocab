import random
from dutchvocab import lessons as lessons
import copy
from dutchvocab import vocab_functions as vf
import pandas as pd
from dutchvocab import lesson_objects as lo
from dutchvocab import figure_generator as fg
import inquirer
import time


def run_practice(log):

    print(
        "\nYou have chosen practice mode. You can now choose from any of the available lessons to practise a mixture of words and phrases.\n\n"
    )
    time.sleep(1.5)
    _ = input("Press Enter to continue")

    playing = True
    while playing:

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

            print(f"You have selected {topic.capitalize()}.")

            continue_with_topic = input(
                "\nPress Enter to accept this choice and continue, or type N to try again. Type X to cancel and exit.     "
            )
            if continue_with_topic.upper() == "X":
                print("Exiting lesson...")
                playing = False
                break
            elif continue_with_topic.upper() == "N":
                continue
            else:
                choosing = False

        if not playing:
            break

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

        if topic == "core":
            lesson = vf.select_lesson(lo.core)
            if not lesson:
                playing = False
                break

            if ltype == "phrases":
                questions = vf.select_questions(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_lesson(lesson, questions)
                )

            elif ltype == "vocabulary":
                words = vf.select_words(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_vocab_lesson(lesson, words)
                )

            if questions:
                log = vf.update_log(
                    log, topic, lesson.name, questions, correct, ltype, eng_typo
                )

        elif topic == "fiction":
            lesson = vf.select_lesson(lo.fiction)
            if not lesson:
                playing = False
                break

            if ltype == "phrases":
                questions = vf.select_questions(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_lesson(lesson, questions)
                )

            elif ltype == "vocabulary":
                words = vf.select_words(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_vocab_lesson(lesson, words)
                )

            if questions:
                log = vf.update_log(
                    log, topic, lesson.name, questions, correct, ltype, eng_typo
                )

        elif topic == "newspapers":
            lesson = vf.select_lesson(lo.newspapers)
            if not lesson:
                playing = False
                break

            if ltype == "phrases":
                questions = vf.select_questions(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_lesson(lesson, questions)
                )

            elif ltype == "vocabulary":
                words = vf.select_words(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_vocab_lesson(lesson, words)
                )

            if questions:
                log = vf.update_log(
                    log, topic, lesson.name, questions, correct, ltype, eng_typo
                )

        elif topic == "spoken":
            lesson = vf.select_lesson(lo.spoken)
            if not lesson:
                playing = False
                break

            if ltype == "phrases":
                questions = vf.select_questions(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_lesson(lesson, questions)
                )

            elif ltype == "vocabulary":
                words = vf.select_words(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_vocab_lesson(lesson, words)
                )

            if questions:
                log = vf.update_log(
                    log, topic, lesson.name, questions, correct, ltype, eng_typo
                )

        elif topic == "web":
            lesson = vf.select_lesson(lo.web)
            if not lesson:
                playing = False
                break

            if ltype == "phrases":
                questions = vf.select_questions(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_lesson(lesson, questions)
                )

            elif ltype == "vocabulary":
                words = vf.select_words(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_vocab_lesson(lesson, words)
                )

            if questions:
                log = vf.update_log(
                    log, topic, lesson.name, questions, correct, ltype, eng_typo
                )

        elif topic == "general":
            lesson = vf.select_lesson(lo.general)
            if not lesson:
                playing = False
                break

            if ltype == "phrases":
                questions = vf.select_questions(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_lesson(lesson, questions)
                )

            elif ltype == "vocabulary":
                words = vf.select_words(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_vocab_lesson(lesson, words)
                )

            if questions:
                log = vf.update_log(
                    log, topic, lesson.name, questions, correct, ltype, eng_typo
                )

        elif topic == "all":
            lesson = lo.all.all
            if ltype == "phrases":
                questions = vf.select_questions(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_lesson(lesson, questions)
                )

            elif ltype == "vocabulary":
                words = vf.select_words(lesson)

                correct, questions, asked_questions, eng_typo = (
                    vf.randomly_generated_vocab_lesson(lesson, words)
                )

            if questions:
                log = vf.update_log(
                    log, topic, lesson.name, questions, correct, ltype, eng_typo
                )

        if topic != "all":
            try:
                while (correct / questions) * 100 < 50:
                    again = input("\nScore less than 50% - try again?  (Y/N)       ")
                    print("\n")
                    if again.upper() != "Y":
                        break
                    print(f"Retrying lesson {lesson.number} from {topic} ...\n")
                    if topic == "core":
                        lesson = copy.deepcopy(lo.core.lessons[int(lesson.number) - 1])
                    elif topic == "fiction":
                        lesson = copy.deepcopy(
                            lo.fiction.lessons[int(lesson.number) - 1]
                        )
                    elif topic == "newspapers":
                        lesson = copy.deepcopy(
                            lo.newspapers.lessons[int(lesson.number) - 1]
                        )
                    elif topic == "spoken":
                        lesson = copy.deepcopy(
                            lo.spoken.lessons[int(lesson.number) - 1]
                        )
                    elif topic == "web":
                        lesson = copy.deepcopy(lo.web.lessons[int(lesson.number) - 1])
                    elif topic == "general":
                        lesson = copy.deepcopy(
                            lo.general.lessons[int(lesson.number) - 1]
                        )
                    correct, questions, asked_questions = vf.repeated_lesson(
                        lesson, questions, all_questions=asked_questions
                    )
                    if questions:
                        log = vf.update_log(
                            log, topic, lesson.name, questions, correct, ltype
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
        if next_action == "Practice":
            # repeat in practice mode
            continue
        elif next_action == "Exit":
            # exit the session
            return None, log
        else:
            # switch to "Test" mode
            return next_action, log

    if not playing:
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

    topics = ["core", "fiction", "newspapers", "spoken", "web", "general"]
    topic_enquiry = [
        inquirer.List(
            "topic",
            message="Select a topic",
            choices=topics,
        )
    ]
    selected = inquirer.prompt(topic_enquiry)

    topic = selected["topic"]

    print(f"You have selected {topic.capitalize()}.")

    if topic == "core":
        lesson = vf.select_lesson(lo.core, test=True)
        total = 2 * len(lesson.questions)
        print(
            "\nBeginning test...\nType exit to end the test. All progress will be lost.\n"
        )
        correct, complete, log = vf.test(lesson)

    elif topic == "fiction":
        lesson = vf.select_lesson(lo.fiction, test=True)
        total = 2 * len(lesson.questions)
        print(
            "\nBeginning test...\nType exit to end the test. All progress will be lost.\n"
        )
        correct, complete, log = vf.test(lesson)

    elif topic == "newspapers":
        lesson = vf.select_lesson(lo.newspapers, test=True)
        total = 2 * len(lesson.questions)
        print(
            "\nBeginning test...\nType exit to end the test. All progress will be lost.\n"
        )
        correct, complete, log = vf.test(lesson)

    elif topic == "spoken":
        lesson = vf.select_lesson(lo.spoken, test=True)
        total = 2 * len(lesson.questions)
        print(
            "\nBeginning test...\nType exit to end the test. All progress will be lost.\n"
        )
        correct, complete, log = vf.test(lesson)

    elif topic == "web":
        lesson = vf.select_lesson(lo.web, test=True)
        total = 2 * len(lesson.questions)
        print(
            "\nBeginning test...\nType exit to end the test. All progress will be lost.\n"
        )
        correct, complete, log = vf.test(lesson)

    elif topic == "general":
        lesson = vf.select_lesson(lo.general, test=True)
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
