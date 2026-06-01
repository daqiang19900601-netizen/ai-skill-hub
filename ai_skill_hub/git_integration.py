import os
from pathlib import Path
from typing import Optional

try:
    import git
    HAS_GIT = True
except ImportError:
    HAS_GIT = False


class GitManager:
    """Manages Git integration for version control"""

    def init_and_commit(self, skills_dir: Path, message: str) -> Optional[str]:
        if not HAS_GIT:
            return None
        
        try:
            repo_path = skills_dir / ".git"
            
            if repo_path.exists():
                repo = git.Repo(skills_dir)
            else:
                repo = git.Repo.init(skills_dir)
            
            repo.index.add(["*"])
            repo.index.commit(message)
            
            return repo.head.commit.hexsha[:7]
        except Exception:
            return None

    def get_history(self, skills_dir: Path, limit: int = 10) -> list:
        if not HAS_GIT:
            return []
        
        try:
            repo = git.Repo(skills_dir)
            commits = list(repo.iter_commits(max_count=limit))
            
            history = []
            for commit in commits:
                history.append({
                    "hash": commit.hexsha[:7],
                    "message": commit.message.strip(),
                    "author": str(commit.author),
                    "date": str(commit.committed_datetime),
                })
            
            return history
        except Exception:
            return []

    def push_to_remote(self, skills_dir: Path, remote_url: str, branch: str = "main") -> bool:
        if not HAS_GIT:
            return False
        
        try:
            repo = git.Repo(skills_dir)
            
            if remote_url not in [r.url for r in repo.remotes]:
                repo.create_remote("origin", remote_url)
            
            repo.remote("origin").push(branch)
            return True
        except Exception:
            return False

    def pull_from_remote(self, skills_dir: Path, remote_url: str, branch: str = "main") -> bool:
        if not HAS_GIT:
            return False
        
        try:
            repo_path = skills_dir / ".git"
            
            if repo_path.exists():
                repo = git.Repo(skills_dir)
            else:
                repo = git.Repo.init(skills_dir)
                repo.create_remote("origin", remote_url)
                repo.remotes.origin.pull(branch)
                return True
            
            repo.remotes.origin.pull(branch)
            return True
        except Exception:
            return False
