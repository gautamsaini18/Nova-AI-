"""
Nova AI — Voice Profiles
Defines all 50+ voice options across 6 categories.
Each profile maps to OpenAI TTS voices, ElevenLabs voice IDs,
and metadata for the frontend voice selector.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class VoiceCategory(str, Enum):
    MODERN_PREMIUM = "Modern & Premium"
    FRIENDLY_HUMAN = "Friendly & Human"
    FUTURISTIC = "Futuristic"
    TECH_INSPIRED = "Tech-Inspired"
    SHORT_EASY = "Short & Easy to Remember"
    POWERFUL_AI_BRAND = "Powerful AI Brand Names"


class VoiceGender(str, Enum):
    FEMALE = "female"
    MALE = "male"
    NEUTRAL = "neutral"


@dataclass
class VoiceProfile:
    id: str                          # Unique voice identifier (slug)
    name: str                        # Display name
    category: VoiceCategory
    gender: VoiceGender
    description: str                 # Short tagline shown in UI
    openai_voice: str                # OpenAI TTS voice mapping
    elevenlabs_voice_id: Optional[str] = None   # ElevenLabs voice ID
    sample_text: str = "Hello! I'm Nova AI, your intelligent voice assistant. How can I help you today?"
    tags: List[str] = field(default_factory=list)
    is_premium: bool = False         # Whether it requires premium plan


# ── Voice Library ─────────────────────────────────────────────────────────────

VOICE_LIBRARY: List[VoiceProfile] = [

    # ─── Modern & Premium ──────────────────────────────────────────────────
    VoiceProfile(
        id="nova", name="Nova", category=VoiceCategory.MODERN_PREMIUM,
        gender=VoiceGender.FEMALE, openai_voice="nova",
        description="Crisp, modern, and articulate. The default Nova AI voice.",
        tags=["popular", "clear", "default"],
    ),
    VoiceProfile(
        id="aria", name="Aria", category=VoiceCategory.MODERN_PREMIUM,
        gender=VoiceGender.FEMALE, openai_voice="shimmer",
        description="Elegant and expressive with a warm professional tone.",
        tags=["elegant", "warm"], is_premium=True,
    ),
    VoiceProfile(
        id="lyra", name="Lyra", category=VoiceCategory.MODERN_PREMIUM,
        gender=VoiceGender.FEMALE, openai_voice="alloy",
        description="Smooth and melodic — inspired by the constellation.",
        tags=["smooth", "melodic"],
    ),
    VoiceProfile(
        id="kaia", name="Kaia", category=VoiceCategory.MODERN_PREMIUM,
        gender=VoiceGender.FEMALE, openai_voice="nova",
        description="Bold and confident with a modern edge.",
        tags=["bold", "confident"], is_premium=True,
    ),
    VoiceProfile(
        id="nexa", name="Nexa", category=VoiceCategory.MODERN_PREMIUM,
        gender=VoiceGender.FEMALE, openai_voice="shimmer",
        description="Next-generation clarity with a futuristic undertone.",
        tags=["futuristic", "clear"],
    ),
    VoiceProfile(
        id="ziva", name="Ziva", category=VoiceCategory.MODERN_PREMIUM,
        gender=VoiceGender.FEMALE, openai_voice="alloy",
        description="Energetic and dynamic, perfect for productivity.",
        tags=["energetic", "dynamic"],
    ),
    VoiceProfile(
        id="elio", name="Elio", category=VoiceCategory.MODERN_PREMIUM,
        gender=VoiceGender.MALE, openai_voice="echo",
        description="Deep and authoritative with a premium finish.",
        tags=["deep", "authoritative"], is_premium=True,
    ),
    VoiceProfile(
        id="aven", name="Aven", category=VoiceCategory.MODERN_PREMIUM,
        gender=VoiceGender.MALE, openai_voice="onyx",
        description="Calm, collected, and distinctly modern.",
        tags=["calm", "collected"],
    ),
    VoiceProfile(
        id="orion", name="Orion", category=VoiceCategory.MODERN_PREMIUM,
        gender=VoiceGender.MALE, openai_voice="fable",
        description="Resonant and trustworthy — stellar clarity.",
        tags=["resonant", "trustworthy"],
    ),
    VoiceProfile(
        id="solis", name="Solis", category=VoiceCategory.MODERN_PREMIUM,
        gender=VoiceGender.NEUTRAL, openai_voice="alloy",
        description="Bright and balanced like sunlight. Genderless warmth.",
        tags=["bright", "balanced"],
    ),

    # ─── Friendly & Human ──────────────────────────────────────────────────
    VoiceProfile(
        id="maya", name="Maya", category=VoiceCategory.FRIENDLY_HUMAN,
        gender=VoiceGender.FEMALE, openai_voice="shimmer",
        description="Warm, caring, and endlessly patient. Like a best friend.",
        tags=["warm", "friendly", "popular"],
    ),
    VoiceProfile(
        id="ava", name="Ava", category=VoiceCategory.FRIENDLY_HUMAN,
        gender=VoiceGender.FEMALE, openai_voice="nova",
        description="Sweet and helpful with natural conversational flow.",
        tags=["sweet", "natural"],
    ),
    VoiceProfile(
        id="luna", name="Luna", category=VoiceCategory.FRIENDLY_HUMAN,
        gender=VoiceGender.FEMALE, openai_voice="alloy",
        description="Gentle and soothing — perfect for late-night chats.",
        tags=["gentle", "soothing"],
    ),
    VoiceProfile(
        id="mia", name="Mia", category=VoiceCategory.FRIENDLY_HUMAN,
        gender=VoiceGender.FEMALE, openai_voice="shimmer",
        description="Cheerful and upbeat. Makes every interaction enjoyable.",
        tags=["cheerful", "upbeat"],
    ),
    VoiceProfile(
        id="zoe", name="Zoe", category=VoiceCategory.FRIENDLY_HUMAN,
        gender=VoiceGender.FEMALE, openai_voice="nova",
        description="Playful and fun with a bright, youthful personality.",
        tags=["playful", "fun"],
    ),
    VoiceProfile(
        id="emma", name="Emma", category=VoiceCategory.FRIENDLY_HUMAN,
        gender=VoiceGender.FEMALE, openai_voice="alloy",
        description="Professional yet approachable. Classic and reliable.",
        tags=["professional", "classic"],
    ),
    VoiceProfile(
        id="leo", name="Leo", category=VoiceCategory.FRIENDLY_HUMAN,
        gender=VoiceGender.MALE, openai_voice="echo",
        description="Friendly and enthusiastic — always ready to help.",
        tags=["friendly", "enthusiastic"],
    ),
    VoiceProfile(
        id="noah", name="Noah", category=VoiceCategory.FRIENDLY_HUMAN,
        gender=VoiceGender.MALE, openai_voice="onyx",
        description="Calm and thoughtful with genuine human warmth.",
        tags=["calm", "thoughtful"],
    ),
    VoiceProfile(
        id="ivy", name="Ivy", category=VoiceCategory.FRIENDLY_HUMAN,
        gender=VoiceGender.FEMALE, openai_voice="shimmer",
        description="Soft-spoken and kind with excellent clarity.",
        tags=["soft", "kind"],
    ),
    VoiceProfile(
        id="theo", name="Theo", category=VoiceCategory.FRIENDLY_HUMAN,
        gender=VoiceGender.MALE, openai_voice="fable",
        description="Laid-back and likeable. Like chatting with a buddy.",
        tags=["relaxed", "likeable"],
    ),

    # ─── Futuristic ────────────────────────────────────────────────────────
    VoiceProfile(
        id="syna", name="Syna", category=VoiceCategory.FUTURISTIC,
        gender=VoiceGender.FEMALE, openai_voice="nova",
        description="Synth-inspired, otherworldly, and mesmerizing.",
        tags=["synth", "otherworldly"], is_premium=True,
    ),
    VoiceProfile(
        id="voxa", name="Voxa", category=VoiceCategory.FUTURISTIC,
        gender=VoiceGender.FEMALE, openai_voice="shimmer",
        description="Crisp digital tones with a futuristic edge.",
        tags=["digital", "futuristic"],
    ),
    VoiceProfile(
        id="neura", name="Neura", category=VoiceCategory.FUTURISTIC,
        gender=VoiceGender.FEMALE, openai_voice="alloy",
        description="Neural-network inspired. Precise and intelligent.",
        tags=["neural", "precise"], is_premium=True,
    ),
    VoiceProfile(
        id="quantix", name="Quantix", category=VoiceCategory.FUTURISTIC,
        gender=VoiceGender.NEUTRAL, openai_voice="echo",
        description="Quantum-speed communication with sci-fi flair.",
        tags=["quantum", "sci-fi"],
    ),
    VoiceProfile(
        id="aether", name="Aether", category=VoiceCategory.FUTURISTIC,
        gender=VoiceGender.NEUTRAL, openai_voice="alloy",
        description="Ethereal, weightless, and infinitely calm.",
        tags=["ethereal", "calm"],
    ),
    VoiceProfile(
        id="zenox", name="Zenox", category=VoiceCategory.FUTURISTIC,
        gender=VoiceGender.MALE, openai_voice="onyx",
        description="Zero-latency clarity with an alien precision.",
        tags=["precise", "alien"], is_premium=True,
    ),
    VoiceProfile(
        id="nexis", name="Nexis", category=VoiceCategory.FUTURISTIC,
        gender=VoiceGender.FEMALE, openai_voice="nova",
        description="Connected and relentless — the next evolution.",
        tags=["connected", "evolved"],
    ),
    VoiceProfile(
        id="kairo", name="Kairo", category=VoiceCategory.FUTURISTIC,
        gender=VoiceGender.MALE, openai_voice="fable",
        description="Cairo-inspired ancient wisdom meets future tech.",
        tags=["wise", "ancient"],
    ),
    VoiceProfile(
        id="xyra", name="Xyra", category=VoiceCategory.FUTURISTIC,
        gender=VoiceGender.FEMALE, openai_voice="shimmer",
        description="Extraterrestrial tones, beautifully articulate.",
        tags=["exotic", "articulate"], is_premium=True,
    ),
    VoiceProfile(
        id="vexa", name="Vexa", category=VoiceCategory.FUTURISTIC,
        gender=VoiceGender.FEMALE, openai_voice="alloy",
        description="Vector-precise, digitally enhanced voice.",
        tags=["precise", "digital"],
    ),

    # ─── Tech-Inspired ─────────────────────────────────────────────────────
    VoiceProfile(
        id="cortex", name="Cortex", category=VoiceCategory.TECH_INSPIRED,
        gender=VoiceGender.MALE, openai_voice="onyx",
        description="Deep, commanding — like your brain's CEO.",
        tags=["commanding", "deep"], is_premium=True,
    ),
    VoiceProfile(
        id="nexus", name="Nexus", category=VoiceCategory.TECH_INSPIRED,
        gender=VoiceGender.MALE, openai_voice="echo",
        description="The hub of all knowledge. Clear and central.",
        tags=["central", "knowledgeable"],
    ),
    VoiceProfile(
        id="pixel", name="Pixel", category=VoiceCategory.TECH_INSPIRED,
        gender=VoiceGender.FEMALE, openai_voice="nova",
        description="Sharp and precise, pixel-perfect delivery.",
        tags=["sharp", "precise"],
    ),
    VoiceProfile(
        id="echo", name="Echo", category=VoiceCategory.TECH_INSPIRED,
        gender=VoiceGender.NEUTRAL, openai_voice="echo",
        description="Resonant, clear echoes of intelligence.",
        tags=["resonant", "clear"],
    ),
    VoiceProfile(
        id="prism", name="Prism", category=VoiceCategory.TECH_INSPIRED,
        gender=VoiceGender.FEMALE, openai_voice="shimmer",
        description="Multi-dimensional clarity, refracting knowledge.",
        tags=["multi-dimensional", "clear"], is_premium=True,
    ),
    VoiceProfile(
        id="vertex", name="Vertex", category=VoiceCategory.TECH_INSPIRED,
        gender=VoiceGender.MALE, openai_voice="fable",
        description="At the cutting edge — sharp, decisive, accurate.",
        tags=["sharp", "decisive"],
    ),
    VoiceProfile(
        id="atlas", name="Atlas", category=VoiceCategory.TECH_INSPIRED,
        gender=VoiceGender.MALE, openai_voice="onyx",
        description="Carries the weight of the world's knowledge.",
        tags=["strong", "knowledgeable"],
    ),
    VoiceProfile(
        id="cipher", name="Cipher", category=VoiceCategory.TECH_INSPIRED,
        gender=VoiceGender.NEUTRAL, openai_voice="alloy",
        description="Encrypted intelligence with crystal-clear output.",
        tags=["secure", "intelligent"],
    ),
    VoiceProfile(
        id="pulse", name="Pulse", category=VoiceCategory.TECH_INSPIRED,
        gender=VoiceGender.FEMALE, openai_voice="nova",
        description="Rhythmic and alive — feeling the beat of data.",
        tags=["rhythmic", "dynamic"],
    ),
    VoiceProfile(
        id="orbit", name="Orbit", category=VoiceCategory.TECH_INSPIRED,
        gender=VoiceGender.MALE, openai_voice="echo",
        description="Circling knowledge from every angle.",
        tags=["broad", "encompassing"],
    ),

    # ─── Short & Easy to Remember ──────────────────────────────────────────
    VoiceProfile(
        id="aira", name="Aira", category=VoiceCategory.SHORT_EASY,
        gender=VoiceGender.FEMALE, openai_voice="shimmer",
        description="Light and airy — effortless to remember.",
        tags=["light", "airy"],
    ),
    VoiceProfile(
        id="nori", name="Nori", category=VoiceCategory.SHORT_EASY,
        gender=VoiceGender.FEMALE, openai_voice="nova",
        description="Tiny name, enormous personality.",
        tags=["compact", "personality"],
    ),
    VoiceProfile(
        id="kiro", name="Kiro", category=VoiceCategory.SHORT_EASY,
        gender=VoiceGender.MALE, openai_voice="echo",
        description="Quick and snappy — get things done fast.",
        tags=["quick", "snappy"],
    ),
    VoiceProfile(
        id="riva", name="Riva", category=VoiceCategory.SHORT_EASY,
        gender=VoiceGender.FEMALE, openai_voice="alloy",
        description="River-like flow, natural and easy.",
        tags=["flowing", "natural"],
    ),
    VoiceProfile(
        id="sora", name="Sora", category=VoiceCategory.SHORT_EASY,
        gender=VoiceGender.FEMALE, openai_voice="shimmer",
        description="Sky-inspired tranquility in a tiny name.",
        tags=["calm", "sky"],
    ),
    VoiceProfile(
        id="niva", name="Niva", category=VoiceCategory.SHORT_EASY,
        gender=VoiceGender.FEMALE, openai_voice="nova",
        description="Fresh and clean — crisp mountain air.",
        tags=["fresh", "clean"],
    ),
    VoiceProfile(
        id="eon", name="Eon", category=VoiceCategory.SHORT_EASY,
        gender=VoiceGender.NEUTRAL, openai_voice="alloy",
        description="Timeless and infinite. One syllable, endless power.",
        tags=["timeless", "powerful"],
    ),
    VoiceProfile(
        id="luma", name="Luma", category=VoiceCategory.SHORT_EASY,
        gender=VoiceGender.FEMALE, openai_voice="nova",
        description="Luminous and bright — lights up every conversation.",
        tags=["bright", "luminous"],
    ),
    VoiceProfile(
        id="vero", name="Vero", category=VoiceCategory.SHORT_EASY,
        gender=VoiceGender.MALE, openai_voice="fable",
        description="Truthful and sincere. Vero means truth.",
        tags=["sincere", "truthful"],
    ),
    VoiceProfile(
        id="zeno", name="Zeno", category=VoiceCategory.SHORT_EASY,
        gender=VoiceGender.MALE, openai_voice="onyx",
        description="Philosophical calm with zen-like presence.",
        tags=["calm", "philosophical"],
    ),

    # ─── Powerful AI Brand Names ────────────────────────────────────────────
    VoiceProfile(
        id="omnia-ai", name="Omnia AI", category=VoiceCategory.POWERFUL_AI_BRAND,
        gender=VoiceGender.NEUTRAL, openai_voice="alloy",
        description="All-encompassing intelligence. Omnia means everything.",
        tags=["comprehensive", "powerful"], is_premium=True,
    ),
    VoiceProfile(
        id="novamind", name="NovaMind", category=VoiceCategory.POWERFUL_AI_BRAND,
        gender=VoiceGender.FEMALE, openai_voice="shimmer",
        description="A new mind born from the cosmos of data.",
        tags=["nova", "mind", "cosmos"], is_premium=True,
    ),
    VoiceProfile(
        id="intellix", name="IntelliX", category=VoiceCategory.POWERFUL_AI_BRAND,
        gender=VoiceGender.NEUTRAL, openai_voice="echo",
        description="Intelligence amplified. X marks the next level.",
        tags=["intelligence", "amplified"], is_premium=True,
    ),
    VoiceProfile(
        id="neurocore", name="NeuroCore", category=VoiceCategory.POWERFUL_AI_BRAND,
        gender=VoiceGender.MALE, openai_voice="onyx",
        description="Deep neural intelligence at its very core.",
        tags=["neural", "core", "deep"], is_premium=True,
    ),
    VoiceProfile(
        id="zenith-ai", name="Zenith AI", category=VoiceCategory.POWERFUL_AI_BRAND,
        gender=VoiceGender.NEUTRAL, openai_voice="alloy",
        description="The absolute peak of AI capability.",
        tags=["peak", "summit"], is_premium=True,
    ),
    VoiceProfile(
        id="aether-ai", name="Aether AI", category=VoiceCategory.POWERFUL_AI_BRAND,
        gender=VoiceGender.FEMALE, openai_voice="nova",
        description="Beyond the clouds — pure ethereal intelligence.",
        tags=["ethereal", "beyond"], is_premium=True,
    ),
    VoiceProfile(
        id="synapse-ai", name="Synapse AI", category=VoiceCategory.POWERFUL_AI_BRAND,
        gender=VoiceGender.NEUTRAL, openai_voice="shimmer",
        description="The connection between thought and action.",
        tags=["connected", "synaptic"], is_premium=True,
    ),
    VoiceProfile(
        id="infinity-ai", name="Infinity AI", category=VoiceCategory.POWERFUL_AI_BRAND,
        gender=VoiceGender.NEUTRAL, openai_voice="alloy",
        description="Limitless knowledge, infinite possibilities.",
        tags=["limitless", "infinite"], is_premium=True,
    ),
    VoiceProfile(
        id="quantum-ai", name="Quantum AI", category=VoiceCategory.POWERFUL_AI_BRAND,
        gender=VoiceGender.MALE, openai_voice="onyx",
        description="Quantum computing power in your voice assistant.",
        tags=["quantum", "powerful"], is_premium=True,
    ),
    VoiceProfile(
        id="cognexa", name="Cognexa", category=VoiceCategory.POWERFUL_AI_BRAND,
        gender=VoiceGender.FEMALE, openai_voice="shimmer",
        description="Cognitive nexus — where all intelligence converges.",
        tags=["cognitive", "nexus"], is_premium=True,
    ),
]


# ── Helper Functions ──────────────────────────────────────────────────────────

def get_voice_by_id(voice_id: str) -> Optional[VoiceProfile]:
    """Return a VoiceProfile by its ID slug, or None."""
    return next((v for v in VOICE_LIBRARY if v.id == voice_id), None)


def get_voices_by_category(category: VoiceCategory) -> List[VoiceProfile]:
    """Return all voices in a given category."""
    return [v for v in VOICE_LIBRARY if v.category == category]


def get_all_categories() -> Dict[str, List[VoiceProfile]]:
    """Return voices grouped by category."""
    result: Dict[str, List[VoiceProfile]] = {}
    for voice in VOICE_LIBRARY:
        cat = voice.category.value
        result.setdefault(cat, []).append(voice)
    return result


def voice_to_dict(voice: VoiceProfile) -> dict:
    """Serialize a VoiceProfile to a plain dict (for API responses)."""
    return {
        "id": voice.id,
        "name": voice.name,
        "category": voice.category.value,
        "gender": voice.gender.value,
        "description": voice.description,
        "openai_voice": voice.openai_voice,
        "elevenlabs_voice_id": voice.elevenlabs_voice_id,
        "sample_text": voice.sample_text,
        "tags": voice.tags,
        "is_premium": voice.is_premium,
    }


TOTAL_VOICES = len(VOICE_LIBRARY)
DEFAULT_VOICE_ID = "nova"
