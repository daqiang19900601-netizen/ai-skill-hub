from ai_skill_hub.storage import Skill
from typing import Dict, Callable


class SkillExporter:
    """Exports skills to formats compatible with different AI tools"""

    TOOL_TEMPLATES = {
        "generic": """# {name}

{description}

## Prompt

{content}

## Variables

{variables}

## Examples

{examples}
""",
        "claude": """<anthropic_thinking_protocol>
{name}
</anthropic_thinking_protocol>

{description}

<prompt>
{content}
</prompt>

<variables>
{variables}
</variables>
""",
        "cursor": """# {name}
# {description}

{content}

# Variables: {variables}
# Examples:
{examples}
""",
        "vscode": """/* AI Skill: {name} */
/* {description} */

{content}

/* Variables: {variables} */
""",
        "trae": """# {name}
# {description}

{content}

## Variables
{variables}

## Examples
{examples}
""",
        "github-copilot": """# {name}
# {description}
# Compatible with GitHub Copilot

{content}

# Variables: {variables}
""",
    }

    def export(self, skill: Skill, tool: str = "generic") -> str:
        template = self.TOOL_TEMPLATES.get(tool, self.TOOL_TEMPLATES["generic"])
        
        variables_str = ", ".join([f"{k}: {v}" for k, v in skill.variables.items()]) if skill.variables else "None"
        
        examples_str = ""
        if skill.examples:
            for i, ex in enumerate(skill.examples, 1):
                examples_str += f"{i}. {ex.get('description', '')}: {ex.get('input', '')} -> {ex.get('output', '')}\n"
        else:
            examples_str = "None"
        
        return template.format(
            name=skill.name,
            description=skill.description,
            content=skill.content,
            variables=variables_str,
            examples=examples_str,
        )

    def export_all(self, skills: list, tool: str = "generic") -> Dict[str, str]:
        results = {}
        for skill in skills:
            results[skill.name] = self.export(skill, tool)
        return results

    def get_compatible_tools(self) -> list:
        return list(self.TOOL_TEMPLATES.keys())
