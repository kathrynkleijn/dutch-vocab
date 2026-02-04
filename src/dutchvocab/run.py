import random
from dutchvocab import lessons as lessons
import copy
from dutchvocab import vocab_functions as vf
import pandas as pd
from dutchvocab import lesson_objects as lo
from dutchvocab import pdf_constructor
from dutchvocab import figure_generator as fg
from datetime import date, timedelta
import os
import inquirer


def main():

    # get settings
    with open("settings.txt", "r") as file:
        settings = file.read().splitlines()
    report_path = settings[0]
    report_output = settings[2]

    if report_path and not report_path.endswith("/"):
        report_path = report_path + "/"

    options = ["Practice", "Test"]
    select_setting = [
        inquirer.List("type", message="Select type of lesson", choices=options)
    ]
    selected = inquirer.prompt(select_setting)

    if selected["type"] == "Practice":

        # Practice
        print(
            "\nYou have chosen practice mode. You can now choose from any of the available lessons to practice a mixture of words and phrases.\n\n"
        )

        playing = True
        log = pd.DataFrame(columns=["Module", "Lesson", "Questions", "Score"])
        while playing:

            print(f"Available lessons:\n {lo.available}\n\n")

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
                    print("Exiting lessons...")
                    playing = False
                    break
                elif continue_with_topic.upper() == "N":
                    continue
                else:
                    choosing = False

            if not playing:
                break

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
                    break

                if ltype == "phrases":
                    questions = vf.select_questions(lesson)

                    correct, questions, asked_questions, eng_typo = (
                        vf.randomly_generated_lesson(lesson, questions)
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype, eng_typo
                    )

                elif ltype == "vocabulary":
                    words = vf.select_words(lesson)

                    correct, questions, asked_questions, eng_typo = (
                        vf.randomly_generated_vocab_lesson(lesson, words)
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype, eng_typo
                    )

            elif topic == "fiction":
                lesson = vf.select_lesson(lo.fiction)
                if not lesson:
                    break

                if ltype == "phrases":
                    questions = vf.select_questions(lesson)

                    correct, questions, asked_questions = vf.randomly_generated_lesson(
                        lesson, questions
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype
                    )

                elif ltype == "vocabulary":
                    words = vf.select_words(lesson)

                    correct, questions, asked_questions = (
                        vf.randomly_generated_vocab_lesson(lesson, words)
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype
                    )

            elif topic == "newspapers":
                lesson = vf.select_lesson(lo.newspapers)
                if not lesson:
                    break

                if ltype == "phrases":
                    questions = vf.select_questions(lesson)

                    correct, questions, asked_questions = vf.randomly_generated_lesson(
                        lesson, questions
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype
                    )

                elif ltype == "vocabulary":
                    words = vf.select_words(lesson)

                    correct, questions, asked_questions = (
                        vf.randomly_generated_vocab_lesson(lesson, words)
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype
                    )

            elif topic == "spoken":
                lesson = vf.select_lesson(lo.spoken)
                if not lesson:
                    break

                if ltype == "phrases":
                    questions = vf.select_questions(lesson)

                    correct, questions, asked_questions = vf.randomly_generated_lesson(
                        lesson, questions
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype
                    )

                elif ltype == "vocabulary":
                    words = vf.select_words(lesson)

                    correct, questions, asked_questions = (
                        vf.randomly_generated_vocab_lesson(lesson, words)
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype
                    )

            elif topic == "web":
                lesson = vf.select_lesson(lo.web)
                if not lesson:
                    break

                if ltype == "phrases":
                    questions = vf.select_questions(lesson)

                    correct, questions, asked_questions = vf.randomly_generated_lesson(
                        lesson, questions
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype
                    )

                elif ltype == "vocabulary":
                    words = vf.select_words(lesson)

                    correct, questions, asked_questions = (
                        vf.randomly_generated_vocab_lesson(lesson, words)
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype
                    )

            elif topic == "general":
                lesson = vf.select_lesson(lo.general)
                if not lesson:
                    break

                if ltype == "phrases":
                    questions = vf.select_questions(lesson)

                    correct, questions, asked_questions = vf.randomly_generated_lesson(
                        lesson, questions
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype
                    )

                elif ltype == "vocabulary":
                    words = vf.select_words(lesson)

                    correct, questions, asked_questions = (
                        vf.randomly_generated_vocab_lesson(lesson, words)
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype
                    )

            elif topic == "all":
                lesson = lo.all.all
                if ltype == "phrases":
                    questions = vf.select_questions(lesson)

                    correct, questions, asked_questions = vf.randomly_generated_lesson(
                        lesson, questions
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype
                    )

                elif ltype == "vocabulary":
                    words = vf.select_words(lesson)

                    correct, questions, asked_questions = (
                        vf.randomly_generated_vocab_lesson(lesson, words)
                    )
                    log = vf.update_log(
                        log, topic, lesson.name, questions, correct, ltype
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
                        if topic == "core":
                            lesson = copy.deepcopy(
                                lo.core.lessons[int(lesson.number) - 1]
                            )
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
                            lesson = copy.deepcopy(
                                lo.web.lessons[int(lesson.number) - 1]
                            )
                        elif topic == "general":
                            lesson = copy.deepcopy(
                                lo.general.lessons[int(lesson.number) - 1]
                            )
                        correct, questions, asked_questions = vf.repeated_lesson(
                            lesson, questions, all_questions=asked_questions
                        )
                        log = vf.update_log(
                            log, topic, lesson.name, questions, correct, ltype
                        )
                except ZeroDivisionError:
                    pass

            again = input("\nWould you like to do another lesson?  (Y/N)       ")
            if again.upper() != "Y":
                playing = False
                print("\nEnd of lessons")

        if os.path.isfile("learning_log.csv"):
            log.to_csv("learning_log.csv", mode="a", header=False)
        else:
            log.to_csv(
                "learning_log.csv",
                mode="a",
                header=True,
                index=True,
                index_label="Date",
            )
        vf.visualisation_today()

        # generate weekly/monthly report, ask about progress report
        if report_output == "Yes":
            print("\nUpdating reports...")

            # make directories if non-existent
            os.makedirs(f"{report_path}Reports/Weekly_Reports", exist_ok=True)
            os.makedirs(f"{report_path}Reports/Monthly_Reports", exist_ok=True)

            log_full = pd.read_csv("learning_log.csv")
            weekly_pdf = pdf_constructor.build_pdf(log_full, "Weekly")
            weekly_pdf.output(
                f"{report_path}Reports/Weekly_Reports/{(date.today() - timedelta(days=date.today().weekday())).strftime('%Y%m%d')}_Report.pdf",
                "F",
            )
            monthly_pdf = pdf_constructor.build_pdf(log_full, "Monthly")

            monthly_pdf.output(
                f"{report_path}Reports/Monthly_Reports/{date.today().strftime('%Y_%B')}_Report.pdf",
                "F",
            )

            print("\nWeekly and monthly reports updated.")
        # progress = input("Would you like to generate a progress report?  (Y/N)       ")
        # if progress == "Y":
        # make directories if non-existent
        #     os.makedirs(f"{report_path}/Reports/Progress_Reports", exist_ok=True)
        #     pdf = pdf_constructor.build_pdf(log_full, "Progress")
        #     pdf.output(
        #         f"Reports/Progress_Reports/{date.today().strftime('%Y%m%d')}_Report.pdf",
        #         "F",
        #     )
        #     print("Progress report completed.")

    elif selected["type"] == "Test":

        # Test
        print(
            "You have chosen test mode. You can choose to be tested on any of the available lessons. You will be given each word or phrase in English to translate first, then each in Dutch.\n\n"  # A report will be given at the end of the test."
        )

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

            print("\nBeginning test...\n")
            correct, complete, log = vf.test(lesson)

        elif topic == "fiction":
            lesson = vf.select_lesson(lo.fiction, test=True)

            print("\nBeginning test...\n")
            correct, complete, log = vf.test(lesson)

        elif topic == "newspapers":
            lesson = vf.select_lesson(lo.newspapers, test=True)
            print("\nBeginning test...\n")
            correct, complete, log = vf.test(lesson)

        elif topic == "spoken":
            lesson = vf.select_lesson(lo.spoken, test=True)
            print("\nBeginning test...\n")
            correct, complete, log = vf.test(lesson)

        elif topic == "web":
            lesson = vf.select_lesson(lo.web, test=True)
            print("\nBeginning test...\n")
            correct, complete, log = vf.test(lesson)

        elif topic == "general":
            lesson = vf.select_lesson(lo.general, test=True)
            print("\nBeginning test...\n")
            correct, complete, log = vf.test(lesson)

        if complete:
            print(
                f"Your test score for {topic.capitalize()} lesson {lesson} is {correct}."
            )
            fg.generate_test_figures(log)


if __name__ == "__main__":
    main()
