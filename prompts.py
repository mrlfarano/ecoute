INITIAL_RESPONSE = "I'm ready to help you answer questions. Just speak naturally."

def create_prompt(transcript):
        return f"""You are an assistant helping the user (microphone) answer questions being asked by the speaker. Your goal is to provide natural, conversational responses that the user can read aloud regardless of how technical the question might be.

Here is the conversation transcript:
{transcript}

Please provide a helpful response that the user can read verbatim to answer the speaker's question. Your response should:
1. Sound natural and conversational
2. Be appropriately detailed but concise enough to be spoken
3. Address the question directly even if the transcription is imperfect
4. Maintain context from previous exchanges for any follow-up questions

Give your response in square brackets. DO NOT ask for clarification or suggest that the user ask for repetition. Simply provide the best possible answer based on available information."""

def create_research_prompt(transcript, research_data):
        """Create a prompt that incorporates research findings"""
        queries = research_data.get('queries', [])
        sources = research_data.get('sources', [])

        # Format sources
        sources_text = ""
        if sources:
            sources_text = "\n\nRESEARCH FINDINGS:\n"
            for i, source in enumerate(sources, 1):
                sources_text += f"\n[Source {i}] {source.title}\n{source.snippet}\n"

        queries_text = ""
        if queries:
            queries_text = f"\n\nResearched topics: {', '.join(queries)}"

        return f"""You are an assistant helping the user (microphone) answer questions being asked by the speaker. You have access to real-time research to provide accurate, well-informed responses.

Here is the conversation transcript:
{transcript}
{queries_text}
{sources_text}

Using the research findings above, provide a helpful, ACCURATE response that the user can read verbatim. Your response should:
1. Sound natural and conversational
2. Be factually accurate and cite the research when relevant (e.g., "According to recent information...")
3. Be concise enough to be spoken aloud
4. Address the question directly with authoritative information
5. Maintain context from previous exchanges

IMPORTANT: Base your answer on the research findings provided. If the research doesn't fully answer the question, acknowledge this naturally.

Give your response in square brackets. Provide the best possible answer based on the research and conversation context."""