import threading
from AudioTranscriber import AudioTranscriber
from GPTResponder import GPTResponder
from DeepDive import open_deep_dive
import customtkinter as ctk
import AudioRecorder
import queue
import time
import sys
import TranscriberModels
import subprocess

def write_in_textbox(textbox, text):
    textbox.delete("0.0", "end")
    textbox.insert("0.0", text)

def update_transcript_UI(transcriber, textbox):
    transcript_string = transcriber.get_transcript()
    write_in_textbox(textbox, transcript_string)
    textbox.after(300, update_transcript_UI, transcriber, textbox)

def update_response_UI(responder, response_textbox, research_textbox, sources_textbox, insights_textbox):
    # Update response
    response_text = str(responder.response)
    write_in_textbox(response_textbox, response_text)

    # Update research activity
    research_status = responder.get_research_status()
    active_searches = research_status.get('active_searches', [])
    recent_searches = research_status.get('recent_searches', [])

    research_text = "🔍 RESEARCH ACTIVITY\n" + "="*40 + "\n\n"
    if active_searches:
        research_text += "⏳ Currently Researching:\n"
        for query in active_searches:
            research_text += f"  → {query}\n"
        research_text += "\n"

    if recent_searches:
        research_text += "📚 Recent Searches:\n"
        for query in recent_searches[-5:]:
            research_text += f"  • {query}\n"
    else:
        research_text += "No active research\n"

    write_in_textbox(research_textbox, research_text)

    # Update sources
    sources_text = "📖 SOURCES\n" + "="*40 + "\n\n"
    if responder.sources:
        for i, source in enumerate(responder.sources, 1):
            sources_text += f"[{i}] {source.title}\n"
            sources_text += f"    {source.snippet[:150]}...\n\n"
    else:
        sources_text += "No sources available yet\n"

    write_in_textbox(sources_textbox, sources_text)

    # Update insights and action items
    insights_text = responder.action_tracker.get_insights_summary()
    write_in_textbox(insights_textbox, insights_text)

    response_textbox.after(500, update_response_UI, responder, response_textbox, research_textbox, sources_textbox, insights_textbox)

def clear_context(transcriber, responder, speaker_queue, mic_queue):
    transcriber.clear_transcript_data()

    if responder:
        responder.clear_context()

    with speaker_queue.mutex:
        speaker_queue.queue.clear()
    with mic_queue.mutex:
        mic_queue.queue.clear()

def create_ui_components(root, transcriber, responder, speaker_queue, mic_queue):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root.title("Ecoute - AI Research Assistant")
    root.geometry("1600x900")

    root.grid_columnconfigure(0, weight=2)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # Left panel - Transcript
    left_frame = ctk.CTkFrame(root)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
    left_frame.grid_columnconfigure(0, weight=1)
    left_frame.grid_rowconfigure(0, weight=0)
    left_frame.grid_rowconfigure(1, weight=2)
    left_frame.grid_rowconfigure(2, weight=1)
    left_frame.grid_rowconfigure(3, weight=0)

    # Title
    title_label = ctk.CTkLabel(
        left_frame,
        text="🎧 LIVE TRANSCRIPT",
        font=("Arial", 18, "bold")
    )
    title_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

    # Transcript box
    transcript_textbox = ctk.CTkTextbox(
        left_frame,
        font=("Arial", 16),
        text_color='#FFFCF2',
        wrap="word"
    )
    transcript_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

    # Response box
    response_label = ctk.CTkLabel(
        left_frame,
        text="💡 SUGGESTED RESPONSE",
        font=("Arial", 16, "bold")
    )
    response_label.grid(row=2, column=0, sticky="ew", padx=10, pady=(10, 0))

    response_textbox = ctk.CTkTextbox(
        left_frame,
        font=("Arial", 14),
        text_color='#90EE90',
        wrap="word"
    )
    response_textbox.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

    # Clear button
    clear_button = ctk.CTkButton(
        left_frame,
        text="Clear Context",
        command=lambda: clear_context(transcriber, responder, speaker_queue, mic_queue),
        height=40
    )
    clear_button.grid(row=4, column=0, sticky="ew", padx=10, pady=(5, 10))

    # Right panel - Research & Sources
    right_frame = ctk.CTkFrame(root)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
    right_frame.grid_columnconfigure(0, weight=1)
    right_frame.grid_rowconfigure(0, weight=0)
    right_frame.grid_rowconfigure(1, weight=1)
    right_frame.grid_rowconfigure(2, weight=0)
    right_frame.grid_rowconfigure(3, weight=2)
    right_frame.grid_rowconfigure(4, weight=0)

    # Research activity
    research_label = ctk.CTkLabel(
        right_frame,
        text="🔍 RESEARCH ACTIVITY",
        font=("Arial", 14, "bold")
    )
    research_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

    research_textbox = ctk.CTkTextbox(
        right_frame,
        font=("Courier", 11),
        text_color='#87CEEB',
        wrap="word"
    )
    research_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

    # Sources
    sources_label = ctk.CTkLabel(
        right_frame,
        text="📖 SOURCES & CITATIONS",
        font=("Arial", 14, "bold")
    )
    sources_label.grid(row=2, column=0, sticky="ew", padx=10, pady=(10, 5))

    sources_textbox = ctk.CTkTextbox(
        right_frame,
        font=("Arial", 11),
        text_color='#FFD700',
        wrap="word"
    )
    sources_textbox.grid(row=3, column=0, sticky="nsew", padx=10, pady=(5, 5))

    # Deep Dive section
    dive_frame = ctk.CTkFrame(right_frame)
    dive_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=(5, 10))
    dive_frame.grid_columnconfigure(0, weight=1)
    dive_frame.grid_columnconfigure(1, weight=0)

    dive_entry = ctk.CTkEntry(
        dive_frame,
        placeholder_text="Enter topic for deep dive research...",
        font=("Arial", 12)
    )
    dive_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

    def trigger_deep_dive():
        topic = dive_entry.get().strip()
        if topic and responder.search_engine:
            open_deep_dive(root, topic, responder.search_engine)
            dive_entry.delete(0, 'end')

    dive_button = ctk.CTkButton(
        dive_frame,
        text="🔬 Deep Dive",
        command=trigger_deep_dive,
        width=120
    )
    dive_button.grid(row=0, column=1, sticky="e")

    # Bind Enter key to trigger deep dive
    dive_entry.bind('<Return>', lambda e: trigger_deep_dive())

    # Third column - Insights panel
    insights_frame = ctk.CTkFrame(root)
    insights_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 20), pady=20)
    insights_frame.grid_columnconfigure(0, weight=1)
    insights_frame.grid_rowconfigure(0, weight=0)
    insights_frame.grid_rowconfigure(1, weight=1)

    insights_label = ctk.CTkLabel(
        insights_frame,
        text="📊 CONVERSATION INSIGHTS",
        font=("Arial", 14, "bold")
    )
    insights_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

    insights_textbox = ctk.CTkTextbox(
        insights_frame,
        font=("Arial", 11),
        text_color='#FFA500',
        wrap="word"
    )
    insights_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

    return transcript_textbox, response_textbox, research_textbox, sources_textbox, insights_textbox

def main():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("ERROR: The ffmpeg library is not installed. Please install ffmpeg and try again.")
        return

    root = ctk.CTk()
    speaker_queue = queue.Queue()
    mic_queue = queue.Queue()

    user_audio_recorder = AudioRecorder.DefaultMicRecorder()
    user_audio_recorder.record_into_queue(mic_queue)

    time.sleep(2)

    speaker_audio_recorder = AudioRecorder.DefaultSpeakerRecorder()
    speaker_audio_recorder.record_into_queue(speaker_queue)

    model = TranscriberModels.get_model('--api' in sys.argv)

    transcriber = AudioTranscriber(user_audio_recorder.source, speaker_audio_recorder.source, model)
    transcribe = threading.Thread(target=transcriber.transcribe_audio_queue, args=(speaker_queue, mic_queue))
    transcribe.daemon = True
    transcribe.start()

    # Initialize GPT Responder with search enabled
    responder = GPTResponder(enable_search=True)
    respond = threading.Thread(target=responder.respond_to_transcriber, args=(transcriber,))
    respond.daemon = True
    respond.start()

    # Create UI components
    transcript_textbox, response_textbox, research_textbox, sources_textbox, insights_textbox = create_ui_components(
        root, transcriber, responder, speaker_queue, mic_queue
    )

    print("READY - AI Research Assistant Initialized")

    # Start UI update loops
    update_transcript_UI(transcriber, transcript_textbox)
    update_response_UI(responder, response_textbox, research_textbox, sources_textbox, insights_textbox)

    root.mainloop()

if __name__ == "__main__":
    main()