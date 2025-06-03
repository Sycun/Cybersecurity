import React, { KeyboardEvent } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Navigation.css';

interface NavigationTab {
  path: string;
  label: string;
  ariaLabel?: string;
}

const Navigation: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const handleNavigation = (path: string) => {
    try {
      navigate(path);
    } catch (error) {
      console.error('Navigation error:', error);
    }
  };

  const handleKeyPress = (event: KeyboardEvent<HTMLSpanElement>, path: string) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleNavigation(path);
    }
  };

  const tabs: NavigationTab[] = [
    { 
      path: '/', 
      label: '📊 题目分析',
      ariaLabel: '题目分析页面'
    },
    { 
      path: '/history', 
      label: '📝 历史记录',
      ariaLabel: '历史记录页面'
    },
    { 
      path: '/stats', 
      label: '📈 统计信息',
      ariaLabel: '统计信息页面'
    },
    { 
      path: '/performance', 
      label: '⚡ 性能监控',
      ariaLabel: '性能监控页面'
    },
    { 
      path: '/docs', 
      label: '📚 文档中心',
      ariaLabel: '文档中心页面'
    }
  ];

  return (
    <nav className="navigation-container" role="navigation" aria-label="主导航">
      {tabs.map(tab => {
        const isActive = location.pathname === tab.path;
        return (
          <span
            key={tab.path}
            className={isActive ? 'navigation-tab-active' : 'navigation-tab'}
            onClick={() => handleNavigation(tab.path)}
            onKeyDown={(event) => handleKeyPress(event, tab.path)}
            role="button"
            tabIndex={0}
            aria-label={tab.ariaLabel || tab.label}
            aria-current={isActive ? 'page' : undefined}
          >
            {tab.label}
          </span>
        );
      })}
    </nav>
  );
};

export default Navigation; 