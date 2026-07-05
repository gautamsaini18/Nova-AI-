"""Nova AI — Communication Service

Integrates with SMS, phone calls (Twilio), WhatsApp, Telegram,
Slack, Discord, and Email.
"""

from __future__ import annotations

import smtplib
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

import httpx

from backend.core.config import settings
from backend.core.logging_config import NovaLogger

logger = NovaLogger("communication.service")


@dataclass
class MessageResult:
    success: bool
    provider: str
    message_id: Optional[str] = None
    error: Optional[str] = None


class CommunicationService:
    """
    Multi-channel communication: calls, SMS, WhatsApp, email, Slack, Discord, Telegram.
    """

    def __init__(self) -> None:
        self._twilio_sid = settings.TWILIO_ACCOUNT_SID
        self._twilio_token = settings.TWILIO_AUTH_TOKEN
        self._twilio_phone = settings.TWILIO_PHONE_NUMBER
        self._slack_token = settings.SLACK_BOT_TOKEN
        self._discord_token = settings.DISCORD_BOT_TOKEN
        self._telegram_token = settings.TELEGRAM_BOT_TOKEN
        logger.info("CommunicationService initialized")

    # ── SMS ────────────────────────────────────────────────────────────────

    async def send_sms(self, to: str, message: str) -> MessageResult:
        """Send an SMS via Twilio."""
        if not self._twilio_sid:
            return MessageResult(success=False, provider="twilio", error="Twilio not configured")
        try:
            from twilio.rest import Client
            client = Client(self._twilio_sid, self._twilio_token)
            msg = client.messages.create(body=message, from_=self._twilio_phone, to=to)
            logger.info("SMS sent", to=to, sid=msg.sid)
            return MessageResult(success=True, provider="twilio", message_id=msg.sid)
        except Exception as exc:
            logger.warning("SMS send failed", error=str(exc))
            return MessageResult(success=False, provider="twilio", error=str(exc))

    # ── Phone Calls ────────────────────────────────────────────────────────

    async def make_call(self, to: str, message: str) -> MessageResult:
        """Make a phone call with TTS message via Twilio."""
        if not self._twilio_sid:
            return MessageResult(success=False, provider="twilio", error="Twilio not configured")
        try:
            from twilio.rest import Client
            from twilio.twiml.voice_response import VoiceResponse
            client = Client(self._twilio_sid, self._twilio_token)
            response = VoiceResponse()
            response.say(message, voice="alice", language="en-US")
            call = client.calls.create(
                twiml=str(response),
                to=to,
                from_=self._twilio_phone,
            )
            logger.info("Call initiated", to=to, sid=call.sid)
            return MessageResult(success=True, provider="twilio_call", message_id=call.sid)
        except Exception as exc:
            logger.warning("Call failed", error=str(exc))
            return MessageResult(success=False, provider="twilio_call", error=str(exc))

    # ── WhatsApp ───────────────────────────────────────────────────────────

    async def send_whatsapp(self, to: str, message: str) -> MessageResult:
        """Send a WhatsApp message via Twilio."""
        if not self._twilio_sid:
            return MessageResult(success=False, provider="whatsapp", error="Twilio not configured")
        try:
            from twilio.rest import Client
            client = Client(self._twilio_sid, self._twilio_token)
            msg = client.messages.create(
                body=message,
                from_=f"whatsapp:{self._twilio_phone}",
                to=f"whatsapp:{to}",
            )
            logger.info("WhatsApp sent", to=to)
            return MessageResult(success=True, provider="whatsapp", message_id=msg.sid)
        except Exception as exc:
            logger.warning("WhatsApp send failed", error=str(exc))
            return MessageResult(success=False, provider="whatsapp", error=str(exc))

    # ── Telegram ───────────────────────────────────────────────────────────

    async def send_telegram(self, chat_id: str, message: str) -> MessageResult:
        """Send a Telegram message."""
        if not self._telegram_token:
            return MessageResult(success=False, provider="telegram", error="Telegram not configured")
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"https://api.telegram.org/bot{self._telegram_token}/sendMessage",
                    json={"chat_id": chat_id, "text": message},
                )
                resp.raise_for_status()
                logger.info("Telegram sent", chat_id=chat_id)
                return MessageResult(success=True, provider="telegram", message_id=str(resp.json().get("result", {}).get("message_id")))
        except Exception as exc:
            logger.warning("Telegram send failed", error=str(exc))
            return MessageResult(success=False, provider="telegram", error=str(exc))

    # ── Slack ──────────────────────────────────────────────────────────────

    async def send_slack(self, channel: str, message: str) -> MessageResult:
        """Send a Slack message."""
        if not self._slack_token:
            return MessageResult(success=False, provider="slack", error="Slack not configured")
        try:
            from slack_sdk import WebClient
            client = WebClient(token=self._slack_token)
            resp = client.chat_postMessage(channel=channel, text=message)
            logger.info("Slack sent", channel=channel)
            return MessageResult(success=True, provider="slack", message_id=resp.get("ts"))
        except Exception as exc:
            logger.warning("Slack send failed", error=str(exc))
            return MessageResult(success=False, provider="slack", error=str(exc))

    # ── Discord ────────────────────────────────────────────────────────────

    async def send_discord(self, channel_id: str, message: str) -> MessageResult:
        """Send a Discord message."""
        if not self._discord_token:
            return MessageResult(success=False, provider="discord", error="Discord not configured")
        try:
            import discord
            intents = discord.Intents.default()
            client = discord.Client(intents=intents)

            async def _send():
                await client.wait_until_ready()
                channel = client.get_channel(int(channel_id))
                if channel:
                    await channel.send(message)
                await client.close()

            await client.start(self._discord_token)
            logger.info("Discord sent", channel_id=channel_id)
            return MessageResult(success=True, provider="discord")
        except Exception as exc:
            logger.warning("Discord send failed", error=str(exc))
            return MessageResult(success=False, provider="discord", error=str(exc))

    # ── Email ──────────────────────────────────────────────────────────────

    async def send_email(self, to: str, subject: str, body: str, html: bool = False) -> MessageResult:
        """Send an email (SMTP)."""
        try:
            msg = MIMEMultipart("alternative") if html else MIMEText(body, "plain" if not html else "html")
            msg["Subject"] = subject
            msg["From"] = "noreply@nova-ai.com"
            msg["To"] = to
            if html:
                msg.attach(MIMEText(body, "html"))
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login("", "")
                server.send_message(msg)
            logger.info("Email sent", to=to, subject=subject)
            return MessageResult(success=True, provider="email")
        except Exception as exc:
            logger.warning("Email send failed", error=str(exc))
            return MessageResult(success=False, provider="email", error=str(exc))
