import random
import re
from typing import Dict, Any
from app.schemas.audit import AuditResponse, AuditIssue

class AuditEngine:
    def __init__(self):
        # Weighted logic configuration
        self.weights = {
            "engagement": 0.30,
            "consistency": 0.20,
            "bio": 0.10,
            "pinned": 0.10,
            "content_safety": 0.20,
            "link_hygiene": 0.10
        }

    async def analyze_channel(self, link: str, reported_issue: str) -> AuditResponse:
        """
        Executes a simulated audit of the provided Telegram entity.
        In a full production environment, this would call the Telegram API
        to fetch real metadata (bio, post frequency, views).
        """
        # --- Simulated Logic for Production Readiness ---
        # 1. Basic Link Validation
        is_valid_link = bool(re.search(r"(t\.me/|@)[a-zA-Z0-9_]{5,}", link))
        
        # 2. Heuristic Scoring (Simulating API metrics)
        metrics = {
            "engagement": random.randint(40, 95) if is_valid_link else 10,
            "consistency": random.randint(50, 100),
            "bio": 80 if len(link) > 10 else 30,
            "pinned": 100 if random.choice([True, False]) else 0,
            "content_safety": 75 if "destination quality" not in reported_issue.lower() else 40,
            "link_hygiene": 60
        }

        # 3. Calculate Weighted Score
        final_score = sum(metrics[k] * self.weights[k] for k in self.weights)
        
        # 4. Generate Specific Issues
        detected_issues = self._identify_issues(metrics, reported_issue)
        
        risk_level = "Low" if final_score > 80 else "Medium" if final_score > 50 else "High"
        prob = "High" if final_score > 85 else "Moderate" if final_score > 60 else "Low"

        return AuditResponse(
            score=int(final_score),
            risk_level=risk_level,
            approval_probability=prob,
            issues=detected_issues
        )

    def _identify_issues(self, metrics: Dict[str, int], issue_type: str) -> list:
        issues = []
        if metrics["content_safety"] < 50:
            issues.append(AuditIssue(
                description="Aggressive marketing language detected in recent posts.",
                severity="High",
                recommendation="Remove 'guaranteed profit' or 'click now' phrases to pass destination quality checks."
            ))
        if metrics["engagement"] < 50:
            issues.append(AuditIssue(
                description="Low view-to-subscriber ratio.",
                severity="Medium",
                recommendation="Increase organic engagement before applying for ads to avoid 'Low Quality' flags."
            ))
        if metrics["link_hygiene"] < 70:
            issues.append(AuditIssue(
                description="High frequency of external redirects.",
                severity="Medium",
                recommendation="Use internal Telegram links (t.me) where possible to improve trust score."
            ))
        return issues

# Instantiate for use in routers
audit_service = AuditEngine()
