/**
 * Entropy Indicator - Visual representation of Zero Entropy metrics
 * 
 * Features:
 * - Color-coded entropy levels
 * - Smooth animations
 * - Tooltip with detailed metrics
 * - Compact and full display modes
 */

import React, { useState } from 'react';
import styled from 'styled-components';

interface EntropyIndicatorProps {
  entropy: number;
  quality?: number;
  compact?: boolean;
  style?: React.CSSProperties;
}

const IndicatorContainer = styled.div<{ compact: boolean }>`
  display: flex;
  align-items: center;
  gap: ${props => props.compact ? props.theme.spacing.xs : props.theme.spacing.sm};
  font-size: ${props => props.compact ? props.theme.typography.sizes.xs : props.theme.typography.sizes.sm};
  color: ${props => props.theme.colors.textSecondary};
`;

const EntropyBar = styled.div<{ compact: boolean }>`
  position: relative;
  width: ${props => props.compact ? '60px' : '80px'};
  height: ${props => props.compact ? '4px' : '6px'};
  background-color: ${props => props.theme.colors.backgroundSecondary};
  border-radius: 3px;
  overflow: hidden;
`;

const EntropyFill = styled.div<{ 
  level: number; 
  quality: 'excellent' | 'good' | 'fair' | 'poor';
}>`
  height: 100%;
  width: ${props => Math.min(props.level * 20, 100)}%;
  background: linear-gradient(90deg, 
    ${props => {
      switch (props.quality) {
        case 'excellent': return props.theme.colors.lowEntropy;
        case 'good': return props.theme.colors.lowEntropy;
        case 'fair': return props.theme.colors.mediumEntropy;
        case 'poor': return props.theme.colors.highEntropy;
        default: return props.theme.colors.mediumEntropy;
      }
    }},
    ${props => {
      switch (props.quality) {
        case 'excellent': return props.theme.colors.lowEntropy + 'AA';
        case 'good': return props.theme.colors.lowEntropy + 'AA';
        case 'fair': return props.theme.colors.mediumEntropy + 'AA';
        case 'poor': return props.theme.colors.highEntropy + 'AA';
        default: return props.theme.colors.mediumEntropy + 'AA';
      }
    }}
  );
  transition: ${props => props.theme.transitions.slow};
  border-radius: 3px;
  
  animation: ${props => props.quality === 'excellent' ? 'pulse 2s infinite' : 'none'};
  
  @keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
  }
`;

const EntropyLabel = styled.div<{ compact: boolean }>`
  display: ${props => props.compact ? 'none' : 'flex'};
  align-items: center;
  gap: ${props => props.theme.spacing.xs};
  font-weight: ${props => props.theme.typography.weights.medium};
`;

const EntropyValue = styled.span<{ quality: string }>`
  color: ${props => {
    switch (props.quality) {
      case 'excellent': return props.theme.colors.lowEntropy;
      case 'good': return props.theme.colors.lowEntropy;
      case 'fair': return props.theme.colors.mediumEntropy;
      case 'poor': return props.theme.colors.highEntropy;
      default: return props.theme.colors.textSecondary;
    }
  }};
  font-weight: ${props => props.theme.typography.weights.semibold};
`;

const QualityIcon = styled.span`
  font-size: 12px;
`;

const Tooltip = styled.div<{ show: boolean }>`
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: ${props => props.theme.colors.text};
  color: ${props => props.theme.colors.textInverse};
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius.md};
  font-size: ${props => props.theme.typography.sizes.xs};
  white-space: nowrap;
  box-shadow: ${props => props.theme.shadows.md};
  opacity: ${props => props.show ? 1 : 0};
  visibility: ${props => props.show ? 'visible' : 'hidden'};
  transition: ${props => props.theme.transitions.default};
  z-index: 1000;
  margin-bottom: 8px;
  
  &::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 5px solid transparent;
    border-top-color: ${props => props.theme.colors.text};
  }
`;

const TooltipContainer = styled.div`
  position: relative;
  display: flex;
  align-items: center;
`;

const MetricRow = styled.div`
  display: flex;
  justify-content: space-between;
  margin: 2px 0;
`;

const EntropyIndicator: React.FC<EntropyIndicatorProps> = ({ 
  entropy, 
  quality, 
  compact = false,
  style 
}) => {
  const [showTooltip, setShowTooltip] = useState(false);

  // Determine quality level based on entropy and quality score
  const getQualityLevel = (): 'excellent' | 'good' | 'fair' | 'poor' => {
    if (quality !== undefined) {
      if (quality > 0.8) return 'excellent';
      if (quality > 0.6) return 'good';
      if (quality > 0.4) return 'fair';
      return 'poor';
    }
    
    // Fallback to entropy-based quality
    if (entropy < 2.0) return 'excellent';
    if (entropy < 3.5) return 'good';
    if (entropy < 5.0) return 'fair';
    return 'poor';
  };

  const getQualityText = (qualityLevel: string): string => {
    switch (qualityLevel) {
      case 'excellent': return 'Excellent';
      case 'good': return 'Good';
      case 'fair': return 'Fair';
      case 'poor': return 'Poor';
      default: return 'Unknown';
    }
  };

  const getQualityIcon = (qualityLevel: string): string => {
    switch (qualityLevel) {
      case 'excellent': return '🟢';
      case 'good': return '🟡';
      case 'fair': return '🟠';
      case 'poor': return '🔴';
      default: return '⚫';
    }
  };

  const qualityLevel = getQualityLevel();

  const handleMouseEnter = () => {
    setShowTooltip(true);
  };

  const handleMouseLeave = () => {
    setShowTooltip(false);
  };

  return (
    <IndicatorContainer 
      compact={compact} 
      style={style}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <TooltipContainer>
        <EntropyBar compact={compact}>
          <EntropyFill level={entropy} quality={qualityLevel} />
        </EntropyBar>
        
        <Tooltip show={showTooltip}>
          <div>
            <strong>Zero Entropy Metrics</strong>
            <MetricRow>
              <span>Shannon Entropy:</span>
              <span>{entropy.toFixed(2)}</span>
            </MetricRow>
            {quality !== undefined && (
              <MetricRow>
                <span>Quality Score:</span>
                <span>{(quality * 100).toFixed(0)}%</span>
              </MetricRow>
            )}
            <MetricRow>
              <span>Status:</span>
              <span>{getQualityText(qualityLevel)}</span>
            </MetricRow>
            <hr style={{ margin: '4px 0', opacity: 0.3 }} />
            <div style={{ fontSize: '10px', opacity: 0.8 }}>
              Lower entropy = Higher quality
            </div>
          </div>
        </Tooltip>
      </TooltipContainer>
      
      <EntropyLabel compact={compact}>
        <QualityIcon>{getQualityIcon(qualityLevel)}</QualityIcon>
        <span>Quality:</span>
        <EntropyValue quality={qualityLevel}>
          {getQualityText(qualityLevel)}
        </EntropyValue>
        {!compact && (
          <span style={{ opacity: 0.7 }}>
            ({entropy.toFixed(2)})
          </span>
        )}
      </EntropyLabel>
    </IndicatorContainer>
  );
};

export default EntropyIndicator;