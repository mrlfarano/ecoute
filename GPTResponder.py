from openai import OpenAI
import os
from prompts import create_prompt, create_research_prompt, INITIAL_RESPONSE
import time
from SearchEngine import SearchEngine
from ActionTracker import ActionTracker
import threading

# Get API key from environment variable or keys.py file
try:
    from keys import OPENAI_API_KEY
    client = OpenAI(api_key=OPENAI_API_KEY)
except ImportError:
    # Fallback to environment variable
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_response_from_transcript(transcript, research_data=None):
    """Generate response with optional research context"""
    try:
        if research_data and research_data.get('has_research'):
            # Use research-enhanced prompt
            prompt = create_research_prompt(transcript, research_data)
        else:
            # Use standard prompt
            prompt = create_prompt(transcript)

        response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.6,
                max_tokens=500
        )
    except Exception as e:
        print(e)
        return '', []

    full_response = response.choices[0].message.content

    # Extract sources if available
    sources = research_data.get('sources', []) if research_data else []

    try:
        # Extract text between square brackets
        if '[' in full_response and ']' in full_response:
            return full_response.split('[')[1].split(']')[0], sources
        # Fallback if response doesn't contain square brackets
        return full_response, sources
    except Exception as e:
        print(f"Error parsing response: {e}")
        return '', sources

class GPTResponder:
    def __init__(self, enable_search=True):
        self.response = INITIAL_RESPONSE
        self.response_interval = 2
        self.sources = []  # Current sources
        self.search_engine = SearchEngine() if enable_search else None
        self.enable_search = enable_search
        self.research_queries = []  # Current research queries
        self.conversation_context = []  # Track conversation history
        self.action_tracker = ActionTracker()  # Track action items and insights

    def get_research_status(self):
        """Get current research activity for UI"""
        if not self.search_engine:
            return {"active_searches": [], "recent_searches": [], "total_sources": 0}
        return self.search_engine.get_current_activity()

    def respond_to_transcriber(self, transcriber):
        while True:
            if transcriber.transcript_changed_event.is_set():
                start_time = time.time()

                transcriber.transcript_changed_event.clear()
                transcript_string = transcriber.get_transcript()

                # Perform research if enabled
                research_data = None
                if self.enable_search and self.search_engine:
                    context = "\n".join(self.conversation_context[-3:])  # Last 3 exchanges
                    research_data = self.search_engine.research_topic(transcript_string, context)
                    self.research_queries = research_data.get('queries', [])

                # Generate response with research
                response, sources = generate_response_from_transcript(transcript_string, research_data)

                end_time = time.time()
                execution_time = end_time - start_time

                if response != '':
                    self.response = response
                    self.sources = sources
                    # Update conversation context
                    self.conversation_context.append(transcript_string)
                    if len(self.conversation_context) > 10:
                        self.conversation_context.pop(0)

                    # Extract insights and action items
                    self.action_tracker.extract_insights(transcript_string)

                remaining_time = self.response_interval - execution_time
                if remaining_time > 0:
                    time.sleep(remaining_time)
            else:
                time.sleep(0.3)

    def update_response_interval(self, interval):
        self.response_interval = interval

    def clear_context(self):
        """Clear conversation context and search history"""
        self.conversation_context.clear()
        self.sources.clear()
        self.research_queries.clear()
        if self.search_engine:
            self.search_engine.clear_history()
        self.action_tracker.clear()