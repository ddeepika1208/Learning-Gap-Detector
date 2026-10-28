import pytest
from db import Base, engine
import mastery


@pytest.fixture(autouse=True)
def fresh_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


def test_new_student_starts_at_half():
    assert mastery.get_mastery("new", "pointers") == 0.5


def test_correct_easy_answer():
    assert mastery.update_mastery("s1", "loops", True, 1) == 0.575


def test_wrong_easy_answer():
    assert mastery.update_mastery("s1", "loops", False, 1) == 0.425


def test_hard_moves_more_than_easy():
    easy = mastery.update_mastery("a", "loops", True, 1)
    hard = mastery.update_mastery("b", "loops", True, 3)
    assert hard > easy


def test_all_correct_goes_up_but_never_above_1():
    m = 0.5
    for _ in range(50):
        m = mastery.update_mastery("s1", "loops", True, 3)
    assert 0.9 < m <= 1.0


def test_all_wrong_goes_down_but_never_below_0():
    m = 0.5
    for _ in range(50):
        m = mastery.update_mastery("s1", "loops", False, 3)
    assert 0.0 <= m < 0.1


def test_one_lucky_guess_is_not_mastery():
    m = mastery.update_mastery("s1", "loops", True, 1)
    assert m < 0.7


def test_concepts_are_independent():
    mastery.update_mastery("s1", "loops", True, 2)
    assert mastery.get_mastery("s1", "pointers") == 0.5


def test_students_are_independent():
    mastery.update_mastery("s1", "loops", True, 2)
    assert mastery.get_mastery("s2", "loops") == 0.5


def test_value_is_saved_in_database():
    mastery.update_mastery("s1", "loops", False, 2)
    assert mastery.get_mastery("s1", "loops") == 0.4


def test_all_mastery_returns_every_concept():
    concepts = [{"id": "a"}, {"id": "b"}]
    result = mastery.all_mastery("s1", concepts)
    assert [r["concept_id"] for r in result] == ["a", "b"]
    assert all(r["mastery"] == 0.5 for r in result)