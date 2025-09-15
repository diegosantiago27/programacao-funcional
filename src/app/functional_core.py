from dataclasses import dataclass, replace
from typing import Callable, Tuple, Dict

# ---------- Modelo de domínio (imutável) ----------
@dataclass(frozen=True)
class Task:
    id: int
    title: str
    tags: Tuple[str, ...] = ()
    done: bool = False
    effort: int = 1

Tasks = Tuple[Task, ...]

# ---------- Funções funcionais ----------
def add_task(tasks: Tasks, new_task: Task) -> Tasks:
    return tasks + (new_task,)

def map_tasks(tasks: Tasks, transform: Callable[[Task], Task]) -> Tasks:
    return tuple(transform(t) for t in tasks)  # HOF + imutável

def filter_tasks(tasks: Tasks, predicate: Callable[[Task], bool]) -> Tasks:
    return tuple(t for t in tasks if predicate(t))  # HOF + list comp

def sort_tasks_by_title(tasks: Tasks) -> Tasks:
    return tuple(sorted(tasks, key=lambda t: t.title.lower()))  # lambda

def summarize_effort_by_tag(tasks: Tasks) -> Dict[str, int]:
    # list comp que “achata” tags e carrega esforço
    tag_effort_pairs = [(tag, t.effort) for t in tasks for tag in t.tags]
    totals: Dict[str, int] = {}
    for tag, effort in tag_effort_pairs:
        totals[tag] = totals.get(tag, 0) + effort
    return totals

# ---------- Closures ----------
def make_title_prefixer(prefix: str) -> Callable[[Task], Task]:
    def _prefixer(t: Task) -> Task:
        return replace(t, title=f"{prefix}{t.title}")
    return _prefixer

def make_min_effort_predicate(min_effort: int) -> Callable[[Task], bool]:
    return lambda t: t.effort >= min_effort  # closure + lambda

# ---------- Exemplo HOF extra ----------
def complete_all_with_tag(tasks: Tasks, tag: str) -> Tasks:
    def mark_done_if_tagged(t: Task) -> Task:
        return replace(t, done=True) if tag in t.tags else t
    return map_tasks(tasks, mark_done_if_tagged)
