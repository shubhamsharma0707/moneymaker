import os
import sys
import json
import time
from dotenv import load_dotenv

from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add parent directory to sys.path to import moneymaker modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from money_maker.core.ai_engine import AIEngine

load_dotenv()
console = Console()

def load_profile():
    profile_path = os.path.join(os.path.dirname(__file__), "profile.json")
    try:
        with open(profile_path, "r") as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]Error loading profile.json: {e}[/]")
        sys.exit(1)

def generate_proposal(ai_engine, profile, job_description):
    prompt = f"""
You are an expert freelance proposal writer. Write a highly tailored, professional proposal for a gig.

Here is my freelancer profile context:
- Name: {profile.get('name')}
- Title: {profile.get('title')}
- Experience: {profile.get('years_of_experience')} years
- Skills: {', '.join(profile.get('skills', []))}
- Portfolio: {', '.join(profile.get('portfolio_links', []))}
- Tone: {profile.get('tone')}

Here is the Job Description posted by the client:
"{job_description}"

Instructions:
1. Write a personalized greeting.
2. Immediately address their core problem/need mentioned in the description.
3. Briefly highlight why my specific skills make me the perfect fit.
4. Include a clear Call to Action (e.g., "Let's hop on a quick call...").
5. Do NOT include placeholders like [Client Name] if the name isn't in the description, just use a generic greeting like "Hi there,".
6. Return ONLY the proposal text.
"""
    try:
        # Use the underlying OpenAI client directly to get a custom completion
        if not ai_engine._client:
            return "Error: OpenAI client not initialized. Check OPENAI_API_KEY."
            
        response = ai_engine._client.chat.completions.create(
            model=ai_engine.model,
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7,
            max_tokens=600,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Failed to generate proposal via AI: {e}\n\nFallback Template: Hi, I'm interested in your project and have the skills to complete it. Let's talk!"

def main():
    console.print(Panel.fit(
        "[bold cyan]Freelance Proposal Auto-Drafter[/]\n"
        "Generate 10x faster proposals for Upwork/Fiverr.",
        border_style="cyan"
    ))

    profile = load_profile()
    console.print(f"[dim]Loaded profile for: {profile.get('name')} ({profile.get('title')})[/]\n")

    ai_engine = AIEngine()
    
    if not ai_engine.api_key:
        console.print("[yellow]Warning: OPENAI_API_KEY not found in .env. Will use fallback templates.[/]")

    console.print("[bold]Paste the Job Description below (press Enter twice to finish):[/]")
    
    # Read multi-line input
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
        
    job_description = "\n".join(lines).strip()
    
    if not job_description:
        console.print("[red]Job description cannot be empty.[/]")
        return

    console.print()
    
    # Generate proposal with progress spinner
    proposal_text = ""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Drafting tailored proposal...", total=None)
        proposal_text = generate_proposal(ai_engine, profile, job_description)
        time.sleep(1) # Just for visual effect if API is too fast

    # Output result
    console.print("\n[bold green]✅ Proposal Generated![/]")
    console.print(Panel(
        Markdown(proposal_text),
        title="[bold yellow]Your Proposal[/]",
        border_style="yellow",
        expand=False
    ))
    
    # Copy hint
    console.print("\n[dim]Highlight the text above and copy it to submit your proposal.[/]")

if __name__ == "__main__":
    main()
