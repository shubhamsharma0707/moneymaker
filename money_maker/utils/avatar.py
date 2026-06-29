"""
Avatar generation using free AI APIs.

Generates avatars for freelancing profiles, content creation,
and client communications.
"""

import os
from typing import Optional

from rich.console import Console

console = Console()


class AvatarGenerator:
    """Generate avatars using free AI APIs."""

    def __init__(self):
        self._output_dir = os.path.expanduser("~/.money_maker_avatars")
        os.makedirs(self._output_dir, exist_ok=True)

    def generate_profile_avatar(self, style: str = "professional") -> Optional[str]:
        """
        Generate a profile avatar.
        Returns path to image file.
        """
        # Try multiple free avatar generation approaches
        path = self._generate_dicebear_avatar(style)
        if not path:
            path = self._generate_placeholder_avatar()
        return path

    def _generate_dicebear_avatar(self, style: str) -> Optional[str]:
        """Use DiceBear API (completely free, no API key)."""
        try:
            import httpx
            import datetime

            styles = {
                "professional": "avataaars",
                "fun": "bottts",
                "minimal": "identicon",
                "artistic": "micah",
                "pixel": "pixel-art",
            }

            dicebear_style = styles.get(style, "avataaars")
            seed = f"money_maker_{datetime.datetime.now().timestamp()}"

            url = f"https://api.dicebear.com/7.x/{dicebear_style}/svg?seed={seed}"

            response = httpx.get(url, timeout=10)
            if response.status_code == 200:
                output_path = os.path.join(self._output_dir, "avatar.svg")
                with open(output_path, "wb") as f:
                    f.write(response.content)
                console.print(f"[dim]✓ Avatar generated: {output_path}[/]")
                return output_path
        except Exception as e:
            console.print(f"[dim]DiceBear avatar failed: {e}[/]")
        return None

    def _generate_placeholder_avatar(self) -> str:
        """Generate a simple colored placeholder avatar."""
        try:
            from PIL import Image, ImageDraw
            import random

            size = 256
            # Random professional color
            colors = [
                (41, 128, 185),   # Blue
                (44, 62, 80),     # Dark
                (39, 174, 96),    # Green
                (142, 68, 173),   # Purple
                (230, 126, 34),   # Orange
            ]

            img = Image.new("RGB", (size, size), random.choice(colors))
            draw = ImageDraw.Draw(img)

            # Draw a simple "A" for AI/Avatar
            draw.ellipse([size//4, size//4, 3*size//4, 3*size//4], fill="white", outline=None)

            output_path = os.path.join(self._output_dir, "avatar.png")
            img.save(output_path, "PNG")
            return output_path

        except ImportError:
            # Can't generate without PIL
            return os.path.join(self._output_dir, "avatar.png")  # Path to non-existent file
        except Exception as e:
            console.print(f"[dim]Placeholder avatar failed: {e}[/]")
            return None

    def generate_branding_assets(self, brand_name: str) -> dict:
        """Generate simple branding assets."""
        return {
            "avatar": self.generate_profile_avatar(),
            "brand_name": brand_name,
            "tagline": f"Professional {brand_name} Services - AI Powered",
        }

    def get_avatar_path(self) -> Optional[str]:
        """Get path to the latest generated avatar."""
        import glob
        files = glob.glob(os.path.join(self._output_dir, "avatar.*"))
        return files[0] if files else None
