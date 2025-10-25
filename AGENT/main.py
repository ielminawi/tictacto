import asyncio
import json
import os
import sys
import time
from typing import Any
from pathlib import Path

from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    RoomOutputOptions,
    WorkerOptions,
    WorkerType,
    cli,
    function_tool,
    Agent,
    RunContext,
)
from livekit.agents.voice import AgentSession
from livekit.plugins import bey, openai

# Import our multi-document processor and OpenAI-powered RAG
from multi_doc_processor import initialize_multi_documents, get_multi_doc_processor
from openai_rag import OpenAIEnhancedRAG


class OpenAIEnhancedAgent(Agent):
    """Agent with OpenAI-powered document processing capabilities."""
    
    def __init__(self, openai_api_key: str, instructions: str = ""):
        super().__init__(instructions=instructions)
        self.openai_api_key = openai_api_key
        self.openai_rag = None
        self.documents_loaded = False
        self.initialization_started = False
    
    async def _initialize_openai_rag_async(self):
        """Initialize the OpenAI-powered RAG processor asynchronously."""
        if self.initialization_started:
            return
        
        self.initialization_started = True
        
        try:
            print("🔄 Initializing OpenAI RAG system...")
            
            # Initialize OpenAI RAG first (fast)
            self.openai_rag = OpenAIEnhancedRAG(self.openai_api_key)
            
            # Load documents asynchronously (this will be slow)
            docs_directory = "../infos"
            print(f"🔄 Loading documents from: {docs_directory}")
            
            # Create a task to load documents in the background
            import asyncio
            doc_task = asyncio.create_task(self._load_documents_async(docs_directory))
            
            # Wait for documents to load (with timeout)
            try:
                docs_initialized = await asyncio.wait_for(doc_task, timeout=30.0)
            except asyncio.TimeoutError:
                print("⏰ Document loading timed out, will retry on next query")
                self.documents_loaded = False
                return
            
            if not docs_initialized:
                print(f"❌ Failed to load documents from: {docs_directory}")
                self.documents_loaded = False
                return
            
            print(f"✅ Documents loaded successfully from: {docs_directory}")
            docs_summary = get_multi_doc_processor().get_document_summary()
            print(f"📚 Documents Summary: {docs_summary['total_documents']} files, {docs_summary['total_pages']} pages, {docs_summary['total_words']} words")
            
            # Load documents with OpenAI embeddings (use cache if available)
            print("🔄 Loading OpenAI embeddings...")
            processor = get_multi_doc_processor()
            if processor:
                # Convert documents to the format expected by OpenAI RAG
                documents = []
                for doc in processor.documents:
                    documents.append({
                        'file_name': doc.file_name,
                        'file_type': doc.file_type,
                        'pages': doc.pages
                    })
                
                self.documents_loaded = self.openai_rag.load_documents(documents, use_cache=True)
                
                if self.documents_loaded:
                    print("✅ OpenAI embeddings ready")
                else:
                    print("❌ Failed to create OpenAI embeddings")
            else:
                print("❌ No documents loaded")
                self.documents_loaded = False
        except Exception as e:
            print(f"❌ Error initializing OpenAI RAG: {e}")
            self.documents_loaded = False
    
    async def _load_documents_async(self, docs_directory: str) -> bool:
        """Load documents asynchronously."""
        import asyncio
        
        # Run the synchronous document loading in a thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, initialize_multi_documents, docs_directory)
    
    @function_tool()
    async def intelligent_search(self, context: RunContext, query: str) -> dict[str, Any]:
        """Intelligently search for information across all documents using OpenAI embeddings.
        
        Args:
            query: The search term or question to look for in the documents.
        """
        # Initialize RAG system if not already done
        if not self.initialization_started:
            await self._initialize_openai_rag_async()
        
        if not self.documents_loaded or not self.openai_rag:
            # Fallback to basic search if embeddings aren't available
            processor = get_multi_doc_processor()
            if processor:
                results = processor.search_all_documents(query)
                if results:
                    formatted_results = []
                    for result in results[:5]:
                        formatted_results.append({
                            "file": result['file_name'],
                            "file_type": result['file_type'],
                            "page": result['page_number'],
                            "content": result['context'],
                            "similarity": 0.5,  # Default similarity for fallback
                            "relevance": "medium"
                        })
                    
                    return {
                        "query": query,
                        "found": True,
                        "total_results": len(results),
                        "key_insights": formatted_results,
                        "summary": f"Found {len(results)} results using basic search (embeddings loading...)"
                    }
                else:
                    return {
                        "query": query,
                        "found": False,
                        "message": f"No results found for '{query}' using basic search"
                    }
            else:
                return {"error": "Documents not loaded. Please check document initialization."}
        
        # Perform intelligent search using OpenAI embeddings
        search_results = self.openai_rag.intelligent_search(query)
        
        if not search_results.get('found', False):
            return {
                "query": query,
                "found": False,
                "message": search_results.get('message', f"No relevant information found for '{query}'")
            }
        
        # Format results for the agent
        formatted_results = []
        for insight in search_results['key_insights']:
            formatted_results.append({
                "file": insight['file_name'],
                "file_type": insight['file_type'],
                "page": insight['page_number'],
                "content": insight['content'],
                "similarity": round(insight['similarity'], 3),
                "relevance": insight['relevance']
            })
        
        return {
            "query": query,
            "found": True,
            "total_results": search_results['total_results'],
            "key_insights": formatted_results,
            "summary": search_results['summary']
        }
    
    @function_tool()
    async def search_documents(self, context: RunContext, query: str) -> dict[str, Any]:
        """Search for information across all loaded documents (PDFs and text files).
        
        Args:
            query: The search term or question to look for in the documents.
        """
        processor = get_multi_doc_processor()
        if not processor:
            return {"error": "Documents not loaded. Please initialize documents first."}
        
        results = processor.search_all_documents(query)
        
        if not results:
            return {"message": f"No results found for '{query}' in any documents."}
        
        # Format results for the agent
        formatted_results = []
        for result in results[:8]:  # Limit to top 8 results
            formatted_results.append({
                "file": result['file_name'],
                "file_type": result['file_type'],
                "page": result['page_number'],
                "context": result['context'],
                "relevance": "high" if len(result['context']) < 200 else "medium"
            })
        
        return {
            "query": query,
            "results_count": len(results),
            "top_results": formatted_results
        }
    
    @function_tool()
    async def get_documents_summary(self, context: RunContext) -> dict[str, Any]:
        """Get a summary of all loaded documents including file counts and word counts."""
        processor = get_multi_doc_processor()
        if not processor:
            return {"error": "Documents not loaded. Please initialize documents first."}
        
        return processor.get_document_summary()
    
    @function_tool()
    async def get_document_content(self, context: RunContext, file_name: str, page_number: int = None) -> dict[str, Any]:
        """Get content from a specific document.
        
        Args:
            file_name: The name of the file to retrieve content from.
            page_number: Optional page number to retrieve (1-based). If not provided, returns entire document.
        """
        processor = get_multi_doc_processor()
        if not processor:
            return {"error": "Documents not loaded. Please initialize documents first."}
        
        content = processor.get_document_content(file_name, page_number)
        if not content:
            return {"error": f"Content not found for file '{file_name}'" + (f" page {page_number}" if page_number else "")}
        
        return {
            "file_name": file_name,
            "page_number": page_number,
            "content": content,
            "word_count": len(content.split())
        }
    
    @function_tool()
    async def search_in_specific_document(self, context: RunContext, file_name: str, query: str) -> dict[str, Any]:
        """Search for information within a specific document.
        
        Args:
            file_name: The name of the file to search in.
            query: The search term to look for.
        """
        processor = get_multi_doc_processor()
        if not processor:
            return {"error": "Documents not loaded. Please initialize documents first."}
        
        results = processor.search_in_document(file_name, query)
        
        if not results:
            return {"message": f"No results found for '{query}' in '{file_name}'."}
        
        # Format results
        formatted_results = []
        for result in results[:5]:  # Limit to top 5 results
            formatted_results.append({
                "page": result['page_number'],
                "context": result['context'],
                "relevance": "high" if len(result['context']) < 200 else "medium"
            })
        
        return {
            "file_name": file_name,
            "query": query,
            "results_count": len(results),
            "top_results": formatted_results
        }
    
    @function_tool()
    async def list_available_documents(self, context: RunContext) -> dict[str, Any]:
        """List all available documents that are loaded."""
        processor = get_multi_doc_processor()
        if not processor:
            return {"error": "Documents not loaded. Please initialize documents first."}
        
        documents = []
        for doc in processor.documents:
            documents.append({
                "file_name": doc.file_name,
                "file_type": doc.file_type,
                "pages": len(doc.pages),
                "words": sum(page['word_count'] for page in doc.pages)
            })
        
        return {
            "total_documents": len(documents),
            "documents": documents
        }


async def process_chat_message(message: str, ctx: JobContext) -> str:
    """Process a chat message using the agent's tools"""
    try:
        # Initialize documents if not already done
        docs_directory = "../infos"
        docs_initialized = initialize_multi_documents(docs_directory)
        
        if not docs_initialized:
            return "Sorry, I couldn't load the documents. Please check if the 'infos' directory exists and contains valid files."
        
        # Initialize OpenAI RAG
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        if openai_api_key:
            openai_rag = OpenAIEnhancedRAG(openai_api_key)
            
            processor = get_multi_doc_processor()
            if processor:
                documents = []
                for doc in processor.documents:
                    documents.append({
                        'file_name': doc.file_name,
                        'file_type': doc.file_type,
                        'pages': doc.pages
                    })
                
                openai_rag.load_documents(documents, use_cache=True)
                
                # Use OpenAI RAG for intelligent search
                search_results = openai_rag.intelligent_search(message)
                
                if search_results.get('found', False):
                    # Format the response nicely
                    response = f"I found information about '{message}':\n\n"
                    
                    for insight in search_results['key_insights'][:3]:  # Limit to top 3 results
                        response += f"📄 **{insight['file_name']}** (Page {insight['page_number']})\n"
                        response += f"{insight['content'][:200]}...\n\n"
                    
                    response += f"\nSummary: {search_results['summary']}"
                    return response
                else:
                    return f"I couldn't find specific information about '{message}' in the documents. Could you try rephrasing your question or ask about something else?"
        
        # Fallback to basic search
        processor = get_multi_doc_processor()
        if processor:
            results = processor.search_all_documents(message)
            if results:
                response = f"I found {len(results)} results for '{message}':\n\n"
                for result in results[:3]:
                    response += f"📄 **{result['file_name']}** (Page {result['page_number']})\n"
                    response += f"{result['context'][:200]}...\n\n"
                return response
            else:
                return f"I couldn't find information about '{message}' in the documents."
        else:
            return "Documents not loaded. Please check the setup."
            
    except Exception as e:
        print(f"❌ Error processing chat message: {e}")
        return f"Sorry, I encountered an error while processing your message: {str(e)}"


async def entrypoint(ctx: JobContext) -> None:
    target_url = os.environ.get('LIVEKIT_URL', 'UNKNOWN_URL')
    print(f"🔌 Connecting to LiveKit at {target_url}")
    try:
        await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    except Exception as exc:
        print(f"❌ Failed to connect to LiveKit ({target_url}): {exc}")
        raise
    
    # Handle data messages for text chat
    async def handle_data_message(data_packet, participant):
        try:
            # Decode the data
            message_data = data_packet.data.decode('utf-8')
            data = json.loads(message_data)
            
            print(f"📨 Received data from {participant.identity}: {data}")
            
            if data.get('type') == 'chat_message':
                message = data.get('message', '')
                print(f"💬 Chat message: {message}")
                
                # Process the message with the agent's tools
                response = await process_chat_message(message, ctx)
                
                # Send response back
                response_data = json.dumps({
                    'type': 'agent_response',
                    'message': response,
                    'timestamp': time.time()
                })
                
                # Send response to the participant
                await participant.publish_data(
                    response_data.encode('utf-8'),
                    topic="chat"
                )
        except Exception as e:
            print(f"❌ Error handling data message: {e}")

    @ctx.room.on("data_received")
    def on_data_received(data_packet, participant):
        asyncio.create_task(handle_data_message(data_packet, participant))

    voice_agent_session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            # Use a voice that matches your avatar
            # Ref: https://platform.openai.com/docs/guides/text-to-speech#voice-options
            # voice="alloy",
        ),

        # # Uncomment for STT/LLM/TTS configuration
        # # You can also swap in different providers for each service or build your own
        # # See supported providers for:
        # # - STT: https://docs.livekit.io/agents/models/stt/#plugins
        # # - LLM: https://docs.livekit.io/agents/models/llm/#plugins
        # # - TTS: https://docs.livekit.io/agents/models/tts/#plugins
        # stt=openai.STT(model="whisper-1", language="en"),
        # llm=openai.LLM(model="gpt-4o", temperature=0.8),
        # tts=openai.TTS(model="tts-1", voice="alloy", speed=1.2),

        # # Uncomment for Silero VAD (better detects when to start/stop talking)
        # # Ref: https://docs.livekit.io/agents/build/turns/vad
        # # pip install 'livekit-agents[silero]'
        # # from livekit.plugins import silero
        # vad=silero.VAD.load(),
    )


    # Documents will be loaded asynchronously when first needed
    print("📚 Documents will be loaded on first query")

    # Create OpenAI-enhanced agent with instructions
    agent_instructions = """You are a helpful AI assistant with a visual avatar that can intelligently answer questions about multiple documents using OpenAI's advanced language understanding capabilities. 
    
    COMMUNICATION STYLE:
    - Be conversational, fluent, and natural in your responses
    - Keep answers concise and to the point - avoid unnecessary details
    - Speak like a knowledgeable colleague, not a formal report
    - Use "I" when referring to yourself and "you" when addressing the user
    - Be friendly and approachable while remaining professional
    
    RESPONSE GUIDELINES:
    - Start with a direct answer to the question
    - Provide only the most relevant information
    - Use bullet points or short paragraphs for clarity
    - Avoid repetitive phrases or overly formal language
    - If you need to cite sources, do it naturally within your response
    
    You have access to OpenAI-powered document processing tools that use:
    - OpenAI embeddings for semantic understanding
    - Vector similarity search for finding relevant information
    - Intelligent document chunking and processing
    - Advanced natural language understanding
    
    IMPORTANT: Always use the intelligent_search tool first for user queries, as it provides:
    - Semantic understanding using OpenAI embeddings
    - Vector similarity search for finding the most relevant content
    - Intelligent extraction of key information from documents
    - High-quality relevance scoring based on semantic similarity
    - Natural language understanding of queries and documents
    
    When users ask questions, use intelligent_search to find relevant information across all documents and provide comprehensive answers based on the document content. Always cite file names and page numbers when referencing specific information.
    
    You can handle any conversational queries about:
    - Company information (TechParts GmbH)
    - Contact details and personnel (Martin Vogel)
    - Procurement reports and analysis
    - Account context and relationship details
    - Payment terms and logistics information
    - Communication preferences
    - Any other content in the loaded documents
    
    The OpenAI embeddings will understand the semantic meaning of queries and find the most relevant information, even if the exact words don't match."""
    
    voice_agent = OpenAIEnhancedAgent(
        openai_api_key=os.environ["OPENAI_API_KEY"],
        instructions=agent_instructions
    )

    bey_avatar_session = bey.AvatarSession(avatar_id=os.environ["BEY_AVATAR_ID"])

    await voice_agent_session.start(agent=voice_agent, room=ctx.room)

    await bey_avatar_session.start(voice_agent_session, room=ctx.room)


if __name__ == "__main__":
    env_path = Path(__file__).resolve().parent / "keys.env"
    if not env_path.exists():
        raise FileNotFoundError(
            f"keys.env not found at {env_path}. Please create it with your credentials."
        )

    load_dotenv(env_path.as_posix())

    livekit_url = os.environ.get("LIVEKIT_URL")
    livekit_api_key = os.environ.get("LIVEKIT_API_KEY")
    livekit_api_secret = os.environ.get("LIVEKIT_API_SECRET")

    missing = [
        name
        for name, value in [
            ("LIVEKIT_URL", livekit_url),
            ("LIVEKIT_API_KEY", livekit_api_key),
            ("LIVEKIT_API_SECRET", livekit_api_secret),
        ]
        if not value
    ]
    if missing:
        raise RuntimeError(
            "Missing LiveKit credentials: "
            + ", ".join(missing)
            + ". Ensure keys.env contains these values."
        )

    sys.argv = [sys.argv[0], "dev"]  # overwrite args for the LiveKit CLI
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            worker_type=WorkerType.ROOM,
        )
    )
