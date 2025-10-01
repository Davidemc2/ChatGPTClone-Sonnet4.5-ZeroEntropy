"""
LLM Integration for Zero Entropy RAG System

Handles:
- OpenAI API integration
- Response generation with context injection
- Token management and optimization  
- Error handling and fallbacks

Zero Entropy Principles:
- Consistent response patterns
- Optimal context utilization
- Deterministic generation settings
"""

import asyncio
import os
from typing import Optional, Dict, List
import json
from datetime import datetime
import openai
from openai import AsyncOpenAI
import tiktoken

from ..models.chat_models import RAGContext, ChatMessage


class LLMIntegration:
    """
    LLM Integration with Zero Entropy optimization
    
    Features:
    - Structured prompt engineering
    - Context-aware response generation
    - Token optimization
    - Error resilience
    """
    
    def __init__(self):
        self.client = None
        self.model = "gpt-4o-mini"  # Fast and cost-effective
        self.max_tokens = 1000
        self.temperature = 0.3  # Low temperature for consistency (Zero Entropy)
        
        # Token management
        self.encoding = None
        self.max_context_tokens = 6000  # Leave room for response
        
        # System prompt for Zero Entropy behavior
        self.system_prompt = """You are an AI assistant enhanced with a Zero Entropy RAG system. This means:

1. PRECISION: Provide accurate, fact-based responses using the provided knowledge context
2. COHERENCE: Maintain logical consistency throughout your response
3. CLARITY: Be clear and direct, avoiding ambiguous language
4. CONTEXT: Always use the retrieved knowledge to enhance your responses
5. HONESTY: If the provided context doesn't contain relevant information, state this clearly

Your responses should be:
- Factually accurate based on the provided context
- Well-structured and easy to understand
- Consistent with previous messages in the conversation
- Enhanced by the retrieved knowledge when relevant

Remember: You have access to a knowledge base through RAG. Use it wisely."""

    async def initialize(self):
        """Initialize LLM integration"""
        print("🤖 Initializing LLM Integration...")
        
        # Get API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
            
        # Initialize OpenAI client
        self.client = AsyncOpenAI(api_key=api_key)
        
        # Initialize tokenizer
        self.encoding = tiktoken.encoding_for_model(self.model)
        
        print("✅ LLM Integration initialized")
        
    async def test_connection(self):
        """Test LLM connection"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=10,
                temperature=0
            )
            return True
        except Exception as e:
            print(f"❌ LLM connection test failed: {e}")
            return False
            
    async def generate_response(
        self, 
        message: str,
        context: RAGContext,
        conversation_history: Optional[List[ChatMessage]] = None
    ) -> str:
        """
        Generate response with RAG context integration
        
        Zero Entropy Approach:
        - Structured prompt with clear context
        - Consistent generation parameters
        - Optimal token usage
        """
        
        try:
            # Build messages for the conversation
            messages = await self._build_conversation_messages(
                message=message,
                context=context,
                conversation_history=conversation_history or []
            )
            
            # Generate response
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=0.9,  # Focused sampling for consistency
                frequency_penalty=0.1,  # Reduce repetition
                presence_penalty=0.1
            )
            
            content = response.choices[0].message.content
            
            # Post-process response
            return await self._post_process_response(content)
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return self._get_fallback_response()
            
    async def _build_conversation_messages(
        self,
        message: str,
        context: RAGContext,
        conversation_history: List[ChatMessage]
    ) -> List[Dict]:
        """Build optimized conversation messages with context"""
        
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add context if available
        if context and context.retrieved_knowledge:
            context_prompt = await self._build_context_prompt(context)
            messages.append({
                "role": "system", 
                "content": f"KNOWLEDGE CONTEXT:\n{context_prompt}"
            })
            
        # Add conversation history (limited by tokens)
        history_messages = await self._add_conversation_history(
            conversation_history, 
            max_tokens=2000
        )
        messages.extend(history_messages)
        
        # Add current user message
        messages.append({"role": "user", "content": message})
        
        # Ensure we don't exceed token limits
        messages = await self._trim_messages_to_limit(messages)
        
        return messages
        
    async def _build_context_prompt(self, context: RAGContext) -> str:
        """Build structured context prompt from RAG results"""
        
        if not context.retrieved_knowledge:
            return "No specific knowledge context available."
            
        context_parts = []
        
        # Add retrieved knowledge
        for i, knowledge in enumerate(context.retrieved_knowledge, 1):
            context_parts.append(f"[KNOWLEDGE {i}]\n{knowledge}\n")
            
        # Add metadata if available
        if context.metadata:
            total_entropy = context.metadata.get("total_entropy", 0)
            avg_confidence = context.metadata.get("average_confidence", 0)
            
            context_parts.append(
                f"[CONTEXT QUALITY]\n"
                f"Information certainty: {1-total_entropy:.2f}/1.0\n"
                f"Average confidence: {avg_confidence:.2f}/1.0\n"
            )
            
        return "\n".join(context_parts)
        
    async def _add_conversation_history(
        self, 
        history: List[ChatMessage], 
        max_tokens: int
    ) -> List[Dict]:
        """Add conversation history within token limits"""
        
        messages = []
        current_tokens = 0
        
        # Add history in reverse order (most recent first)
        for chat_msg in reversed(history):
            message_dict = {
                "role": chat_msg.role,
                "content": chat_msg.content
            }
            
            # Estimate tokens
            message_tokens = len(self.encoding.encode(chat_msg.content))
            
            if current_tokens + message_tokens > max_tokens:
                break
                
            messages.insert(0, message_dict)  # Insert at beginning
            current_tokens += message_tokens
            
        return messages
        
    async def _trim_messages_to_limit(self, messages: List[Dict]) -> List[Dict]:
        """Trim messages to fit within token limits"""
        
        total_tokens = 0
        for message in messages:
            total_tokens += len(self.encoding.encode(message["content"]))
            
        # If within limits, return as is
        if total_tokens <= self.max_context_tokens:
            return messages
            
        # Keep system message and trim from the middle
        system_messages = [msg for msg in messages if msg["role"] == "system"]
        user_messages = [msg for msg in messages if msg["role"] != "system"]
        
        # Start with system messages
        trimmed_messages = system_messages.copy()
        current_tokens = sum(len(self.encoding.encode(msg["content"])) 
                           for msg in system_messages)
        
        # Add user messages from the end (most recent)
        for message in reversed(user_messages):
            message_tokens = len(self.encoding.encode(message["content"]))
            
            if current_tokens + message_tokens > self.max_context_tokens:
                break
                
            trimmed_messages.insert(-1 if len(trimmed_messages) > 1 else 0, message)
            current_tokens += message_tokens
            
        return trimmed_messages
        
    async def _post_process_response(self, response: str) -> str:
        """Post-process response for Zero Entropy optimization"""
        
        if not response:
            return self._get_fallback_response()
            
        # Clean up response
        response = response.strip()
        
        # Remove potential model artifacts
        response = response.replace("```", "")  # Remove code block markers if misused
        
        return response
        
    def _get_fallback_response(self) -> str:
        """Get fallback response when generation fails"""
        return ("I apologize, but I'm experiencing technical difficulties "
                "generating a response. Please try rephrasing your question or "
                "try again in a moment.")
                
    async def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
        
    async def get_model_info(self) -> Dict:
        """Get current model information"""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "max_context_tokens": self.max_context_tokens,
            "status": "active"
        }
        
    async def update_settings(self, settings: Dict):
        """Update LLM settings"""
        if "temperature" in settings:
            self.temperature = max(0.0, min(1.0, settings["temperature"]))
        if "max_tokens" in settings:
            self.max_tokens = max(100, min(2000, settings["max_tokens"]))
        if "model" in settings and settings["model"] in ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]:
            self.model = settings["model"]
            
        print(f"✅ LLM settings updated: temp={self.temperature}, tokens={self.max_tokens}")
        
    async def shutdown(self):
        """Shutdown LLM integration"""
        print("🔄 Shutting down LLM Integration...")
        # No explicit cleanup needed for OpenAI client