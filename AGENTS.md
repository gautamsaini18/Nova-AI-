# Nova AI — Agent Instructions

## Commands
- **Run backend**: `uvicorn backend.main:app --reload` (from project root)
- **Run frontend**: `cd frontend && npm run dev`
- **Run tests**: `cd backend && pytest -v`
- **Type check**: `cd backend && mypy .`
- **Lint**: `cd backend && black . && isort .`

## Architecture
- **Backend**: Python/FastAPI in `backend/`
- **Frontend**: Next.js in `frontend/`
- **Database**: SQLite (dev) / PostgreSQL (prod) + ChromaDB for vector memory
- **STT**: OpenAI Whisper
- **TTS**: OpenAI TTS / ElevenLabs
- **Wake Word**: Porcupine
- **Auth**: JWT + Firebase (optional)

## Backend Structure
- `backend/main.py` — FastAPI app entry point
- `backend/core/` — Config, logging, security
- `backend/models/` — Pydantic schemas
- `backend/api/` — API routers (chat, voice, memory, settings)
- `backend/modules/` — Feature modules:
  - `ai_reasoning/` — GPT-4 agent
  - `voice/` — TTS engine + 60+ voice profiles
  - `memory/` — ChromaDB memory manager
  - `wake_word/` — Porcupine wake word detection
  - `voice_input/` — Audio capture
  - `speech_processing/` — VAD + noise reduction
  - `weather/` — Weather service
  - `device_control/` — Windows device control
  - `calendar_module/` — Calendar + reminders
  - `navigation/` — Maps + directions
  - `music/` — Music playback
  - `communication/` — SMS, calls, WhatsApp, email, Slack, Discord, Telegram
  - `smart_home/` — HomeKit + IoT control
  - `vision/` — OCR, barcode, scene description
  - `automation/` — Workflow automation
  - `api_services/` — News, currency, translation, stock
  - `plugins/` — Plugin system
  - `security/` — Voice authentication
- `backend/database/` — SQLAlchemy models + session
- `backend/tests/` — Unit tests

## Key Conventions
- All API routes prefixed with `/api/v1/`
- Async everywhere in backend
- Loguru for structured logging
- Pydantic v2 for validation
- ChromaDB for semantic memory
- Voice profiles map to OpenAI TTS voices
