/**
 * Design Theme - Apple/Johnny Ive Inspired
 * 
 * Principles:
 * - Minimal color palette for clarity
 * - Generous whitespace for breathing room
 * - Typography hierarchy for information order
 * - Subtle animations for delight
 * - Zero entropy visual design
 */

export const theme = {
  colors: {
    // Primary colors - inspired by Apple's design system
    primary: '#007AFF',
    primaryHover: '#0056CC',
    primaryLight: '#E3F3FF',
    
    // Background colors - clean and minimal
    background: '#FFFFFF',
    backgroundSecondary: '#F8F9FA',
    backgroundTertiary: '#F1F3F4',
    
    // Text colors - high contrast for readability
    text: '#1A1A1A',
    textSecondary: '#666666',
    textTertiary: '#9B9B9B',
    textInverse: '#FFFFFF',
    
    // UI element colors
    border: '#E5E5E5',
    borderLight: '#F0F0F0',
    borderDark: '#D1D1D1',
    
    // State colors
    success: '#34C759',
    warning: '#FF9500',
    error: '#FF3B30',
    
    // Chat-specific colors
    userMessage: '#007AFF',
    assistantMessage: '#F8F9FA',
    systemMessage: '#E3F3FF',
    
    // Entropy visualization colors
    lowEntropy: '#34C759',    // Green for good quality
    mediumEntropy: '#FF9500', // Orange for medium quality  
    highEntropy: '#FF3B30',   // Red for poor quality
  },
  
  typography: {
    // Font families - Apple system fonts
    primary: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif",
    monospace: "'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace",
    
    // Font sizes - modular scale
    sizes: {
      xs: '12px',
      sm: '14px',
      base: '16px',
      lg: '18px',
      xl: '20px',
      '2xl': '24px',
      '3xl': '30px',
      '4xl': '36px',
    },
    
    // Font weights
    weights: {
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
    },
    
    // Line heights
    lineHeights: {
      tight: 1.2,
      normal: 1.5,
      relaxed: 1.6,
      loose: 1.8,
    },
  },
  
  spacing: {
    // Spacing scale - based on 8px grid
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    '2xl': '48px',
    '3xl': '64px',
    '4xl': '96px',
  },
  
  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    full: '50%',
  },
  
  shadows: {
    // Subtle shadows for depth
    sm: '0 1px 2px rgba(0, 0, 0, 0.05)',
    md: '0 4px 8px rgba(0, 0, 0, 0.1)',
    lg: '0 8px 16px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 40px rgba(0, 0, 0, 0.1)',
  },
  
  transitions: {
    // Smooth, natural animations
    default: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
    fast: 'all 0.15s cubic-bezier(0.4, 0, 0.2, 1)',
    slow: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  },
  
  breakpoints: {
    // Responsive breakpoints
    mobile: '480px',
    tablet: '768px',
    desktop: '1024px',
    wide: '1200px',
  },
  
  zIndex: {
    // Z-index scale
    dropdown: 1000,
    sticky: 1100,
    modal: 1200,
    popover: 1300,
    tooltip: 1400,
  },
  
  // Component-specific theme values
  components: {
    header: {
      height: '64px',
      background: 'rgba(255, 255, 255, 0.8)',
      backdropFilter: 'blur(20px)',
    },
    
    sidebar: {
      width: '280px',
      background: '#F8F9FA',
    },
    
    chat: {
      maxWidth: '800px',
      messageSpacing: '16px',
      avatarSize: '32px',
    },
    
    input: {
      height: '48px',
      borderRadius: '12px',
      focusBorderColor: '#007AFF',
    },
    
    button: {
      height: '44px',
      borderRadius: '8px',
      fontWeight: 500,
    },
  },
};

// Type definitions for TypeScript
export type Theme = typeof theme;

// Utility functions for theme usage
export const getColor = (colorPath: string) => {
  const keys = colorPath.split('.');
  let value: any = theme.colors;
  
  for (const key of keys) {
    value = value?.[key];
  }
  
  return value || colorPath;
};

export const getSpacing = (size: keyof typeof theme.spacing) => {
  return theme.spacing[size];
};

export const getFontSize = (size: keyof typeof theme.typography.sizes) => {
  return theme.typography.sizes[size];
};

// Media query helpers
export const media = {
  mobile: `@media (max-width: ${theme.breakpoints.mobile})`,
  tablet: `@media (max-width: ${theme.breakpoints.tablet})`,
  desktop: `@media (min-width: ${theme.breakpoints.desktop})`,
  wide: `@media (min-width: ${theme.breakpoints.wide})`,
};

export default theme;

