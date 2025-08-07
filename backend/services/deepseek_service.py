# backend/services/deepseek_service.py
import os
import numpy as np
from typing import List, Optional, Any
from langchain.llms.base import LLM
from langchain.embeddings.base import Embeddings
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class DeepSeekLLM(LLM):
    """Custom LLM wrapper for DeepSeek API"""
    
    client: Any = None
    model: str = "deepseek-chat"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.model = "deepseek-chat"
    
    @property
    def _llm_type(self) -> str:
        return "deepseek"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> str:
        """Call DeepSeek API with the given prompt"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                stream=False,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling DeepSeek API: {str(e)}"


class DeepSeekEmbeddings(Embeddings):
    """Custom embeddings wrapper for DeepSeek API"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        # DeepSeek might not have embeddings endpoint, so we'll use a fallback
        # You can replace this with actual DeepSeek embeddings if available
        try:
            # Test if embeddings endpoint exists
            self.client.embeddings.create(
                model="text-embedding-ada-002",  # Test model
                input="test"
            )
            self.has_embeddings = True
        except:
            self.has_embeddings = False
            print("⚠️  DeepSeek embeddings not available, using simple text-based embeddings")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents"""
        if self.has_embeddings:
            try:
                embeddings = []
                for text in texts:
                    response = self.client.embeddings.create(
                        model="text-embedding-ada-002",
                        input=text
                    )
                    embeddings.append(response.data[0].embedding)
                return embeddings
            except Exception as e:
                print(f"Error with DeepSeek embeddings: {e}")
                return self._fallback_embeddings(texts)
        else:
            return self._fallback_embeddings(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        if self.has_embeddings:
            try:
                response = self.client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=text
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"Error with DeepSeek embeddings: {e}")
                return self._fallback_embedding(text)
        else:
            return self._fallback_embedding(text)
    
    def _fallback_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Simple fallback embeddings based on text characteristics"""
        embeddings = []
        for text in texts:
            embeddings.append(self._fallback_embedding(text))
        return embeddings
    
    def _fallback_embedding(self, text: str) -> List[float]:
        """Create a simple embedding based on text characteristics"""
        # This is a very basic fallback - in production you'd want to use
        # a proper embedding model like sentence-transformers
        words = text.lower().split()
        
        # Create a 384-dimensional vector based on text features
        features = [
            len(text),
            len(words),
            len(set(words)),  # unique words
            text.count('.'),
            text.count(','),
            text.count('python'),
            text.count('javascript'),
            text.count('experience'),
            text.count('skills'),
            text.count('project'),
        ]
        
        # Pad or truncate to 384 dimensions
        embedding = features + [0.0] * (384 - len(features))
        embedding = embedding[:384]
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = [x / norm for x in embedding]
        
        return embedding


def get_deepseek_llm(**kwargs) -> DeepSeekLLM:
    """Factory function to create DeepSeek LLM instance"""
    return DeepSeekLLM(**kwargs)


def get_deepseek_embeddings(**kwargs) -> DeepSeekEmbeddings:
    """Factory function to create DeepSeek Embeddings instance"""
    return DeepSeekEmbeddings(**kwargs)
