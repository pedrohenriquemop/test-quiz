import pytest
from model import Question, Choice


def test_create_question():
    question = Question(title="q1")
    assert question.id != None


def test_create_multiple_questions():
    question1 = Question(title="q1")
    question2 = Question(title="q2")
    assert question1.id != question2.id


def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title="")
    with pytest.raises(Exception):
        Question(title="a" * 201)
    with pytest.raises(Exception):
        Question(title="a" * 500)


def test_create_question_with_valid_points():
    question = Question(title="q1", points=1)
    assert question.points == 1
    question = Question(title="q1", points=100)
    assert question.points == 100


def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title="q1", points=-1)
    with pytest.raises(Exception):
        Question(title="q1", points=101)


def test_add_choice():
    question = Question(title="q1")

    question.add_choice("a", False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == "a"
    assert not choice.is_correct


def test_remove_choice_by_id():
    question = Question(title="q1")

    question.add_choice("a", False)
    question.add_choice("b", True)

    assert len(question.choices) == 2

    question.remove_choice_by_id(question.choices[0].id)

    assert len(question.choices) == 1


def test_remove_all_choices():
    question = Question(title="q1")

    question.add_choice("a", False)
    question.add_choice("b", True)

    assert len(question.choices) == 2

    question.remove_all_choices()

    assert len(question.choices) == 0


def test_create_choice():
    choice = Choice(1, "Choice 1", True)
    assert choice.id == 1
    assert choice.text == "Choice 1"
    assert choice.is_correct == True

    choice = Choice(2, "Choice 2", False)
    assert choice.id == 2
    assert choice.text == "Choice 2"
    assert choice.is_correct == False


def test_create_choice_with_no_text():
    with pytest.raises(Exception):
        Choice(1, "", True)


def test_create_choice_with_long_text():
    with pytest.raises(Exception):
        Choice(
            1,
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc sed pretium eros, ac malesuada dui. In efficitur efficitur ipsum eget viverra.",
            True,
        )


def test_set_correct_choices():
    question = Question(title="q1", max_selections=2)

    choice1 = question.add_choice("a", False)
    choice2 = question.add_choice("b", False)
    choice3 = question.add_choice("c", False)

    question.set_correct_choices([choice1.id, choice2.id])

    assert choice1.is_correct == True
    assert choice2.is_correct == True
    assert choice3.is_correct == False


def test_set_correct_choices_with_invalid_id():
    question = Question(title="q1", max_selections=2)

    with pytest.raises(Exception):
        question.set_correct_choices([451])


def test_correct_selected_choices():
    question = Question(title="q1", max_selections=2)

    choice1 = question.add_choice("a", True)
    question.add_choice("b", True)
    choice3 = question.add_choice("c", False)

    correct_choices = question.correct_selected_choices([choice1.id, choice3.id])

    assert correct_choices == [choice1.id]


def test_correct_selected_choices_no_correct_choices():
    question = Question(title="q1", max_selections=2)

    choice1 = question.add_choice("a", False)
    question.add_choice("b", True)
    choice3 = question.add_choice("c", False)

    correct_choices = question.correct_selected_choices([choice1.id, choice3.id])

    assert correct_choices == []


def test_correct_selected_choices_with_more_than_max_selections():
    question = Question(title="q1", max_selections=1)

    choice1 = question.add_choice("a", False)
    question.add_choice("b", True)
    choice3 = question.add_choice("c", False)

    with pytest.raises(Exception):
        question.correct_selected_choices([choice1.id, choice3.id])
