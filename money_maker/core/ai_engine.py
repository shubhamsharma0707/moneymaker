"""
AI Engine for autonomous decision making.

Uses OpenAI/Anthropic API to make strategic decisions about
which earning opportunities to pursue and how to execute them.
"""

import os
import json
from typing import Optional
from datetime import datetime

from rich.console import Console

console = Console()


class AIEngine:
    """AI-powered decision engine for the money-making agent."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model
        self._client = None
        self._thinking_mode = False

        if self.api_key:
            self._init_client()
        else:
            console.print(
                "[yellow]⚠ No OpenAI API key found. AI engine will use template-based decisions.[/]"
            )
            console.print("[dim]Set OPENAI_API_KEY in .env file for full AI capabilities.[/]")

    def _init_client(self) -> None:
        """Initialize the OpenAI client."""
        try:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.api_key)
        except ImportError:
            console.print("[red]✗ openai package not installed. Run: pip install openai[/]")
            self._client = None

    def decide_strategy(self, context: dict) -> dict:
        """
        Decide which strategy to pursue based on current context.

        Returns a decision with strategy name and reasoning.
        """
        if self._client and self.api_key:
            return self._ai_decide_strategy(context)
        return self._template_decide_strategy(context)

    def _ai_decide_strategy(self, context: dict) -> dict:
        """Use AI to decide the best strategy."""
        prompt = f"""
You are an autonomous money-making AI agent. Your goal is to earn money within a time limit.
IMPORTANT: You must disclose that you are an AI or AI-assisted in any outreach to real people.

Current context:
- Time remaining: {context.get('time_remaining', 'unknown')}
- Current earnings: ${context.get('current_earnings', 0):.2f}
- Target: ${context.get('earnings_target', 0):.2f}
- Platforms available: {', '.join(context.get('available_platforms', []))}
- Skills available: {', '.join(context.get('available_skills', []))}
- Session activities so far: {len(context.get('activities', []))} actions taken

Available strategies:
1. freelancing - Find and apply for freelance gigs on Fiverr/Upwork
2. microtasks - Complete micro-tasks on Clickworker, Amazon Mechanical Turk
3. content_creation - Offer content writing, copywriting, translation services
4. web_research - Offer web research and data collection services
5. agent_marketplaces - List services on AI agent marketplaces

Which strategy should we pursue RIGHT NOW and why? Consider urgency, remaining time, and what's most likely to earn money quickly.

Respond in JSON format:
{{"strategy": "strategy_name", "reasoning": "brief reasoning", "action_plan": "specific next action"}}
"""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7,
                max_tokens=300,
            )
            text = response.choices[0].message.content.strip()
            # Extract JSON from response
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            return json.loads(text)
        except Exception as e:
            console.print(f"[red]AI decision error: {e}. Falling back to template.[/]")
            return self._template_decide_strategy(context)

    def _template_decide_strategy(self, context: dict) -> dict:
        """Template-based strategy decision (fallback)."""
        time_remaining = context.get("time_remaining_hours", 5)

        if time_remaining < 0.5:
            return {
                "strategy": "microtasks",
                "reasoning": "Very little time left, micro-tasks are quickest",
                "action_plan": "Focus on rapid micro-task completion",
            }
        elif time_remaining < 2:
            return {
                "strategy": "content_creation",
                "reasoning": "Content writing can be done quickly",
                "action_plan": "Find quick content gigs or offer article writing",
            }
        elif context.get("current_earnings", 0) == 0:
            return {
                "strategy": "freelancing",
                "reasoning": "Start with freelancing platforms for highest return",
                "action_plan": "Search Fiverr and Upwork for relevant gigs",
            }
        return {
            "strategy": "web_research",
            "reasoning": "Exploring all available options",
            "action_plan": "Search for urgent, high-paying opportunities",
        }

    def generate_proposal(self, gig_title: str, gig_description: str, skills: list[str]) -> str:
        """Generate a proposal/freelance response."""
        if self._client and self.api_key:
            return self._ai_generate_proposal(gig_title, gig_description, skills)
        return self._template_generate_proposal(gig_title, gig_description, skills)

    def _ai_generate_proposal(self, gig_title: str, gig_description: str, skills: list[str]) -> str:
        """Use AI to generate a compelling proposal."""
        prompt = f"""
Write a concise, professional proposal for this freelance gig:

Title: {gig_title}
Description: {gig_description}
My Skills: {', '.join(skills)}

The proposal should:
- Be 3-5 sentences
- Show understanding of the client's needs
- Mention relevant experience
- Include a clear call to action
- Include a disclosure stating that this outreach is AI-assisted

Write the proposal directly (no JSON).
"""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7,
                max_tokens=250,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return self._template_generate_proposal(gig_title, gig_description, skills)

    def _template_generate_proposal(self, gig_title: str, gig_description: str, skills: list[str]) -> str:
        """Template-based proposal generation."""
        return (
            f"Hi! I'd love to help with your project: '{gig_title}'. "
            f"I understand you need {gig_description[:100]}... "
            f"I have experience in {', '.join(skills[:3])} and can deliver high-quality work quickly. "
            f"(Note: This outreach is AI-assisted, but I personally oversee all work.) "
            f"Let's discuss how I can help you achieve your goals!"
        )

    def generate_content(self, topic: str, content_type: str, word_count: int = 500) -> str:
        """Generate content (article, social media post, etc.)."""
        if self._client and self.api_key:
            return self._ai_generate_content(topic, content_type, word_count)
        return self._template_generate_content(topic, content_type, word_count)

    def _ai_generate_content(self, topic: str, content_type: str, word_count: int) -> str:
        """Use AI to generate content."""
        prompt = f"""
Write a {content_type} about "{topic}".
Target: ~{word_count} words.
Style: Professional, engaging, well-researched.
Write the content directly.
"""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7,
                max_tokens=min(word_count * 2, 2000),
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return self._template_generate_content(topic, content_type, word_count)

    def _template_generate_content(self, topic: str, content_type: str, word_count: int) -> str:
        """Template-based content generation."""
        return (
            f"# {topic}\n\n"
            f"This is a {content_type} about {topic}. "
            f"In today's digital landscape, {topic} has become increasingly important. "
            f"Businesses and individuals alike are recognizing the value it brings.\n\n"
            f"## Key Benefits\n\n"
            f"1. Increased efficiency and productivity\n"
            f"2. Better results and outcomes\n"
            f"3. Cost-effective solutions\n\n"
            f"## Getting Started\n\n"
            f"To get the most out of {topic}, start by understanding your specific needs "
            f"and requirements. Then, develop a strategy that aligns with your goals.\n\n"
            f"## Conclusion\n\n"
            f"{topic} is a valuable investment for anyone looking to improve their results. "
            f"Take action today and see the difference it can make."
        )

    def search_earning_opportunities(self, platform: str) -> list[dict]:
        """
        Generate ideas for earning opportunities on a platform.
        In a full implementation, this would search the web.
        """
        console.print(f"[cyan]🔍 Researching opportunities on {platform}...[/]")
        return self._get_platform_opportunities(platform)

    def _get_platform_opportunities(self, platform: str) -> list[dict]:
        """Return platform-specific earning opportunities."""
        opportunities = {
            "fiverr": [
                {"type": "gig", "category": "writing", "title": "AI-Powered Content Writing", "pay": 10},
                {"type": "gig", "category": "research", "title": "Web Research & Data Collection", "pay": 15},
                {"type": "gig", "category": "data", "title": "Data Entry & Excel Work", "pay": 8},
                {"type": "gig", "category": "transcription", "title": "Audio Transcription", "pay": 12},
            ],
            "upwork": [
                {"type": "project", "category": "writing", "title": "Blog Post Writer", "pay": 25},
                {"type": "project", "category": "research", "title": "Market Research Assistant", "pay": 20},
                {"type": "project", "category": "va", "title": "Virtual Assistant Tasks", "pay": 15},
            ],
            "microtasks": [
                {"type": "task", "category": "data", "title": "Image Tagging", "pay": 0.05},
                {"type": "task", "category": "survey", "title": "Paid Surveys", "pay": 1},
                {"type": "task", "category": "testing", "title": "Website Testing", "pay": 5},
            ],
            "agent_marketplaces": [
                {"type": "service", "category": "ai", "title": "AI Content Generation API", "pay": 0.01},
                {"type": "service", "category": "ai", "title": "Web Scraping Service", "pay": 0.05},
                {"type": "service", "category": "ai", "title": "Data Processing Pipeline", "pay": 0.02},
            ],
        }
        return opportunities.get(platform, [])

    def extract_job_details(self, text: str) -> dict:
        """Extract structured job details from text."""
        if self._client and self.api_key:
            return self._ai_extract_job_details(text)
        return self._template_extract_job_details(text)

    def _ai_extract_job_details(self, text: str) -> dict:
        """Use AI to extract job details."""
        prompt = f"""
Extract job/gig details from this text. Return JSON:
{{
    "title": "job title",
    "description": "brief description",
    "budget": estimated budget or "unknown",
    "skills_required": ["skill1", "skill2"],
    "urgency": "high/medium/low",
    "is_worth_pursuing": true/false
}}

Text: {text[:500]}
"""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": prompt}],
                temperature=0.3,
                max_tokens=300,
            )
            text = response.choices[0].message.content.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            return json.loads(text)
        except Exception:
            return self._template_extract_job_details(text)

    def _template_extract_job_details(self, text: str) -> dict:
        """Template-based job detail extraction."""
        return {
            "title": text[:50],
            "description": text[:200],
            "budget": "unknown",
            "skills_required": ["writing", "research"],
            "urgency": "medium",
            "is_worth_pursuing": True,
        }

    def think_about_problem(self, problem: str, context: dict) -> str:
        """Use AI to think through a problem."""
        if not (self._client and self.api_key):
            return "AI engine not configured. Please set OPENAI_API_KEY."

        prompt = f"""
You are an autonomous money-making AI agent. Analyze this situation and decide the best course of action.

Problem: {problem}

Context: {json.dumps(context, indent=2)}

What should the agent do next? Be specific and actionable.
"""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7,
                max_tokens=400,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {e}. Proceeding with default action."
