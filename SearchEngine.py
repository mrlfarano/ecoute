import threading
import time
from typing import List, Dict, Optional
from openai import OpenAI
import os
import re

try:
    from keys import OPENAI_API_KEY
    client = OpenAI(api_key=OPENAI_API_KEY)
except ImportError:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class SearchResult:
    """Represents a single search result with source information"""
    def __init__(self, title: str, url: str, snippet: str, source_type: str = "web"):
        self.title = title
        self.url = url
        self.snippet = snippet
        self.source_type = source_type
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source_type": self.source_type,
            "timestamp": self.timestamp
        }

    def __str__(self):
        return f"[{self.title}]({self.url})\n{self.snippet}"


class SearchEngine:
    """Handles intelligent search queries and tracks research activity"""

    def __init__(self):
        self.search_history = []
        self.current_searches = []  # Tracks ongoing searches
        self.search_lock = threading.Lock()
        self.callbacks = []  # UI update callbacks

    def register_callback(self, callback):
        """Register a callback for when search status changes"""
        self.callbacks.append(callback)

    def _notify_callbacks(self):
        """Notify all registered callbacks of state change"""
        for callback in self.callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Callback error: {e}")

    def extract_search_queries(self, transcript: str, conversation_context: str = "") -> List[str]:
        """
        Use GPT to intelligently extract what needs to be researched from the conversation
        """
        try:
            prompt = f"""Analyze this conversation and identify what topics need real-time research to provide an accurate, helpful response.

Conversation:
{transcript}

Previous context:
{conversation_context}

Extract 0-3 specific search queries that would help answer questions or provide accurate information.
Only suggest searches for:
- Factual claims that need verification
- Technical topics that need current/accurate information
- Specific questions about products, companies, or recent events
- Complex topics that benefit from authoritative sources

Return ONLY the search queries, one per line. If no research is needed, return "NONE".
Be specific and focused. Examples:
- "latest Python 3.12 features"
- "GPT-4 API pricing 2024"
- "difference between REST and GraphQL"
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=150
            )

            result = response.choices[0].message.content.strip()

            if result == "NONE" or not result:
                return []

            queries = [q.strip() for q in result.split('\n') if q.strip() and not q.strip().startswith('-')]
            # Remove markdown list markers
            queries = [re.sub(r'^[-*]\s*', '', q) for q in queries]
            return queries[:3]  # Max 3 searches

        except Exception as e:
            print(f"Error extracting search queries: {e}")
            return []

    def search_web(self, query: str) -> List[SearchResult]:
        """
        Perform web search using OpenAI's web search capabilities.
        This is a placeholder - you can integrate with Tavily, Brave, or other search APIs.
        For now, we'll use a simulated approach.
        """
        with self.search_lock:
            self.current_searches.append(query)
            self._notify_callbacks()

        try:
            # TODO: Integrate with actual search API (Tavily, Brave Search, etc.)
            # For now, use GPT to generate research-based responses

            prompt = f"""Research the following topic and provide authoritative information with sources:

Query: {query}

Provide a comprehensive answer based on reliable sources. Include:
1. Key facts and findings
2. Important context
3. Recent developments (if applicable)

Format your response as factual information that could be cited."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=400
            )

            content = response.choices[0].message.content

            # Create a search result
            # In a real implementation, this would be multiple results from a search API
            result = SearchResult(
                title=f"Research: {query}",
                url=f"search:{query.replace(' ', '+')}",
                snippet=content[:300] + "..." if len(content) > 300 else content,
                source_type="ai_research"
            )

            results = [result]

            # Store in history
            with self.search_lock:
                self.search_history.append({
                    "query": query,
                    "results": results,
                    "timestamp": time.time()
                })
                if query in self.current_searches:
                    self.current_searches.remove(query)
                self._notify_callbacks()

            return results

        except Exception as e:
            print(f"Search error for '{query}': {e}")
            with self.search_lock:
                if query in self.current_searches:
                    self.current_searches.remove(query)
                self._notify_callbacks()
            return []

    def get_current_activity(self) -> Dict:
        """Get current search activity for UI display"""
        with self.search_lock:
            return {
                "active_searches": list(self.current_searches),
                "recent_searches": [h["query"] for h in self.search_history[-5:]],
                "total_sources": sum(len(h["results"]) for h in self.search_history)
            }

    def get_all_sources(self) -> List[SearchResult]:
        """Get all search results from current session"""
        with self.search_lock:
            all_results = []
            for search in self.search_history:
                all_results.extend(search["results"])
            return all_results

    def clear_history(self):
        """Clear search history"""
        with self.search_lock:
            self.search_history.clear()
            self.current_searches.clear()
            self._notify_callbacks()

    def research_topic(self, transcript: str, context: str = "") -> Dict:
        """
        Main research method: Extracts queries, performs searches, returns comprehensive results
        """
        # Extract what needs to be researched
        queries = self.extract_search_queries(transcript, context)

        if not queries:
            return {
                "queries": [],
                "sources": [],
                "has_research": False
            }

        # Perform searches (could be done in parallel for speed)
        all_sources = []
        for query in queries:
            results = self.search_web(query)
            all_sources.extend(results)

        return {
            "queries": queries,
            "sources": all_sources,
            "has_research": True
        }
