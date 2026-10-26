def build_graph(concepts):
    return {c["id"]: c["prerequisites"] for c in concepts}

def all_prerequisites(concept_id, graph):
    seen = set()
    stack = list(graph.get(concept_id, []))
    while stack:
        c = stack.pop()
        if c in seen:
            continue
        seen.add(c)
        stack.extend(graph.get(c, []))
    return seen

def find_weak_root(student_id, concept_id, graph, get_mastery, threshold=0.5):
    weak = []
    for p in all_prerequisites(concept_id, graph):
        m = get_mastery(student_id, p)
        if m < threshold:
            weak.append((m, p))
    if not weak:
        return None
    return min(weak)[1]