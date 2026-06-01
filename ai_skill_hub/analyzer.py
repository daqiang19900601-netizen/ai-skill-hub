from ai_skill_hub.storage import Skill
from typing import List, Dict, Optional
import re

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False


class SkillAnalyzer:
    """Analyzes skills for optimization and metrics"""

    def analyze(self, skill: Skill) -> Dict:
        content = skill.content
        token_count = self._count_tokens(content)
        char_count = len(content)
        word_count = len(content.split())
        complexity = self._assess_complexity(content)
        suggestions = self._generate_suggestions(content, token_count, complexity)

        return {
            "token_count": token_count,
            "char_count": char_count,
            "word_count": word_count,
            "complexity": complexity,
            "suggestions": suggestions,
        }

    def _count_tokens(self, text: str) -> int:
        if HAS_TIKTOKEN:
            try:
                encoding = tiktoken.get_encoding("cl100k_base")
                return len(encoding.encode(text))
            except Exception:
                pass
        return len(text) // 4

    def _assess_complexity(self, text: str) -> str:
        lines = text.split("\n")
        sections = len([l for l in lines if l.strip().startswith("#")])
        has_examples = "example" in text.lower()
        has_variables = "{" in text and "}" in text
        
        score = 0
        score += min(sections * 2, 20)
        score += 10 if has_examples else 0
        score += 10 if has_variables else 0
        
        if score < 15:
            return "Simple"
        elif score < 30:
            return "Medium"
        else:
            return "Complex"

    def _generate_suggestions(self, text: str, token_count: int, complexity: str) -> List[str]:
        suggestions = []
        
        if token_count > 4000:
            suggestions.append("Consider breaking this skill into smaller, focused sub-skills")
        
        if token_count > 8000:
            suggestions.append("Very long prompt - AI models may lose context. Consider using external references")
        
        if not any(marker in text for marker in ["#", "##", "###"]):
            suggestions.append("Add markdown headers for better structure")
        
        if "example" not in text.lower():
            suggestions.append("Add examples to improve AI understanding")
        
        if complexity == "Complex":
            suggestions.append("Consider simplifying for better reliability")
        
        if len(text.split("\n")) < 5:
            suggestions.append("Consider adding more structure with sections")
        
        repeated_words = self._find_repeated_patterns(text)
        if repeated_words:
            suggestions.append(f"Remove repeated patterns: {', '.join(repeated_words[:3])}")
        
        return suggestions if suggestions else ["Looking good! No major improvements needed."]

    def _find_repeated_patterns(self, text: str) -> List[str]:
        words = text.lower().split()
        word_counts = {}
        for word in words:
            if len(word) > 5:
                word_counts[word] = word_counts.get(word, 0) + 1
        
        return [w for w, c in word_counts.items() if c > 3]

    def relevance_score(self, skill: Skill, query: str) -> float:
        query_lower = query.lower()
        score = 0.0
        
        if query_lower in skill.name.lower():
            score += 40
        if query_lower in skill.description.lower():
            score += 30
        if query_lower in skill.content.lower():
            score += 20
        for tag in skill.tags:
            if query_lower in tag.lower():
                score += 10
        
        return min(score, 100.0)
