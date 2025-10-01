"""
Entropy Calculator for Zero Entropy RAG System

Implements entropy calculations for:
- Text entropy measurement
- Information disorder quantification  
- Uncertainty assessment
- Knowledge quality scoring

Mathematical Foundation:
Shannon Entropy: H(X) = -Σ p(x) * log2(p(x))
Zero Entropy Goal: Minimize H(X) for maximum information order
"""

import math
import re
from typing import Dict, List, Tuple, Optional
from collections import Counter
import numpy as np
from dataclasses import dataclass


@dataclass
class EntropyMetrics:
    """Complete entropy analysis results"""
    shannon_entropy: float
    normalized_entropy: float
    certainty_score: float  # 1 - normalized_entropy
    word_diversity: float
    semantic_coherence: float
    overall_quality: float


class EntropyCalculator:
    """
    Advanced entropy calculator for Zero Entropy optimization
    
    Features:
    - Shannon entropy calculation
    - Text quality assessment
    - Semantic coherence measurement
    - Information order quantification
    """
    
    def __init__(self):
        # Entropy calculation parameters
        self.min_word_length = 2
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
        }
        
    async def calculate_text_entropy(self, text: str) -> float:
        """
        Calculate Shannon entropy of text
        
        Lower entropy = more ordered/predictable = better for Zero Entropy
        Higher entropy = more chaotic/uncertain = worse for Zero Entropy
        
        Returns: Entropy value between 0 (perfect order) and ~10 (maximum chaos)
        """
        
        if not text or len(text.strip()) == 0:
            return 0.0
            
        # Preprocess text
        words = self._preprocess_text(text)
        
        if len(words) == 0:
            return 0.0
            
        # Calculate word frequency distribution
        word_counts = Counter(words)
        total_words = len(words)
        
        # Calculate Shannon entropy
        entropy = 0.0
        for count in word_counts.values():
            probability = count / total_words
            if probability > 0:
                entropy -= probability * math.log2(probability)
                
        return entropy
        
    async def calculate_comprehensive_metrics(self, text: str) -> EntropyMetrics:
        """
        Calculate comprehensive entropy and quality metrics
        
        Zero Entropy Principle: Lower values indicate better information quality
        """
        
        if not text or len(text.strip()) == 0:
            return EntropyMetrics(
                shannon_entropy=0.0,
                normalized_entropy=0.0,
                certainty_score=1.0,
                word_diversity=0.0,
                semantic_coherence=1.0,
                overall_quality=1.0
            )
            
        # Calculate basic entropy
        shannon_entropy = await self.calculate_text_entropy(text)
        
        # Calculate normalized entropy (0-1 scale)
        words = self._preprocess_text(text)
        max_possible_entropy = math.log2(len(set(words))) if len(set(words)) > 1 else 1.0
        normalized_entropy = min(1.0, shannon_entropy / max_possible_entropy)
        
        # Calculate certainty score (inverse of normalized entropy)
        certainty_score = 1.0 - normalized_entropy
        
        # Calculate word diversity (vocabulary richness)
        word_diversity = await self._calculate_word_diversity(words)
        
        # Calculate semantic coherence
        semantic_coherence = await self._calculate_semantic_coherence(text)
        
        # Calculate overall quality score
        overall_quality = await self._calculate_overall_quality(
            certainty_score, word_diversity, semantic_coherence
        )
        
        return EntropyMetrics(
            shannon_entropy=shannon_entropy,
            normalized_entropy=normalized_entropy,
            certainty_score=certainty_score,
            word_diversity=word_diversity,
            semantic_coherence=semantic_coherence,
            overall_quality=overall_quality
        )
        
    def _preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text for entropy calculation
        
        Steps:
        1. Convert to lowercase
        2. Remove punctuation and special characters  
        3. Split into words
        4. Filter short words and stop words
        """
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation and special characters, keep letters and spaces
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Split into words
        words = text.split()
        
        # Filter words
        filtered_words = []
        for word in words:
            if (len(word) >= self.min_word_length and 
                word not in self.stop_words):
                filtered_words.append(word)
                
        return filtered_words
        
    async def _calculate_word_diversity(self, words: List[str]) -> float:
        """
        Calculate word diversity (vocabulary richness)
        
        Higher diversity = more varied vocabulary = potentially higher entropy
        Lower diversity = repeated words = potentially lower entropy
        
        Returns: Value between 0 (no diversity) and 1 (maximum diversity)
        """
        
        if len(words) == 0:
            return 0.0
            
        unique_words = len(set(words))
        total_words = len(words)
        
        # Calculate diversity ratio
        diversity = unique_words / total_words
        
        return diversity
        
    async def _calculate_semantic_coherence(self, text: str) -> float:
        """
        Calculate semantic coherence of text
        
        Higher coherence = more logical flow = lower entropy
        Lower coherence = chaotic content = higher entropy
        
        Simplified implementation using structural markers
        Returns: Value between 0 (no coherence) and 1 (perfect coherence)
        """
        
        if not text or len(text.strip()) == 0:
            return 0.0
            
        sentences = self._split_into_sentences(text)
        
        if len(sentences) <= 1:
            return 1.0  # Single sentence is considered coherent
            
        coherence_factors = []
        
        # Check for transition words (indicates logical flow)
        transition_words = {
            'however', 'therefore', 'furthermore', 'moreover', 'consequently',
            'meanwhile', 'subsequently', 'additionally', 'similarly', 'likewise',
            'instead', 'otherwise', 'thus', 'hence', 'accordingly', 'finally'
        }
        
        transition_count = 0
        for sentence in sentences:
            words = sentence.lower().split()
            if any(word in transition_words for word in words):
                transition_count += 1
                
        transition_factor = min(1.0, transition_count / max(1, len(sentences) - 1))
        coherence_factors.append(transition_factor)
        
        # Check sentence length consistency (indicates structured writing)
        sentence_lengths = [len(sentence.split()) for sentence in sentences]
        if len(sentence_lengths) > 1:
            length_variance = np.var(sentence_lengths)
            mean_length = np.mean(sentence_lengths)
            length_consistency = 1.0 - min(1.0, length_variance / max(1, mean_length ** 2))
        else:
            length_consistency = 1.0
            
        coherence_factors.append(length_consistency)
        
        # Average coherence factors
        overall_coherence = np.mean(coherence_factors)
        
        return overall_coherence
        
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting (can be enhanced with NLTK or spaCy)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
        
    async def _calculate_overall_quality(
        self,
        certainty_score: float,
        word_diversity: float, 
        semantic_coherence: float
    ) -> float:
        """
        Calculate overall text quality for Zero Entropy system
        
        Quality Formula:
        - High certainty (low entropy) = good
        - Moderate diversity (not too repetitive, not too chaotic) = good  
        - High coherence = good
        
        Returns: Value between 0 (poor quality) and 1 (excellent quality)
        """
        
        # Weight factors for quality calculation
        certainty_weight = 0.4    # Most important for Zero Entropy
        diversity_weight = 0.3    # Moderate importance
        coherence_weight = 0.3    # Important for usability
        
        # Normalize diversity (optimal range is 0.3-0.7)
        optimal_diversity = 0.5
        diversity_penalty = abs(word_diversity - optimal_diversity) / optimal_diversity
        normalized_diversity = max(0.0, 1.0 - diversity_penalty)
        
        # Calculate weighted quality score
        quality_score = (
            certainty_score * certainty_weight +
            normalized_diversity * diversity_weight +
            semantic_coherence * coherence_weight
        )
        
        return min(1.0, quality_score)
        
    async def compare_entropy(self, text1: str, text2: str) -> Dict:
        """Compare entropy between two texts"""
        
        metrics1 = await self.calculate_comprehensive_metrics(text1)
        metrics2 = await self.calculate_comprehensive_metrics(text2)
        
        return {
            "text1_entropy": metrics1.shannon_entropy,
            "text2_entropy": metrics2.shannon_entropy,
            "entropy_difference": abs(metrics1.shannon_entropy - metrics2.shannon_entropy),
            "better_quality": "text1" if metrics1.overall_quality > metrics2.overall_quality else "text2",
            "quality_difference": abs(metrics1.overall_quality - metrics2.overall_quality),
            "recommendation": await self._get_entropy_recommendation(metrics1, metrics2)
        }
        
    async def _get_entropy_recommendation(
        self, 
        metrics1: EntropyMetrics, 
        metrics2: EntropyMetrics
    ) -> str:
        """Get recommendation based on entropy comparison"""
        
        if metrics1.overall_quality > metrics2.overall_quality + 0.1:
            return "Text 1 has significantly better information quality (lower entropy)"
        elif metrics2.overall_quality > metrics1.overall_quality + 0.1:
            return "Text 2 has significantly better information quality (lower entropy)" 
        else:
            return "Both texts have similar information quality"
            
    async def get_entropy_status(self, entropy_value: float) -> str:
        """Get human-readable entropy status"""
        
        if entropy_value < 2.0:
            return "Excellent (Very Low Entropy)"
        elif entropy_value < 3.5:
            return "Good (Low Entropy)"
        elif entropy_value < 5.0:
            return "Acceptable (Moderate Entropy)"
        elif entropy_value < 7.0:
            return "Poor (High Entropy)"
        else:
            return "Very Poor (Very High Entropy)"
            
    async def suggest_improvements(self, text: str) -> List[str]:
        """Suggest improvements to reduce entropy"""
        
        metrics = await self.calculate_comprehensive_metrics(text)
        suggestions = []
        
        if metrics.certainty_score < 0.6:
            suggestions.append("Reduce word repetition to decrease entropy")
            
        if metrics.word_diversity > 0.8:
            suggestions.append("Use more consistent vocabulary to improve coherence")
            
        if metrics.semantic_coherence < 0.5:
            suggestions.append("Add transition words to improve logical flow")
            suggestions.append("Ensure sentences have consistent structure")
            
        if metrics.overall_quality < 0.6:
            suggestions.append("Consider restructuring content for better information organization")
            
        if not suggestions:
            suggestions.append("Text quality is good - entropy is well-controlled")
            
        return suggestions

