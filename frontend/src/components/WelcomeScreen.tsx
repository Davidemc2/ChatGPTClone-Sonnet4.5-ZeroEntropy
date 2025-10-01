/**
 * Welcome Screen - Initial state when no conversations exist
 * 
 * Features:
 * - Apple-inspired minimal design
 * - Engaging introduction to Zero Entropy
 * - Quick start suggestions
 * - Beautiful animations
 */

import React from 'react';
import styled from 'styled-components';

interface WelcomeScreenProps {
  onStartChat: () => void;
}

const WelcomeContainer = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: ${props => props.theme.spacing['4xl']};
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    padding: ${props => props.theme.spacing.xl};
  }
`;

const LogoSection = styled.div`
  margin-bottom: ${props => props.theme.spacing['3xl']};
  animation: fadeInUp 1s cubic-bezier(0.4, 0, 0.2, 1);
  
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

const Logo = styled.div`
  width: 120px;
  height: 120px;
  margin: 0 auto ${props => props.theme.spacing.lg};
  background: linear-gradient(135deg, ${props => props.theme.colors.primary}, ${props => props.theme.colors.primaryHover});
  border-radius: ${props => props.theme.borderRadius.xl};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 48px;
  font-weight: bold;
  box-shadow: ${props => props.theme.shadows.lg};
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
    transform: rotate(45deg);
    animation: shimmer 3s infinite;
  }
  
  @keyframes shimmer {
    0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
    100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
  }
`;

const Title = styled.h1`
  font-size: ${props => props.theme.typography.sizes['4xl']};
  font-weight: ${props => props.theme.typography.weights.bold};
  color: ${props => props.theme.colors.text};
  margin: 0 0 ${props => props.theme.spacing.md} 0;
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    font-size: ${props => props.theme.typography.sizes['3xl']};
  }
`;

const Subtitle = styled.p`
  font-size: ${props => props.theme.typography.sizes.lg};
  color: ${props => props.theme.colors.textSecondary};
  margin: 0 0 ${props => props.theme.spacing.xl} 0;
  line-height: ${props => props.theme.typography.lineHeights.relaxed};
  
  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    font-size: ${props => props.theme.typography.sizes.base};
  }
`;

const FeaturesSection = styled.div`
  margin-bottom: ${props => props.theme.spacing['3xl']};
  animation: fadeInUp 1s cubic-bezier(0.4, 0, 0.2, 1) 0.2s both;
`;

const FeatureList = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: ${props => props.theme.spacing.xl};
  margin-bottom: ${props => props.theme.spacing.xl};
`;

const Feature = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: ${props => props.theme.spacing.lg};
  border-radius: ${props => props.theme.borderRadius.lg};
  background-color: ${props => props.theme.colors.backgroundSecondary};
  border: 1px solid ${props => props.theme.colors.borderLight};
  transition: ${props => props.theme.transitions.default};
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: ${props => props.theme.shadows.md};
    border-color: ${props => props.theme.colors.primary}30;
  }
`;

const FeatureIcon = styled.div`
  font-size: 32px;
  margin-bottom: ${props => props.theme.spacing.sm};
`;

const FeatureTitle = styled.h3`
  font-size: ${props => props.theme.typography.sizes.base};
  font-weight: ${props => props.theme.typography.weights.semibold};
  color: ${props => props.theme.colors.text};
  margin: 0 0 ${props => props.theme.spacing.xs} 0;
`;

const FeatureDescription = styled.p`
  font-size: ${props => props.theme.typography.sizes.sm};
  color: ${props => props.theme.colors.textSecondary};
  margin: 0;
  text-align: center;
  line-height: ${props => props.theme.typography.lineHeights.normal};
`;

const QuickStartSection = styled.div`
  animation: fadeInUp 1s cubic-bezier(0.4, 0, 0.2, 1) 0.4s both;
`;

const QuickStartTitle = styled.h2`
  font-size: ${props => props.theme.typography.sizes.xl};
  font-weight: ${props => props.theme.typography.weights.semibold};
  color: ${props => props.theme.colors.text};
  margin: 0 0 ${props => props.theme.spacing.lg} 0;
`;

const SuggestionList = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.sm};
  margin-bottom: ${props => props.theme.spacing.xl};
`;

const SuggestionItem = styled.button`
  padding: ${props => props.theme.spacing.md} ${props => props.theme.spacing.lg};
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: ${props => props.theme.borderRadius.lg};
  background-color: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text};
  font-size: ${props => props.theme.typography.sizes.sm};
  text-align: left;
  cursor: pointer;
  transition: ${props => props.theme.transitions.default};
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.sm};
  
  &:hover {
    border-color: ${props => props.theme.colors.primary};
    background-color: ${props => props.theme.colors.primary}05;
    transform: translateX(4px);
  }
  
  &::before {
    content: '💡';
    font-size: 16px;
  }
`;

const StartButton = styled.button`
  padding: ${props => props.theme.spacing.md} ${props => props.theme.spacing.xl};
  background: linear-gradient(135deg, ${props => props.theme.colors.primary}, ${props => props.theme.colors.primaryHover});
  color: white;
  border: none;
  border-radius: ${props => props.theme.borderRadius.lg};
  font-size: ${props => props.theme.typography.sizes.base};
  font-weight: ${props => props.theme.typography.weights.semibold};
  cursor: pointer;
  transition: ${props => props.theme.transitions.default};
  box-shadow: ${props => props.theme.shadows.md};
  position: relative;
  overflow: hidden;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: ${props => props.theme.shadows.lg};
  }
  
  &:active {
    transform: translateY(0);
  }
  
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
  }
  
  &:active::before {
    width: 300px;
    height: 300px;
  }
`;

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onStartChat }) => {
  const suggestions = [
    "Explain quantum computing in simple terms",
    "Help me write a professional email",
    "What are the latest developments in AI?",
    "Create a meal plan for healthy eating",
  ];

  const features = [
    {
      icon: "🧠",
      title: "Zero Entropy",
      description: "Advanced RAG system with minimal uncertainty for more accurate responses"
    },
    {
      icon: "⚡",
      title: "Fast & Reliable",
      description: "Lightning-fast responses powered by optimized AI architecture"
    },
    {
      icon: "🎯",
      title: "Context-Aware",
      description: "Maintains conversation context and learns from your interactions"
    }
  ];

  return (
    <WelcomeContainer>
      <LogoSection>
        <Logo>∅</Logo>
        <Title>Zero Entropy Chat</Title>
        <Subtitle>
          Experience AI conversations with minimal uncertainty and maximum clarity
        </Subtitle>
      </LogoSection>

      <FeaturesSection>
        <FeatureList>
          {features.map((feature, index) => (
            <Feature key={index}>
              <FeatureIcon>{feature.icon}</FeatureIcon>
              <FeatureTitle>{feature.title}</FeatureTitle>
              <FeatureDescription>{feature.description}</FeatureDescription>
            </Feature>
          ))}
        </FeatureList>
      </FeaturesSection>

      <QuickStartSection>
        <QuickStartTitle>Try asking me about:</QuickStartTitle>
        
        <SuggestionList>
          {suggestions.map((suggestion, index) => (
            <SuggestionItem
              key={index}
              onClick={() => {
                onStartChat();
                // In a real implementation, you'd also auto-fill this suggestion
              }}
            >
              {suggestion}
            </SuggestionItem>
          ))}
        </SuggestionList>
        
        <StartButton onClick={onStartChat}>
          Start Your First Conversation
        </StartButton>
      </QuickStartSection>
    </WelcomeContainer>
  );
};

export default WelcomeScreen;