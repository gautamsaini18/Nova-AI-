"""Tests for Voice Profiles."""

from backend.modules.voice.voice_profiles import (
    DEFAULT_VOICE_ID,
    TOTAL_VOICES,
    VoiceCategory,
    VoiceGender,
    get_all_categories,
    get_voice_by_id,
    get_voices_by_category,
    voice_to_dict,
)


def test_total_voices():
    assert TOTAL_VOICES == 60


def test_default_voice_exists():
    voice = get_voice_by_id(DEFAULT_VOICE_ID)
    assert voice is not None
    assert voice.id == "nova"


def test_get_voice_by_id():
    voice = get_voice_by_id("maya")
    assert voice is not None
    assert voice.name == "Maya"
    assert voice.category == VoiceCategory.FRIENDLY_HUMAN
    assert voice.gender == VoiceGender.FEMALE


def test_get_voice_by_id_unknown():
    assert get_voice_by_id("nonexistent") is None


def test_get_voices_by_category():
    modern = get_voices_by_category(VoiceCategory.MODERN_PREMIUM)
    assert len(modern) == 10
    for v in modern:
        assert v.category == VoiceCategory.MODERN_PREMIUM


def test_get_all_categories():
    categories = get_all_categories()
    assert len(categories) == 6
    assert VoiceCategory.MODERN_PREMIUM.value in categories


def test_voice_to_dict():
    voice = get_voice_by_id("nova")
    d = voice_to_dict(voice)
    assert d["id"] == "nova"
    assert d["name"] == "Nova"
    assert d["category"] == VoiceCategory.MODERN_PREMIUM.value
    assert d["gender"] == VoiceGender.FEMALE.value
    assert d["is_premium"] is False


def test_premium_voices():
    voice = get_voice_by_id("aria")
    assert voice.is_premium is True


def test_all_voices_have_unique_ids():
    from backend.modules.voice.voice_profiles import VOICE_LIBRARY
    ids = [v.id for v in VOICE_LIBRARY]
    assert len(ids) == len(set(ids))


def test_all_voices_have_valid_openai_voice():
    from backend.modules.voice.voice_profiles import VOICE_LIBRARY
    valid_openai = {"nova", "shimmer", "alloy", "echo", "onyx", "fable"}
    for v in VOICE_LIBRARY:
        assert v.openai_voice in valid_openai, f"{v.id} has invalid openai_voice: {v.openai_voice}"
