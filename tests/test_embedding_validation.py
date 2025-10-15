import math

import numpy as np
import pytest

from app.services.embedding_validation import (
    EmbeddingValidationError,
    ensure_f32_unit,
    validate_embedding_payload,
)


def test_ensure_f32_unit_normalised_vector():
    dim = 4
    value = [0.5, 0.5, 0.5, 0.5]
    result = ensure_f32_unit(value, dim=dim)
    assert isinstance(result, np.ndarray)
    assert pytest.approx(float(np.linalg.norm(result)), rel=1e-6, abs=1e-6) == 1.0


def test_ensure_f32_unit_rejects_invalid_dimension():
    with pytest.raises(EmbeddingValidationError):
        ensure_f32_unit([0.1, 0.2], dim=4)


def test_validate_embedding_payload_normalises_and_flags():
    dim = 4
    payload = {"embedding": [2.0, 0.0, 0.0, 0.0]}
    result = validate_embedding_payload(payload, dim=dim)
    assert pytest.approx(float(np.linalg.norm(result.vector)), rel=1e-6, abs=1e-6) == 1.0
    assert result.was_normalized is True


def test_ensure_f32_unit_rejects_non_finite():
    dim = 4
    payload = [math.nan, 0.0, 0.0, 0.0]
    with pytest.raises(EmbeddingValidationError):
        ensure_f32_unit(payload, dim=dim)
