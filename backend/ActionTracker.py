from openai import OpenAI
import os
import time
import re

try:
    from keys import OPENAI_API_KEY
    client = OpenAI(api_key=OPENAI_API_KEY)
except ImportError:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class ActionItem:
    """Represents a single action item or task"""
    def __init__(self, text, priority="medium", assigned_to="You", timestamp=None):
        self.text = text
        self.priority = priority  # low, medium, high
        self.assigned_to = assigned_to
        self.timestamp = timestamp or time.time()
        self.completed = False

    def __str__(self):
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
        status = "✅" if self.completed else "⏳"
        return f"{status} {priority_emoji.get(self.priority, '⚪')} {self.text} ({self.assigned_to})"


class ConversationInsights:
    """Container for conversation insights"""
    def __init__(self):
        self.key_topics = []
        self.decisions_made = []
        self.questions_raised = []
        self.action_items = []


class ActionTracker:
    """Tracks action items and conversation insights in real-time"""

    def __init__(self):
        self.action_items = []
        self.conversation_insights = ConversationInsights()
        self.last_analysis_transcript = ""

    def extract_insights(self, transcript):
        """
        Analyze conversation transcript to extract action items, key topics, and decisions
        """
        # Only analyze if transcript has changed significantly
        if len(transcript) < 50 or transcript == self.last_analysis_transcript:
            return self.conversation_insights

        self.last_analysis_transcript = transcript

        try:
            prompt = f"""Analyze this conversation transcript and extract structured insights:

{transcript}

Provide:
1. ACTION ITEMS: Tasks, TODOs, or commitments mentioned (who should do what)
2. KEY TOPICS: Main discussion points (3-5 topics)
3. DECISIONS: Any decisions or conclusions reached
4. QUESTIONS: Unanswered questions or topics needing follow-up

Format your response as:

ACTION ITEMS:
- [Priority: high/medium/low] [Person] Action description
- ...

KEY TOPICS:
- Topic 1
- Topic 2
...

DECISIONS:
- Decision 1
- Decision 2
...

QUESTIONS:
- Question 1
- Question 2
...

Only include items that are clearly present. Use "NONE" for empty sections."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=500
            )

            result = response.choices[0].message.content
            self._parse_insights(result)

        except Exception as e:
            print(f"Error extracting insights: {e}")

        return self.conversation_insights

    def _parse_insights(self, text):
        """Parse the formatted insights response"""
        insights = ConversationInsights()

        # Split into sections
        sections = {
            'ACTION ITEMS:': [],
            'KEY TOPICS:': [],
            'DECISIONS:': [],
            'QUESTIONS:': []
        }

        current_section = None
        for line in text.split('\n'):
            line = line.strip()
            if line in sections:
                current_section = line
            elif line and line.startswith('-') and current_section:
                sections[current_section].append(line.lstrip('- '))

        # Parse action items
        for item in sections.get('ACTION ITEMS:', []):
            if item.upper() == 'NONE':
                continue

            # Try to extract priority
            priority_match = re.search(r'\[Priority:\s*(high|medium|low)\]', item, re.IGNORECASE)
            priority = priority_match.group(1).lower() if priority_match else 'medium'

            # Try to extract person
            person_match = re.search(r'\[(.*?)\]', item)
            person = person_match.group(1) if person_match and 'Priority' not in person_match.group(1) else 'You'

            # Clean up text
            clean_text = re.sub(r'\[.*?\]', '', item).strip()

            if clean_text:
                action = ActionItem(clean_text, priority, person)
                insights.action_items.append(action)

        # Parse other sections
        insights.key_topics = [t for t in sections.get('KEY TOPICS:', []) if t.upper() != 'NONE']
        insights.decisions_made = [d for d in sections.get('DECISIONS:', []) if d.upper() != 'NONE']
        insights.questions_raised = [q for q in sections.get('QUESTIONS:', []) if q.upper() != 'NONE']

        self.conversation_insights = insights
        self.action_items = insights.action_items

    def get_action_items_text(self):
        """Get formatted action items for display"""
        if not self.action_items:
            return "No action items detected yet"

        text = ""
        for item in self.action_items:
            text += str(item) + "\n"
        return text

    def get_insights_summary(self):
        """Get formatted insights summary"""
        insights = self.conversation_insights

        summary = "📊 CONVERSATION INSIGHTS\n"
        summary += "="*50 + "\n\n"

        # Key Topics
        summary += "🎯 KEY TOPICS:\n"
        if insights.key_topics:
            for topic in insights.key_topics[:5]:
                summary += f"  • {topic}\n"
        else:
            summary += "  None yet\n"
        summary += "\n"

        # Decisions
        summary += "✅ DECISIONS MADE:\n"
        if insights.decisions_made:
            for decision in insights.decisions_made:
                summary += f"  • {decision}\n"
        else:
            summary += "  None yet\n"
        summary += "\n"

        # Questions
        summary += "❓ OPEN QUESTIONS:\n"
        if insights.questions_raised:
            for question in insights.questions_raised:
                summary += f"  • {question}\n"
        else:
            summary += "  None yet\n"
        summary += "\n"

        # Action Items
        summary += "📋 ACTION ITEMS:\n"
        if insights.action_items:
            for item in insights.action_items:
                summary += f"  {str(item)}\n"
        else:
            summary += "  None yet\n"

        return summary

    def clear(self):
        """Clear all tracked items"""
        self.action_items.clear()
        self.conversation_insights = ConversationInsights()
        self.last_analysis_transcript = ""
