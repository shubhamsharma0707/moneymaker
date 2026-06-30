import os
import sys
import json
import time
import glob
from dotenv import load_dotenv

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

load_dotenv()
console = Console()

PROFILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles")


def load_all_profiles() -> list[dict]:
    """Load every profile JSON in the profiles/ folder."""
    paths = sorted(glob.glob(os.path.join(PROFILES_DIR, "*.json")))
    if not paths:
        console.print(f"[red]No profile files found in {PROFILES_DIR}[/]")
        sys.exit(1)

    profiles = []
    for path in paths:
        try:
            with open(path) as f:
                data = json.load(f)
                data["_filename"] = os.path.basename(path)
                profiles.append(data)
        except Exception as e:
            console.print(f"[yellow]Warning: could not load {path}: {e}[/]")
    return profiles


def has_unfilled_fields(profile: dict) -> bool:
    """Check if a profile still has FILL_IN placeholders."""
    text = json.dumps(profile)
    return "FILL_IN" in text


def choose_profile(profiles: list[dict]) -> dict:
    """Ask the user which profile/account to draft a proposal for."""
    console.print("\n[bold]Which account/skill profile is this proposal for?[/]\n")
    for i, p in enumerate(profiles, start=1):
        flag = " [red](needs setup — see below)[/]" if has_unfilled_fields(p) else ""
        console.print(f"  [cyan]{i}.[/] {p.get('title', p['_filename'])}{flag}")

    while True:
        choice = console.input("\n[bold]Enter number: [/]").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(profiles):
            return profiles[int(choice) - 1]
        console.print("[red]Invalid choice, try again.[/]")


def get_openai_client():
    """Initialize the OpenAI client from OPENAI_API_KEY."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return None, None
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key), os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    except ImportError:
        console.print("[red]✗ openai package not installed. Run: pip install openai --break-system-packages[/]")
        return None, None


def generate_proposal(client, model: str, profile: dict, job_description: str) -> str:
    skills = ", ".join(profile.get("skills", [])) or "Not specified"
    portfolio = ", ".join(profile.get("portfolio_links", [])) or "No portfolio links yet"

    prompt = f"""You are an expert freelance proposal writer. Write a highly tailored, professional proposal for a gig.

Here is my freelancer profile context:
- Name: {profile.get('name')}
- Title: {profile.get('title')}
- Experience: {profile.get('years_of_experience')} years
- Skills: {skills}
- Portfolio: {portfolio}
- Tone: {profile.get('tone')}

Here is the Job Description posted by the client:
"{job_description}"

Instructions:
1. Write a personalized greeting.
2. Immediately address their core problem/need mentioned in the description.
3. Briefly highlight why my specific skills make me the perfect fit.
4. If I have no portfolio links yet, do NOT apologize for it or mention the lack of one — just lead with skills and confidence instead.
5. Include a clear Call to Action (e.g., "Let's hop on a quick call...").
6. Do NOT include placeholders like [Client Name] if the name isn't in the description; just use a generic greeting like "Hi there,".
7. Return ONLY the proposal text, nothing else.
"""
    if not client:
        return (
            "[No OPENAI_API_KEY found — fallback template used]\n\n"
            "Hi there,\n\n"
            f"I read through your project and I'm confident I can help — I specialize in "
            f"{skills} and have {profile.get('years_of_experience')} years of relevant experience. "
            "I'd love to hop on a quick call to discuss your goals and how I can deliver this for you.\n\n"
            f"Best,\n{profile.get('name')}"
        )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=600,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return (
            f"[AI generation failed: {e}]\n\n"
            "Fallback: Hi, I'm interested in your project and have the skills to complete it. "
            "Let's talk!"
        )


def read_multiline_input() -> str:
    console.print("[bold]Paste the Job Description below (press Enter twice to finish):[/]")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def main():
    console.print(Panel.fit(
        "[bold cyan]Freelance Proposal Auto-Drafter[/]\n"
        "Generate tailored proposals fast — you review and send them yourself.",
        border_style="cyan"
    ))

    profiles = load_all_profiles()
    profile = choose_profile(profiles)

    if has_unfilled_fields(profile):
        console.print(
            f"\n[yellow]⚠ {profile['_filename']} still has FILL_IN placeholders.[/]\n"
            f"[dim]Edit profiles/{profile['_filename']} with your real info for accurate proposals.[/]\n"
        )

    console.print(f"\n[dim]Using profile: {profile.get('name')} — {profile.get('title')}[/]\n")

    client, model = get_openai_client()
    if not client:
        console.print("[yellow]Warning: OPENAI_API_KEY not found in .env. Using fallback template instead of AI.[/]\n")

    job_description = read_multiline_input()
    if not job_description:
        console.print("[red]Job description cannot be empty.[/]")
        return

    console.print()
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Drafting tailored proposal...", total=None)
        proposal_text = generate_proposal(client, model, profile, job_description)
        time.sleep(0.5)

    console.print("\n[bold green]✅ Proposal Generated![/]")
    console.print(Panel(
        Markdown(proposal_text),
        title=f"[bold yellow]Proposal — {profile.get('title')}[/]",
        border_style="yellow",
        expand=False
    ))

    console.print("\n[dim]Highlight the text above and copy it to submit your proposal.[/]")
    console.print("[dim]Reminder: review before sending — check accuracy, tone, and that it actually fits the job.[/]")


if __name__ == "__main__":
    main()
