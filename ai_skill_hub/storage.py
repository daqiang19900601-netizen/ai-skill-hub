import os
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any


class Skill:
    """Represents an AI skill/prompt"""
    
    def __init__(self, name: str, content: str, description: str = "",
                 tags: List[str] = None, author: str = "", version: str = "1.0.0",
                 compatible_tools: List[str] = None, created_at: str = None,
                 updated_at: str = None, examples: List[Dict] = None,
                 variables: Dict[str, str] = None):
        self.name = name
        self.content = content
        self.description = description
        self.tags = tags or []
        self.author = author
        self.version = version
        self.compatible_tools = compatible_tools or ["all"]
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
        self.examples = examples or []
        self.variables = variables or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "content": self.content,
            "description": self.description,
            "tags": self.tags,
            "author": self.author,
            "version": self.version,
            "compatible_tools": self.compatible_tools,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "examples": self.examples,
            "variables": self.variables,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Skill":
        return cls(
            name=data.get("name", ""),
            content=data.get("content", ""),
            description=data.get("description", ""),
            tags=data.get("tags", []),
            author=data.get("author", ""),
            version=data.get("version", "1.0.0"),
            compatible_tools=data.get("compatible_tools", ["all"]),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            examples=data.get("examples", []),
            variables=data.get("variables", {}),
        )

    def to_yaml(self) -> str:
        return yaml.dump(self.to_dict(), default_flow_style=False, allow_unicode=True)

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "Skill":
        data = yaml.safe_load(yaml_str)
        return cls.from_dict(data)


class SkillStorage:
    """Manages local skill storage"""

    def __init__(self, skills_dir: Optional[str] = None):
        self.skills_dir = Path(skills_dir) if skills_dir else self._get_default_dir()
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        (self.skills_dir / "library").mkdir(exist_ok=True)

    def _get_default_dir(self) -> Path:
        home = Path.home()
        return home / ".skills"

    def list_skills(self, tag: Optional[str] = None) -> List[Skill]:
        skills = []
        library_dir = self.skills_dir / "library"
        
        for skill_file in library_dir.glob("*.yaml"):
            try:
                with open(skill_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    skill = Skill.from_dict(data)
                    if tag and tag not in skill.tags:
                        continue
                    skills.append(skill)
            except Exception:
                continue
        
        return sorted(skills, key=lambda s: s.name)

    def get_skill(self, name: str) -> Optional[Skill]:
        skill_file = self.skills_dir / "library" / f"{name}.yaml"
        if not skill_file.exists():
            return None
        
        try:
            with open(skill_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return Skill.from_dict(data)
        except Exception:
            return None

    def save_skill(self, skill: Skill) -> str:
        skill_file = self.skills_dir / "library" / f"{skill.name}.yaml"
        skill.updated_at = datetime.now().isoformat()
        
        with open(skill_file, "w", encoding="utf-8") as f:
            f.write(skill.to_yaml())
        
        return str(skill_file)

    def delete_skill(self, name: str) -> bool:
        skill_file = self.skills_dir / "library" / f"{name}.yaml"
        if skill_file.exists():
            skill_file.unlink()
            return True
        return False

    def search_skills(self, query: str) -> List[Skill]:
        results = []
        query_lower = query.lower()
        
        for skill in self.list_skills():
            if (query_lower in skill.name.lower() or
                query_lower in skill.description.lower() or
                query_lower in skill.content.lower() or
                any(query_lower in tag.lower() for tag in skill.tags)):
                results.append(skill)
        
        return results

    def export_skill_as_dict(self, name: str) -> Optional[Dict]:
        skill = self.get_skill(name)
        return skill.to_dict() if skill else None
