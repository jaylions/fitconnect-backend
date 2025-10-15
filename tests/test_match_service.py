import numpy as np

from app.services.match_service import (
    all_for_job,
    all_for_talent,
    topk_for_job,
    topk_for_talent,
)


def _unit(axis: int, dim: int = 3) -> np.ndarray:
    vec = np.zeros(dim, dtype=np.float32)
    vec[axis] = 1.0
    return vec


def _weights():
    return {"roles": 0.7, "skills": 0.3}


def test_topk_for_job_orders_by_score():
    job_vecs = {"roles": _unit(0), "skills": _unit(1)}
    candidates = [
        {"talent_id": 1, "roles": _unit(0), "skills": _unit(1)},
        {"talent_id": 2, "roles": _unit(0), "skills": np.zeros(3, dtype=np.float32)},
        {"talent_id": 3, "roles": -_unit(0), "skills": np.zeros(3, dtype=np.float32)},
    ]

    rows = topk_for_job(job_vecs, candidates, _weights(), top_k=3)
    assert [row["talent_id"] for row in rows] == [1, 2, 3]
    assert rows[0]["overall"]["score_100"] == 100.0


def test_all_for_job_pagination():
    job_vecs = {"roles": _unit(0)}
    candidates = [
        {"talent_id": 10, "roles": _unit(0)},
        {"talent_id": 11, "roles": _unit(0)},
        {"talent_id": 12, "roles": -_unit(0)},
    ]

    rows, total = all_for_job(job_vecs, candidates, _weights(), limit=1, offset=1)
    assert total == 3
    assert len(rows) == 1
    assert rows[0]["talent_id"] == 11


def test_topk_for_talent_mirrors_job_direction():
    talent_vecs = {"roles": _unit(0), "skills": _unit(1)}
    jobs = [
        {"job_id": 5, "roles": _unit(0), "skills": _unit(1)},
        {"job_id": 6, "roles": _unit(0)},
        {"job_id": 7, "roles": -_unit(0)},
    ]

    rows = topk_for_talent(talent_vecs, jobs, _weights(), top_k=3)
    assert [row["job_id"] for row in rows] == [5, 6, 7]


def test_all_for_talent_pagination():
    talent_vecs = {"roles": _unit(0)}
    jobs = [
        {"job_id": 20, "roles": _unit(0)},
        {"job_id": 30, "roles": _unit(0)},
        {"job_id": 40, "roles": _unit(0)},
    ]

    rows, total = all_for_talent(talent_vecs, jobs, _weights(), limit=2, offset=1)
    assert total == 3
    assert [row["job_id"] for row in rows] == [30, 40]
