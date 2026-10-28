from graph import all_prerequisites, find_weak_root, build_graph

CONCEPTS = [
    {"id": "a", "prerequisites": []},
    {"id": "b", "prerequisites": ["a"]},
    {"id": "c", "prerequisites": ["b"]},
]


def test_all_prerequisites_chain():
    g = build_graph(CONCEPTS)
    assert all_prerequisites("c", g) == {"a", "b"}


def test_no_prerequisites():
    g = build_graph(CONCEPTS)
    assert all_prerequisites("a", g) == set()


def test_unknown_concept():
    g = build_graph(CONCEPTS)
    assert all_prerequisites("zzz", g) == set()


def test_cycle_does_not_loop_forever():
    g = {"x": ["y"], "y": ["x"]}
    assert all_prerequisites("x", g) == {"x", "y"}


def test_find_weak_root_picks_lowest():
    g = build_graph(CONCEPTS)
    scores = {"a": 0.2, "b": 0.4}
    weak = find_weak_root("s1", "c", g, lambda s, c: scores.get(c, 0.5))
    assert weak == "a"


def test_find_weak_root_none_when_strong():
    g = build_graph(CONCEPTS)
    weak = find_weak_root("s1", "c", g, lambda s, c: 0.9)
    assert weak is None