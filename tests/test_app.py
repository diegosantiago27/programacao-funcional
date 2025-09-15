from app.functional_core import (
    Task, add_task, filter_tasks, map_tasks, sort_tasks_by_title,
    summarize_effort_by_tag, make_title_prefixer, make_min_effort_predicate,
    complete_all_with_tag
)

def sample_tasks():
    return (
        Task(1, "Write docs", ("docs", "team"), effort=1),
        Task(2, "Fix bug", ("bug",), effort=3),
        Task(3, "Code review", ("team",), effort=2),
    )

def test_add_task():
    tasks = sample_tasks()
    new = Task(4, "Refactor", ("tech",), effort=2)
    updated = add_task(tasks, new)
    assert len(updated) == 4
    assert len(tasks) == 3  # imutabilidade

def test_filter_closure():
    tasks = sample_tasks()
    pred = make_min_effort_predicate(2)  # closure
    filtered = filter_tasks(tasks, pred)
    assert {t.id for t in filtered} == {2, 3}

def test_map_closure():
    tasks = sample_tasks()
    prefixer = make_title_prefixer("[HOT] ")  # closure
    mapped = map_tasks(tasks, prefixer)
    assert all(m.title.startswith("[HOT] ") for m in mapped)

def test_sort_lambda():
    tasks = sample_tasks()
    sorted_tasks = sort_tasks_by_title(tasks)
    assert [t.title for t in sorted_tasks] == ["Code review", "Fix bug", "Write docs"]

def test_list_comprehension_summary():
    tasks = sample_tasks()
    totals = summarize_effort_by_tag(tasks)
    assert totals["team"] == 3
    assert totals["bug"] == 3

def test_complete_hof():
    tasks = sample_tasks()
    done = complete_all_with_tag(tasks, "team")
    assert {t.id for t in done if t.done} == {1, 3}
