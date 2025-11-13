# Testing

from unittest import mock
from unittest import TestCase
from unittest import main
from io import StringIO
import contextlib
import vocab_functions
import lesson_objects
import copy


test_lesson_1 = lesson_objects.Lesson(1, "core")
test_lesson_1.add_question("voor", "for, in front of")

test_lesson_2 = lesson_objects.Lesson(2, "core")
test_lesson_2.add_question(
    "Hij geeft de bloemen aan Lena", "He gives the flowers to Lena"
)

test_lesson_3 = lesson_objects.Lesson(3, "core")
test_lesson_3.add_question(
    "We staan voor de deur van het hotel", "We stand in front of the hotel door"
)

test_lesson_4 = lesson_objects.Lesson(4, "core")
test_lesson_4.add_question(
    "Ik krijg dorst als ik die fles zie staan",
    "I get thirsty when I see that bottle standing there",
)

test_lesson_5 = lesson_objects.Lesson(5, "core")
test_lesson_5.add_question(
    "Alle informatie over de camping vind je op de website",
    "All the information about camping is on the website",
)

test_lesson_6 = lesson_objects.Lesson(6, "core")
test_lesson_6.add_question(
    "Na enkele seconden hoorde ik de auto ook",
    "After a few seconds I also heard the car",
)

test_lesson_7 = lesson_objects.Lesson(7, "core")
test_lesson_7.add_question(
    "Hij maakte haar kapotte fiets", "He repaired her broken bicycle"
)

test_lesson_8 = lesson_objects.Lesson(8, "core")
test_lesson_8.add_question("de mens", "human")

test_lesson_9 = lesson_objects.Lesson(9, "core")
test_lesson_9.add_question("de heleboel", "a lot")

test_lesson_10 = lesson_objects.Lesson(10, "core")
test_lesson_10.add_question(
    "Het hotel was gesloten van augustus tot april",
    "The hotel was closed from August to April",
)

test_lesson_11 = lesson_objects.Lesson(11, "core")
test_lesson_11.add_question(
    "Ze stond die eerste nacht met haar tentje op een soort dorpsplein",
    "She stood that first night with her tent on a kind of village square",
)

test_lesson_12 = lesson_objects.Lesson(12, "core")
test_lesson_12.add_question(
    "Bovendien betaalt de stad de energiefactuur", "The town also pays the energy bill"
)

test_lesson_13 = lesson_objects.Lesson(13, "core")
test_lesson_13.add_question(
    "We hebben twee leerkrachten Nederlands die één uur per week lesgeven aan anderstaligen",
    "We have two Dutch teachers who teach one hour per week to non-native speakers",
)

test_lesson_14 = lesson_objects.Lesson(14, "core")
test_lesson_14.add_question("willen het liefst", "to prefer")

test_lesson_15 = lesson_objects.Lesson(15, "web")
test_lesson_15.add_question("aangezien", "since")

test_lesson_16 = lesson_objects.Lesson(16, "newspapers")
test_lesson_16.add_question(
    "De hypotheekrente is momenteel aan het stijgen",
    "Mortgage rates are currently climbing",
)

test_lesson_17 = lesson_objects.Lesson(17, "core")
test_lesson_17.add_question("nog", "still")

test_lesson_18 = lesson_objects.Lesson(18, "core")
test_lesson_18.add_question(
    "Op het pleintje bij de kerk waren kinderen aan het spelen",
    "Children were playing on the square near the church",
)

test_lesson_19 = lesson_objects.Lesson(19, "core")
test_lesson_19.add_question(
    "Een stormvloed spoelde de hele stad in een keer weg, aldus de overlevering",
    "A storm surge washed away the whole city in one go, according to legend",
)

test_lesson_20 = lesson_objects.Lesson(20, "core")
test_lesson_20.add_question(
    "Eigenlijk ben ik daar wel benieuwd naar",
    "Actually I'm curious about that",
)

core = lesson_objects.Topic("core")
core.add_lesson(test_lesson_1)
core.add_lesson(test_lesson_2)


class Test(TestCase):

    @mock.patch("vocab_functions.input", create=True)
    def test_wrong_input(self, mocked_input):
        mocked_input.side_effect = ["sdf", "ihkjk", "1"]
        result = vocab_functions.select_lesson(core)
        expected_result = test_lesson_1
        self.assertEqual(str(result), str(expected_result))

    @mock.patch("vocab_functions.input", create=True)
    def test_capitalisation_ned1(self, mocked_input):
        mocked_input.side_effect = ["VoOr"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_1), 1, testing=1
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_capitalisation_eng1(self, mocked_input):
        mocked_input.side_effect = ["FOR, In front Of"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_1), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_capitalisation_ned2(self, mocked_input):
        mocked_input.side_effect = ["hij geeft de BLoemen aan lena"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_2), 1, testing=1
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_capitalisation_eng2(self, mocked_input):
        mocked_input.side_effect = ["He gives THE Flowers to lEna"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_2), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_capitalisation_eng3(self, mocked_input):
        mocked_input.side_effect = [
            "i get thirsty when i see that bottle standing there"
        ]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_4), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_capitalisation_ned3(self, mocked_input):
        mocked_input.side_effect = ["de Mens"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_8), 1, testing=1
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_capitalisation_eng4(self, mocked_input):
        mocked_input.side_effect = ["Human"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_8), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_capitalisation_ned4(self, mocked_input):
        mocked_input.side_effect = ["de heleboel"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_9), 1, testing=1
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_capitalisation_eng5(self, mocked_input):
        mocked_input.side_effect = ["to prefer"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_14), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_capitalisation_ned5(self, mocked_input):
        mocked_input.side_effect = ["willen het liefst"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_14), 1, testing=1
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_wij_we(self, mocked_input):
        mocked_input.side_effect = ["Wij staan voor de deur van het hotel"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_3), 1, testing=1
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_wij_we2(self, mocked_input):
        mocked_input.side_effect = ["We staan voor de deur van het hotel"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_3), 1, testing=1
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_zij_ze(self, mocked_input):
        mocked_input.side_effect = [
            "Zij stond die eerste nacht met haar tentje op een soort dorpsplein"
        ]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_11), 1, testing=1
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_meaning_order(self, mocked_input):
        mocked_input.side_effect = ["in front of, for"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_1), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_alternative_answer_eng(self, mocked_input):
        mocked_input.side_effect = [
            "All the information about camping can be found on the website"
        ]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_5), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_alternative_answer_ned(self, mocked_input):
        mocked_input.side_effect = ["Na enkele seconden hoorde ik ook de auto"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_6), 1, testing=1
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_alternative_answer_eng_multi(self, mocked_input):
        mocked_input.side_effect = [
            "He repaired her broken bike",
            "He fixed her broken bike",
            "He fixed her broken bicycle",
        ]
        result1 = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_7), 1, testing=0
        )
        result2 = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_7), 1, testing=0
        )
        result3 = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_7), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(
            (result1[0], result2[0], result3[0]),
            (expected_result, expected_result, expected_result),
        )

    @mock.patch("vocab_functions.input", create=True)
    def test_alternative_answer_eng_multi2(self, mocked_input):
        mocked_input.side_effect = [
            "Children were playing on the square near the church",
            "On the square near the church children were playing",
        ]
        result1 = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_18), 1, testing=0
        )
        result2 = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_18), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(
            (result1[0], result2[0]),
            (expected_result, expected_result),
        )

    @mock.patch("vocab_functions.input", create=True)
    def test_alternative_answer_eng_multi3(self, mocked_input):
        mocked_input.side_effect = [
            "A storm surge washed away the whole town in one go, according to legend",
            "A storm surge washed the whole town away in one go, according to legend",
            "A storm surge washed the whole city away in one go, according to legend",
        ]
        result1 = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_19), 1, testing=0
        )
        result2 = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_19), 1, testing=0
        )
        result3 = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_19), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(
            (result1[0], result2[0], result3[0]),
            (expected_result, expected_result, expected_result),
        )

    @mock.patch("vocab_functions.input", create=True)
    def test_ned(self, mocked_input):
        mocked_input.side_effect = ["Het hotel was gesloten van augustus tot april"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_10), 1, testing=1
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_eng1(self, mocked_input):
        mocked_input.side_effect = ["The hotel was closed from August to April"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_10), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_eng2(self, mocked_input):
        mocked_input.side_effect = ["The city also pays the energy bil"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_12), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_eng3(self, mocked_input):
        mocked_input.side_effect = [
            "WE have two Dutch teachers who teach one hour per week to non-native speakers"
        ]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_13), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    # test for incorrect answer not printing
    @mock.patch("vocab_functions.input", create=True)
    def test_stdout(self, mocked_input):

        mocked_input.side_effect = ["indien"]

        fake_output = StringIO()

        with contextlib.redirect_stdout(fake_output):
            result = vocab_functions.randomly_generated_lesson(
                copy.deepcopy(test_lesson_15), 1, testing=1
            )

        expected_result = 0
        self.assertEqual(result[0], expected_result)

        output = fake_output.getvalue()
        self.assertIn("That's not right!", output)

    # test for empty answer
    @mock.patch("vocab_functions.input", create=True)
    def test_empty(self, mocked_input):
        mocked_input.side_effect = [""]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_16), 1, testing=1
        )
        expected_result = 0
        self.assertEqual(result[0], expected_result)

    # test for typos
    @mock.patch("vocab_functions.input", create=True)
    def test_typo_eng1(self, mocked_input):
        mocked_input.side_effect = [
            "I get thisrty when I see that bottle standing there"
        ]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_4), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_typo_eng2(self, mocked_input):
        mocked_input.side_effect = ["stil"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_17), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_typo_eng3(self, mocked_input):
        mocked_input.side_effect = ["lot"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_9), 1, testing=0
        )
        expected_result = 0
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_order_eng1(self, mocked_input):
        mocked_input.side_effect = ["Mortgage rates are climbing currently"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_16), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_order_eng1(self, mocked_input):
        mocked_input.side_effect = ["Mortgage rates are climbing currentluy"]
        result = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_16), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(result[0], expected_result)

    @mock.patch("vocab_functions.input", create=True)
    def test_iam(self, mocked_input):
        mocked_input.side_effect = [
            "Actually I am curious about that",
            "Actually I'm curious about that",
        ]
        result1 = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_20), 1, testing=0
        )
        result2 = vocab_functions.randomly_generated_lesson(
            copy.deepcopy(test_lesson_20), 1, testing=0
        )
        expected_result = 1
        self.assertEqual(
            (result1[0], result2[0]),
            (expected_result, expected_result),
        )


if __name__ == "__main__":

    main()
