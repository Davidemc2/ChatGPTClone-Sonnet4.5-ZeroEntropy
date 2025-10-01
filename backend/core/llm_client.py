"""
LLM Client - Unified interface for language models

Supports:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Compatible APIs
"""

import os
from typing import List, Dict, Optional, AsyncIterator
from loguru import logger
from openai import AsyncOpenAI
import tiktoken


class LLMClient:
    """
    Unified LLM client with streaming support
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
        
        if not self.api_key:
            logger.warning("No OPENAI_API_KEY found. LLM functionality will be limited.")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=self.api_key)
        
        # Initialize tokenizer for token counting
        try:
            self.encoding = tiktoken.encoding_for_model(self.model_name)
        except KeyError:
            self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Count tokens in messages"""
        try:
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # Every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(self.encoding.encode(value))
            num_tokens += 2  # Every reply is primed with <im_start>assistant
            return num_tokens
        except Exception as e:
            logger.warning(f"Error counting tokens: {e}")
            # Rough estimate: 4 chars per token
            total_chars = sum(len(msg.get("content", "")) for msg in messages)
            return total_chars // 4
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ):
        """
        Generate LLM response
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Override default temperature
            max_tokens: Override default max tokens
            stream: Whether to stream response
            
        Returns:
            Response text (if not streaming) or async iterator (if streaming)
        """
        if not self.client:
            raise ValueError("LLM client not initialized. Check OPENAI_API_KEY.")
        
        try:
            temperature = temperature if temperature is not None else self.temperature
            max_tokens = max_tokens if max_tokens is not None else self.max_tokens
            
            # Log token usage
            token_count = self.count_tokens(messages)
            logger.debug(f"Generating response with {token_count} input tokens")
            
            if stream:
                return self._stream_response(messages, temperature, max_tokens)
            else:
                response = await self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    async def _stream_response(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> AsyncIterator[str]:
        """Stream response from LLM"""
        try:
            stream = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            raise
    
    async def generate_summary(
        self,
        text: str,
        max_length: int = 100
    ) -> str:
        """
        Generate a summary of text
        Useful for memory consolidation
        """
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that creates concise summaries."
            },
            {
                "role": "user",
                "content": f"Summarize the following text in {max_length} words or less:\n\n{text}"
            }
        ]
        
        try:
            summary = await self.generate_response(
                messages,
                temperature=0.3,
                max_tokens=max_length * 2
            )
            return summary
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return text[:max_length * 4]  # Fallback: truncate
    
    async def extract_keywords(self, text: str) -> List[str]:
        """
        Extract key terms from text
        Useful for metadata generation
        """
        messages = [
            {
                "role": "system",
                "content": "Extract 5-10 key terms or phrases from the text. Return as comma-separated list."
            },
            {
                "role": "user",
                "content": text
            }
        ]
        
        try:
            keywords_str = await self.generate_response(
                messages,
                temperature=0.3,
                max_tokens=100
            )
            keywords = [k.strip() for k in keywords_str.split(",")]
            return keywords
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def get_model_info(self) -> Dict[str, any]:
        """Get information about current model configuration"""
        return {
            "model": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "api_configured": self.client is not None
        }
