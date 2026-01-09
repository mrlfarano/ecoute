import threading
import customtkinter as ctk
from SearchEngine import SearchEngine
from openai import OpenAI
import os

try:
    from keys import OPENAI_API_KEY
    client = OpenAI(api_key=OPENAI_API_KEY)
except ImportError:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class DeepDiveWindow:
    """Separate window for deep-dive research on a specific topic"""

    def __init__(self, parent, topic, search_engine):
        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"Deep Dive: {topic}")
        self.window.geometry("1000x700")

        self.topic = topic
        self.search_engine = search_engine
        self.research_results = []

        self._create_ui()
        self._start_research()

    def _create_ui(self):
        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=0)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=2)
        self.window.grid_rowconfigure(3, weight=0)

        # Title
        title = ctk.CTkLabel(
            self.window,
            text=f"🔬 Deep Dive Research: {self.topic}",
            font=("Arial", 20, "bold")
        )
        title.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        # Status label
        self.status_label = ctk.CTkLabel(
            self.window,
            text="🔍 Researching...",
            font=("Arial", 14)
        )
        self.status_label.grid(row=1, column=0, sticky="ew", padx=20, pady=5)

        # Results textbox
        self.results_textbox = ctk.CTkTextbox(
            self.window,
            font=("Arial", 13),
            wrap="word"
        )
        self.results_textbox.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        # Close button
        close_btn = ctk.CTkButton(
            self.window,
            text="Close",
            command=self.window.destroy,
            height=40
        )
        close_btn.grid(row=3, column=0, sticky="ew", padx=20, pady=(5, 20))

    def _start_research(self):
        """Start deep dive research in background thread"""
        thread = threading.Thread(target=self._perform_deep_research)
        thread.daemon = True
        thread.start()

    def _perform_deep_research(self):
        """Perform comprehensive research on the topic"""
        try:
            # Generate comprehensive research queries
            queries = self._generate_research_queries()

            self.status_label.configure(text=f"🔍 Researching {len(queries)} aspects...")

            # Perform searches
            all_sources = []
            for query in queries:
                sources = self.search_engine.search_web(query)
                all_sources.extend(sources)

            # Generate comprehensive summary
            self.status_label.configure(text="📝 Generating comprehensive analysis...")
            summary = self._generate_summary(all_sources)

            # Display results
            self._display_results(summary, all_sources)

            self.status_label.configure(text="✅ Research Complete")

        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {str(e)}")
            print(f"Deep dive error: {e}")

    def _generate_research_queries(self):
        """Generate multiple research angles for comprehensive coverage"""
        try:
            prompt = f"""Generate 5 specific, diverse research queries to thoroughly understand this topic: "{self.topic}"

The queries should cover:
1. Basic definition and overview
2. Technical details or mechanisms
3. Real-world applications or examples
4. Recent developments or current state (2024-2026)
5. Related concepts or comparisons

Return only the queries, one per line."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=200
            )

            queries_text = response.choices[0].message.content.strip()
            queries = [q.strip().lstrip('0123456789.- ') for q in queries_text.split('\n') if q.strip()]
            return queries[:5]

        except Exception as e:
            print(f"Error generating queries: {e}")
            return [self.topic]  # Fallback to basic query

    def _generate_summary(self, sources):
        """Generate comprehensive summary from research"""
        try:
            sources_text = "\n\n".join([
                f"Source {i+1}: {s.title}\n{s.snippet}"
                for i, s in enumerate(sources)
            ])

            prompt = f"""Based on the following research sources about "{self.topic}", create a comprehensive, well-structured analysis:

{sources_text}

Provide:
1. **Overview**: Clear explanation of what this is
2. **Key Points**: Important facts and concepts (bullet points)
3. **Details**: Technical or nuanced information
4. **Current State**: Recent developments or current status
5. **Practical Implications**: Real-world applications or significance

Format with clear sections. Be thorough but concise."""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Error generating summary. See sources below."

    def _display_results(self, summary, sources):
        """Display research results in the textbox"""
        result_text = f"""{'='*80}
COMPREHENSIVE ANALYSIS
{'='*80}

{summary}

{'='*80}
SOURCES ({len(sources)} found)
{'='*80}

"""

        for i, source in enumerate(sources, 1):
            result_text += f"\n[{i}] {source.title}\n"
            result_text += f"    {source.snippet}\n"
            result_text += f"    Type: {source.source_type}\n\n"

        self.results_textbox.delete("0.0", "end")
        self.results_textbox.insert("0.0", result_text)


def open_deep_dive(parent, topic, search_engine):
    """Open a deep dive research window for a topic"""
    DeepDiveWindow(parent, topic, search_engine)
