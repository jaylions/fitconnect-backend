import numpy as np

from app.services.scoring import cosine, fuse_scores_100, score_pair_100, to_100


def test_cosine_handles_zero_norm_vector():
    u = np.zeros(3, dtype=np.float32)
    v = np.ones(3, dtype=np.float32)
    assert cosine(u, v) == 0.0


def test_to_100_clamps_values():
    assert to_100(2.0) == 100.0
    assert to_100(-2.0) == 0.0
    assert to_100(0.0) == 50.0


def test_fuse_scores_renormalizes_missing_facets():
    facet_cos = {"roles": 1.0}
    weights = {"roles": 0.7, "skills": 0.3}
    assert fuse_scores_100(facet_cos, weights, renorm_missing=True) == 100.0


def test_score_pair_100_returns_overall_and_facets():
    a = {
        "roles": np.array([1.0, 0.0, 0.0], dtype=np.float32),
        "skills": np.array([0.0, 1.0, 0.0], dtype=np.float32),
    }
    b = {
        "roles": np.array([1.0, 0.0, 0.0], dtype=np.float32),
        "skills": np.array([0.0, 1.0, 0.0], dtype=np.float32),
    }
    weights = {"roles": 0.6, "skills": 0.4}
    result = score_pair_100(a, b, weights)
    assert result["overall"]["score_100"] == 100.0
    assert result["facets"]["roles"]["score_100"] == 100.0
