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
import inquirer
import time
import re


def slow_print(text, char_delay=0.01, line_delay=0.2):
    """Print multi-line text at a consistent, slowed rate
    for easy readability, with a pause between lines."""
    for line in text.splitlines(keepends=True):
        for char in line:
            print(char, end="", flush=True)
            time.sleep(char_delay)
        time.sleep(line_delay)


def select_lesson(topic, test=False):
    trying = True
    available = [lesson for lesson in range(1, len(topic.lessons) + 1)]
    while trying:
        if not test:
            try:
                available.extend(["random", "all"])
                lesson_enquiry = [
                    inquirer.List(
                        "lesson",
                        message="Select a lesson, choose random for a random choice of lesson, or choose all for an assortment of questions from all lessons          ",
                        choices=available,
                    )
                ]
                selected = inquirer.prompt(lesson_enquiry)

                if selected["lesson"] == "random":
                    lesson_num = random.randrange((len(topic.lessons) - 1))
                    lesson = copy.deepcopy(topic.lessons[int(lesson_num) - 1])
                    print(
                        f"\nYou have chosen lesson {lesson.number} from {topic.name.capitalize()}."
                    )
                elif selected["lesson"] == "all":
                    lesson = copy.deepcopy(topic.all)
                    print(f"\nYou have chosen all of {topic.name.capitalize()}.")
                else:
                    lesson = copy.deepcopy(topic.lessons[int(selected["lesson"]) - 1])
                    print(
                        f"\nYou have chosen lesson {lesson.number} from {topic.name.capitalize()}."
                    )
                continue_with_lesson = input(
                    "\nPress Enter to accept this choice and continue, or type N to try again. Type X to cancel and exit.       "
                )
                if continue_with_lesson.upper() == "N":
                    continue
                elif continue_with_lesson.upper() == "X":
                    lesson = False
                    trying = False
                else:
                    trying = False
            except:
                print("\nInput not recognised. Please try again.\n")
                continue
        else:
            try:
                lesson_enquiry = [
                    inquirer.List(
                        "lesson",
                        message="Select a lesson to be tested on          ",
                        choices=available,
                    )
                ]
                selected = inquirer.prompt(lesson_enquiry)

                lesson = copy.deepcopy(topic.lessons[int(selected["lesson"]) - 1])
                print(
                    f"\nYou have chosen lesson {lesson.number} from {topic.name.capitalize()}."
                )
                continue_with_lesson = input(
                    "\nPress Enter to accept this choice and continue, or type N to try again.      "
                )
                if continue_with_lesson.upper() == "N":
                    continue
                else:
                    trying = False
            except:
                print("\nInput not recognised. Please try again.\n")
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

        answer_formatted = " ".join(word for word in answer_words)

        # check for wij/we, zij/ze, jij/je
        answer_formatted = accept_alternatives(correct_answer, answer_formatted)

    else:
        for word in lessons.proper_nouns_eng:
            if word.lower() in answer_words:
                index = answer_words.index(word.lower())
                answer_words[index] = word

        answer_words = ["I" if word == "i" else word for word in answer_words]
        if len(test.split()) > 2 and len(lesson.questions[test].split()) > 2:
            answer_words[0] = answer_words[0].capitalize()

        answer_formatted = " ".join(word for word in answer_words)

        if "I am" in answer_formatted:
            answer_formatted = answer_formatted.replace("I am", "I'm")

        if "town" in answer_formatted:
            answer_formatted = answer_formatted.replace("town", "city")

    return answer_formatted


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


def ignore_brackets(test):

    brackets = re.findall("\((.*?)\)", test)[0]

    return test.replace(f"({brackets})", "").strip()


def question(language, dutch, english, lesson, log=None, eng_typo=0, test=False):
    if language == 0:
        question = dutch
        correct_answer = english
    else:
        question = english
        correct_answer = dutch

    answer = input(f"{question}         ")
    if answer.lower() == "exit":
        return False
    if not answer:
        print("That's not right!")
        print(f"{correct_answer}\n")
        return 0, 0
    else:
        answer_formatted = answer_formatting(
            answer, question, lesson, language, correct_answer=correct_answer
        )
        result = check_answer(
            user_answer=answer_formatted,
            correct_answer=correct_answer,
            dutch_to_english=language,
            phrases=True,
            test=test,
            log=log,
            typo_count=eng_typo,
        )
        return result


def check_answer(
    user_answer,
    correct_answer,
    dutch_to_english,
    phrases,
    test=False,
    log=None,
    typo_count=0,
):

    # exact match
    if user_answer == correct_answer:
        print("Correct!\n")
        return update_results(correct=True, test=test, log=log, typo_count=typo_count)

    # typos in english
    if dutch_to_english:
        if typos_and_word_order(user_answer, correct_answer):
            (
                print("Correct! (You have a typo or different word order)")
                if phrases
                else print("Correct! (You have a typo)")
            )
            print(f"{correct_answer}\n")
            return update_results(
                correct=True,
                test=test,
                log=log,
                typo_count=typo_count + 1,
                error="Typo",
            )

    # handle brackets
    if "(" in correct_answer and "(zich)" not in correct_answer:
        updated_answer = ignore_brackets(correct_answer)
        if user_answer == updated_answer:
            print("Correct!")
            return update_results(
                correct=True, test=test, log=log, typo_count=typo_count
            )
        if dutch_to_english:
            if typos_and_word_order(user_answer, updated_answer):
                print("Correct! (You have a typo or different word order)")
                print(f"{correct_answer}\n")
                return update_results(
                    correct=True,
                    test=test,
                    log=log,
                    typo_count=typo_count + 1,
                    error="Typo",
                )

    # alternatives
    if correct_answer in lessons.alternatives.keys():
        alternatives = lessons.alternatives[correct_answer]
        # multiple alternatives
        if isinstance(alternatives, list):
            if user_answer in alternatives:
                print("Correct!\n")
                return update_results(
                    correct=True, test=test, log=log, typo_count=typo_count
                )
            if dutch_to_english:
                if any(typos_and_word_order(user_answer, alt) for alt in alternatives):
                    (
                        print("Correct! (You have a typo or different word order)")
                        if phrases
                        else print("Correct! (You have a typo)")
                    )
                    print(f"{correct_answer}\n")
                    return update_results(
                        correct=True,
                        test=test,
                        log=log,
                        typo_count=typo_count + 1,
                        error="Typo",
                    )
        # single alternative
        else:
            if user_answer == alternatives:
                print("Correct!\n")
                return update_results(
                    correct=True, test=test, log=log, typo_count=typo_count
                )
            if dutch_to_english:
                if typos_and_word_order(
                    user_answer,
                    alternatives,
                ):
                    (
                        print("Correct! (You have a typo or different word order)")
                        if phrases
                        else print("Correct! (You have a typo)")
                    )
                    print(f"{correct_answer}\n")
                    return update_results(
                        correct=True,
                        test=test,
                        log=log,
                        typo_count=typo_count + 1,
                        error="Typo",
                    )

    # no match
    print("That's not right!")
    print(f"{correct_answer}\n")
    return update_results(
        correct=False,
        test=test,
        log=log,
        typo_count=typo_count,
        error="Vocab/Understanding",
    )


def update_results(correct, test=False, log=None, typo_count=0, error="Ok"):
    if correct and not test:
        return 1, typo_count
    elif correct and test:
        log = pd.concat(
            [
                log,
                pd.DataFrame(
                    {"Result": "Correct", "Error": error},
                    index=pd.Index([date.today()]),
                ),
            ]
        )
        return 1, log
    elif test:
        log = pd.concat(
            [
                log,
                pd.DataFrame(
                    {"Result": "Incorrect", "Error": error},
                    index=pd.Index([date.today()]),
                ),
            ]
        )
        return 0, log
    return 0, typo_count


def dutch_question(answer_formatted, english, eng_typo=0, log=[], test=False):

    commas = answer_formatted.count(",")
    if commas == 1 and len(answer_formatted.split()) < 6 or commas > 1:
        answer_meanings = [item.strip() for item in answer_formatted.split(",")]
        test_meanings = [item.strip() for item in english.split(",")]
        if Counter(answer_meanings) == Counter(test_meanings):
            print("Correct!\n")
            if test:
                log = pd.concat(
                    [
                        log,
                        pd.DataFrame(
                            {"Result": "Correct", "Error": "Ok"},
                            index=pd.Index([date.today()]),
                        ),
                    ]
                )
                return 1, log
            else:
                return 1, 0
        else:
            print("That's not right!")
            print(f"{english}\n")
            if test:
                log = pd.concat(
                    [
                        log,
                        pd.DataFrame(
                            {"Result": "Incorrect", "Error": "Vocab/Understanding"},
                            index=pd.Index([date.today()]),
                        ),
                    ]
                )
                return 0, log
            else:
                return 0, 0

    result = check_answer(
        user_answer=answer_formatted,
        correct_answer=english,
        dutch_to_english=True,
        phrases=True,
        test=test,
        log=log,
        typo_count=eng_typo,
    )

    return result


def english_question(answer, dutch, english, lesson, log=[], test=False):

    answer_formatted = answer_formatting(answer, english, lesson, 1, dutch)

    # check for wij/we, zij/ze, jij/je
    answer = accept_alternatives(dutch, answer_formatted)

    result = check_answer(
        user_answer=answer,
        correct_answer=dutch,
        dutch_to_english=True,
        phrases=True,
        test=test,
        log=log,
    )

    return result


def dutch_word(answer, english, eng_typo):

    answer_words = answer.lower().split()
    answer_formatted = " ".join(word for word in answer_words)

    if any(True for char in answer_formatted if char in ","):
        answer_meanings = [item.strip() for item in answer_formatted.split(",")]
        test_meanings = [item.strip() for item in english.split(",")]
        if Counter(answer_meanings) == Counter(test_meanings):
            print("Correct!\n")
            return 1, 0
        else:
            print("That's not right!")
            print(f"{english}\n")
            return 0, 0

    result = check_answer(
        user_answer=answer_formatted,
        correct_answer=english,
        dutch_to_english=True,
        phrases=True,
        typo_count=eng_typo,
    )

    return result


def english_word(answer, dutch):

    answer_words = answer.lower().split()
    answer = " ".join(word for word in answer_words)

    result = check_answer(
        user_answer=answer,
        correct_answer=dutch,
        dutch_to_english=True,
        phrases=True,
    )

    return result


def randomly_generated_lesson(lesson, questions, testing=None):

    all_questions = list(lesson.questions.items())

    random.shuffle(all_questions)

    if questions < len(all_questions):
        all_questions = all_questions[:questions]
    elif questions > len(all_questions):
        extra = math.ceil(questions / len(all_questions)) - 1
        for _ in range(extra):
            extra_questions = list(lesson.questions.items())
            all_questions.extend(random.shuffle(extra_questions))

    correct = 0
    eng_typo = 0
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
                answer = answer_formatting(
                    answer, dutch, lesson, language, correct_answer=english
                )
                result = dutch_question(answer, english, eng_typo=eng_typo)
                correct += result[0]
                eng_typo += result[1]

        else:
            # English question
            result = question(language, dutch, english, lesson)
            if not result:
                questions = question_number - 1
                break
            correct += result[0]

        asked_questions.append((language, dutch, english))

        # count questions
        question_number += 1

    print(f"Lesson finished. You got {correct}/{questions} correct.")

    return correct, questions, asked_questions, eng_typo


def randomly_generated_vocab_lesson(lesson, words):

    all_questions = list(lesson.words.items())

    random.shuffle(all_questions)

    if words < len(all_questions):
        all_questions = all_questions[:words]
    elif words > len(all_questions):
        extra = math.ceil(words / len(all_questions)) - 1
        for _ in range(extra):
            extra_questions = list(lesson.words.items())
            all_questions.extend(random.shuffle(extra_questions))

    correct = 0
    eng_typo = 0
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
                result = dutch_word(answer, english, eng_typo)
                correct += result[0]
                eng_typo += result[1]

        else:
            # English question
            result = question(language, dutch, english, lesson)
            if not result:
                words = question_number - 1
                break
            correct += result[0]

        asked_questions.append((language, dutch, english))

        # count questions
        question_number += 1

    print(f"Lesson finished. You got {correct}/{words} correct.")

    return correct, words, asked_questions, eng_typo


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
                answer = answer_formatting(
                    answer, dutch, lesson, language, correct_answer=english
                )
                result = dutch_question(answer, english)
                correct += result[0]

        else:
            # English question
            result = question(language, dutch, english, lesson)
            if not result:
                questions = question_number - 1
                break
            correct += result[0]

        # count questions
        question_number += 1

    print(f"Lesson finished. You got {correct}/{questions} correct.")

    return correct, questions, all_questions


def test(lesson):

    log = pd.DataFrame(columns=["Result", "Error"])

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
                log = pd.concat(
                    [
                        log,
                        pd.DataFrame(
                            [{"Result": "Incorrect", "Error": "Attempted exit"}]
                        ),
                    ]
                )
                continue
            else:
                print("\nExiting...\n")
                return correct, complete, log
        if not answer:
            print("That's not right!")
            print(f"{dutch}\n")
            # default vocab/understanding until further development
            log = pd.concat(
                [
                    log,
                    pd.DataFrame(
                        [{"Result": "Incorrect", "Error": "Vocab/Understanding"}]
                    ),
                ]
            )
        else:
            result = english_question(answer, dutch, english, lesson, log, test=True)
            correct += result[0]
            log = result[1]

    random.shuffle(all_questions)

    for dutch, english in all_questions:
        answer = input(f"{dutch}         ")
        if answer.lower() == "exit":
            exit_confirm = input(
                "\nExiting test. All progress will be lost. Are you sure you wish to exit?   "
            )
            if exit_confirm.strip().lower() != "y":
                print("\nContinuing with test\n")
                log = pd.concat(
                    [
                        log,
                        pd.DataFrame(
                            [{"Result": "Incorrect", "Error": "Attempted exit"}]
                        ),
                    ]
                )
                continue
            else:
                print("\nExiting...\n")
                return correct, complete, log
        if not answer:
            print("That's not right!")
            print(f"{english}\n")
            log = pd.concat(
                [
                    log,
                    pd.DataFrame(
                        [{"Result": "Incorrect", "Error": "Vocab/Understanding"}]
                    ),
                ]
            )
        else:
            result = dutch_question(
                answer, correct, dutch, english, lesson, log=log, test=True
            )
            correct += result[0]
            log = result[1]

    complete = True

    return correct, complete, log


def update_log(log, topic, lesson, questions, correct, ltype, eng_typo):

    log_today = {
        "Module": topic,
        "Lesson": lesson,
        "Questions": questions,
        "Score": correct,
        "Type": ltype,
        "Typos English": eng_typo,
    }

    return pd.concat([log, pd.DataFrame(log_today, index=pd.Index([date.today()]))])


def visualisation_today(year=False, month=False, day=False):
    if year:
        chosen_date = date(year, month, day)
    else:
        chosen_date = date.today()

    log = pd.read_csv("learning_log.csv")
    log_today = log[log.Date == chosen_date.strftime("%Y-%m-%d")]

    log_today = log_today.groupby(["Type", "Module", "Lesson"], observed=True).agg(
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
