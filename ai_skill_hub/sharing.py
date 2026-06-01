import os
import json
from typing import Optional
import requests
from ai_skill_hub.storage import Skill


class SkillSharer:
    """Handles sharing and installing skills"""

    def share_to_gist(self, skill: Skill) -> Optional[str]:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            return None
        
        url = "https://api.github.com/gists"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        
        data = {
            "description": f"AI Skill Hub: {skill.name} - {skill.description}",
            "public": True,
            "files": {
                f"{skill.name}.yaml": {
                    "content": skill.to_yaml()
                }
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json().get("html_url")
        except Exception:
            return None

    def install_from_gist(self, gist_url: str) -> Optional[Skill]:
        gist_id = gist_url.split("/")[-1]
        
        url = f"https://api.github.com/gists/{gist_id}"
        headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            gist_data = response.json()
            
            files = gist_data.get("files", {})
            for filename, file_data in files.items():
                if filename.endswith(".yaml"):
                    content = file_data.get("content", "")
                    skill = Skill.from_yaml(content)
                    return skill
            
            return None
        except Exception:
            return None

    def share_to_github_repo(self, skill: Skill, repo_url: str) -> Optional[str]:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            return None
        
        owner_repo = repo_url.replace("https://github.com/", "").rstrip(".git")
        parts = owner_repo.split("/")
        if len(parts) != 2:
            return None
        
        owner, repo = parts
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/skills/{skill.name}.yaml"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        
        data = {
            "message": f"Add skill: {skill.name}",
            "content": skill.to_yaml(),
            "branch": "main",
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data["sha"] = response.json()["sha"]
            
            response = requests.put(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json().get("content", {}).get("html_url")
        except Exception:
            return None

    def install_from_github(self, raw_url: str) -> Optional[Skill]:
        try:
            response = requests.get(raw_url)
            response.raise_for_status()
            content = response.text
            return Skill.from_yaml(content)
        except Exception:
            return None

    def search_github_skills(self, query: str, limit: int = 10) -> list:
        token = os.environ.get("GITHUB_TOKEN")
        headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"token {token}"
        
        url = f"https://api.github.com/search/code?q={query}+extension:yaml+path:skills&per_page={limit}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get("items", [])
        except Exception:
            return []
