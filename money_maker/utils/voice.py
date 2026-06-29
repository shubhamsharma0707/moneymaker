"""
Voice generation capabilities.

Uses ElevenLabs free tier for text-to-speech.
Falls back to pyttsx3 (offline TTS) if ElevenLabs is unavailable.
"""

import os
from typing import Optional

from rich.console import Console

console = Console()


class VoiceGenerator:
    """Generate voice audio using free tier APIs."""

    def __init__(self):
        self._api_key = os.environ.get("ELEVENLABS_API_KEY", "")
        self._has_elevenlabs = bool(self._api_key)

        if self._has_elevenlabs:
            console.print("[dim]✓ ElevenLabs API configured[/]")

    def speak(self, text: str, voice: str = "default") -> Optional[str]:
        """
        Convert text to speech.
        Returns the path to the audio file, or None if failed.
        """
        if self._has_elevenlabs:
            return self._speak_elevenlabs(text, voice)
        return self._speak_offline(text)

    def _speak_elevenlabs(self, text: str, voice: str) -> Optional[str]:
        """Use ElevenLabs API (free tier: 10,000 chars/month)."""
        try:
            import httpx

            voice_id = self._get_voice_id(voice)
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self._api_key,
            }
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                },
            }

            response = httpx.post(url, json=data, headers=headers, timeout=30)

            if response.status_code == 200:
                output_dir = os.path.expanduser("~/.money_maker_audio")
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"voice_{hash(text) % 10000}.mp3")

                with open(output_path, "wb") as f:
                    f.write(response.content)

                console.print(f"[dim]✓ Voice audio saved to {output_path}[/]")
                return output_path
            else:
                console.print(f"[yellow]ElevenLabs error: {response.status_code} - {response.text[:100]}[/]")
                return None

        except Exception as e:
            console.print(f"[yellow]ElevenLabs failed: {e}. Trying offline TTS.[/]")
            return self._speak_offline(text)

    def _speak_offline(self, text: str) -> Optional[str]:
        """Use pyttsx3 for offline TTS."""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            output_dir = os.path.expanduser("~/.money_maker_audio")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, "voice_offline.wav")
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            return output_path
        except Exception as e:
            console.print(f"[yellow]Offline TTS failed: {e}[/]")
            return None

    def _get_voice_id(self, voice: str) -> str:
        """Get ElevenLabs voice ID."""
        voices = {
            "default": "21m00Tcm4TlvDq8ikWAM",     # Rachel
            "male": "AZnzlk1XvdvUeBnXmlld",        # Dominic
            "female": "21m00Tcm4TlvDq8ikWAM",       # Rachel
            "american": "ErXwobaYiN019PkySvjV",     # Antoni
            "british": "ThT5KcBeYPX3keUQqHPh",      # Thomas
        }
        return voices.get(voice, voices["default"])

    def generate_client_message(self, client_name: str, message: str) -> Optional[str]:
        """Generate a voice message for a client."""
        intro = f"Hello {client_name}, this is your AI assistant. "
        full_text = intro + message
        return self.speak(full_text, voice="american")
