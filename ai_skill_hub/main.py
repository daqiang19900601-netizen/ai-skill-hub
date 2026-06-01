import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich import print as rprint

from ai_skill_hub.storage import Skill, SkillStorage
from ai_skill_hub.exporter import SkillExporter
from ai_skill_hub.analyzer import SkillAnalyzer
from ai_skill_hub.git_integration import GitManager
from ai_skill_hub.sharing import SkillSharer

console = Console()
storage = SkillStorage()
exporter = SkillExporter()
analyzer = SkillAnalyzer()
git_manager = GitManager()
sharer = SkillSharer()


@click.group()
@click.version_option(version="1.0.0", prog_name="AI Skill Hub")
def cli():
    """🚀 AI Skill Hub - Cross-AI tool local skill management system"""
    pass


@cli.command()
@click.option("--name", "-n", required=True, help="Skill name")
@click.option("--description", "-d", default="", help="Skill description")
@click.option("--tags", "-t", default="", help="Comma-separated tags")
@click.option("--author", "-a", default="", help="Author name")
@click.option("--tools", default="all", help="Compatible tools (comma-separated or 'all')")
def init(name, description, tags, author, tools):
    """Initialize a new skill"""
    console.print(Panel(f"Creating new skill: [bold]{name}[/bold]", style="green"))
    
    content = Prompt.ask("Enter skill content (prompt)")
    variables_input = Prompt.ask("Enter variables (JSON format, e.g. {'lang': 'python'})", default="{}")
    
    try:
        import json
        variables = json.loads(variables_input)
    except json.JSONDecodeError:
        console.print("[yellow]Warning: Invalid JSON for variables, using empty dict[/yellow]")
        variables = {}
    
    tags_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    tools_list = [t.strip() for t in tools.split(",")] if tools != "all" else ["all"]
    
    skill = Skill(
        name=name,
        content=content,
        description=description,
        tags=tags_list,
        author=author,
        compatible_tools=tools_list,
        variables=variables,
    )
    
    file_path = storage.save_skill(skill)
    console.print(f"[green]✅ Skill saved to:[/green] {file_path}")
    
    git_manager.init_and_commit(storage.skills_dir, f"Add skill: {name}")


@cli.command()
@click.argument("name")
def show(name):
    """Show details of a skill"""
    skill = storage.get_skill(name)
    if not skill:
        console.print(f"[red]❌ Skill '{name}' not found[/red]")
        return
    
    table = Table(title=f"Skill: {name}")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Description", skill.description)
    table.add_row("Author", skill.author)
    table.add_row("Version", skill.version)
    table.add_row("Tags", ", ".join(skill.tags))
    table.add_row("Tools", ", ".join(skill.compatible_tools))
    table.add_row("Created", skill.created_at)
    table.add_row("Updated", skill.updated_at)
    
    console.print(table)
    console.print(Panel(skill.content, title="Content", border_style="blue"))
    
    if skill.examples:
        console.print("\n[yellow]Examples:[/yellow]")
        for i, ex in enumerate(skill.examples, 1):
            console.print(f"  {i}. {ex.get('description', '')}")


@cli.command()
@click.option("--tag", "-t", default="", help="Filter by tag")
def list(tag):
    """List all skills"""
    skills = storage.list_skills(tag=tag if tag else None)
    
    if not skills:
        console.print("[yellow]No skills found.[/yellow]")
        return
    
    table = Table(title="📚 Your Skills")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Tags", style="green")
    table.add_column("Version", style="yellow")
    table.add_row("Updated", style="dim")
    
    for skill in skills:
        table.add_row(
            skill.name,
            skill.description[:50] + ("..." if len(skill.description) > 50 else ""),
            ", ".join(skill.tags[:3]),
            skill.version,
            skill.updated_at[:10],
        )
    
    console.print(table)


@cli.command()
@click.argument("name")
@click.option("--tool", "-t", default="generic", 
              type=click.Choice(["generic", "claude", "cursor", "vscode", "trae", "github-copilot"]),
              help="Target AI tool")
def export(name, tool):
    """Export a skill for a specific AI tool"""
    skill = storage.get_skill(name)
    if not skill:
        console.print(f"[red]❌ Skill '{name}' not found[/red]")
        return
    
    exported = exporter.export(skill, tool)
    
    output_file = f"{name}_{tool}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(exported)
    
    console.print(f"[green]✅ Exported to:[/green] {output_file}")
    console.print(Panel(exported, title=f"Exported for {tool}", border_style="green"))


@cli.command()
@click.argument("name")
def analyze(name):
    """Analyze a skill (token count, optimization suggestions)"""
    skill = storage.get_skill(name)
    if not skill:
        console.print(f"[red]❌ Skill '{name}' not found[/red]")
        return
    
    analysis = analyzer.analyze(skill)
    
    table = Table(title=f"📊 Analysis: {name}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Token Count", str(analysis["token_count"]))
    table.add_row("Character Count", str(analysis["char_count"]))
    table.add_row("Word Count", str(analysis["word_count"]))
    table.add_row("Complexity", analysis["complexity"])
    
    console.print(table)
    
    if analysis["suggestions"]:
        console.print("\n[yellow]💡 Optimization Suggestions:[/yellow]")
        for i, suggestion in enumerate(analysis["suggestions"], 1):
            console.print(f"  {i}. {suggestion}")


@cli.command()
@click.argument("name")
@click.option("--query", "-q", default="", help="Search query")
def search(query):
    """Search skills"""
    if not query:
        query = Prompt.ask("Enter search query")
    
    results = storage.search_skills(query)
    
    if not results:
        console.print(f"[yellow]No skills found for '{query}'[/yellow]")
        return
    
    table = Table(title=f"🔍 Search Results: {query}")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Tags", style="green")
    table.add_row("Score", style="yellow")
    
    for skill in results:
        score = analyzer.relevance_score(skill, query)
        table.add_row(
            skill.name,
            skill.description[:50],
            ", ".join(skill.tags[:3]),
            f"{score:.1f}%",
        )
    
    console.print(table)


@cli.command()
@click.argument("name")
def delete(name):
    """Delete a skill"""
    if not click.confirm(f"Are you sure you want to delete '{name}'?"):
        console.print("[yellow]Cancelled.[/yellow]")
        return
    
    if storage.delete_skill(name):
        console.print(f"[green]✅ Deleted skill '{name}'[/green]")
        git_manager.init_and_commit(storage.skills_dir, f"Delete skill: {name}")
    else:
        console.print(f"[red]❌ Skill '{name}' not found[/red]")


@cli.command()
@click.argument("name")
@click.option("--tag", "-t", default="", help="Add tag")
@click.option("--description", "-d", default="", help="Update description")
def update(name, tag, description):
    """Update a skill"""
    skill = storage.get_skill(name)
    if not skill:
        console.print(f"[red]❌ Skill '{name}' not found[/red]")
        return
    
    if tag:
        new_tags = [t.strip() for t in tag.split(",")]
        skill.tags.extend(new_tags)
        skill.tags = list(set(skill.tags))
    
    if description:
        skill.description = description
    
    content = Prompt.ask("Update content? (leave empty to keep current)", default="")
    if content:
        skill.content = content
    
    storage.save_skill(skill)
    console.print(f"[green]✅ Updated skill '{name}'[/green]")
    git_manager.init_and_commit(storage.skills_dir, f"Update skill: {name}")


@cli.command()
@click.argument("name")
@click.option("--from-file", "-f", type=click.Path(exists=True), help="Load from file")
def import_skill(name, from_file):
    """Import a skill from file or URL"""
    if from_file:
        with open(from_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        try:
            skill = Skill.from_yaml(content)
            storage.save_skill(skill)
            console.print(f"[green]✅ Imported skill: {skill.name}[/green]")
        except Exception as e:
            console.print(f"[red]❌ Failed to import: {e}[/red]")


@cli.command()
@click.argument("name")
def share(name):
    """Share a skill to GitHub Gist"""
    skill = storage.get_skill(name)
    if not skill:
        console.print(f"[red]❌ Skill '{name}' not found[/red]")
        return
    
    gist_url = sharer.share_to_gist(skill)
    if gist_url:
        console.print(f"[green]✅ Shared to GitHub Gist:[/green] {gist_url}")
    else:
        console.print("[yellow]⚠️  Gist sharing requires GitHub token. Set GITHUB_TOKEN environment variable.[/yellow]")


@cli.command()
@click.argument("gist_url")
def install(gist_url):
    """Install a skill from GitHub Gist URL"""
    skill = sharer.install_from_gist(gist_url)
    if skill:
        storage.save_skill(skill)
        console.print(f"[green]✅ Installed skill: {skill.name}[/green]")
    else:
        console.print(f"[red]❌ Failed to install skill from {gist_url}[/red]")


@cli.command()
def status():
    """Show storage status and statistics"""
    skills = storage.list_skills()
    
    table = Table(title="📈 Storage Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Total Skills", str(len(skills)))
    table.add_row("Storage Path", str(storage.skills_dir))
    
    all_tags = set()
    for skill in skills:
        all_tags.update(skill.tags)
    table.add_row("Unique Tags", str(len(all_tags)))
    
    console.print(table)


@cli.command()
@click.option("--dir", "-d", default=None, help="Custom skills directory")
def config(dir):
    """Show or set configuration"""
    if dir:
        new_storage = SkillStorage(dir)
        console.print(f"[green]✅ Skills directory set to:[/green] {dir}")
    else:
        console.print(f"📁 Current skills directory: {storage.skills_dir}")


if __name__ == "__main__":
    cli()
