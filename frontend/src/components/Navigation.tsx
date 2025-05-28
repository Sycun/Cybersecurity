// import {
//     Analytics as AnalyticsIcon,
//     History as HistoryIcon,
//     Assessment as StatsIcon
// } from '@mui/icons-material';
// import { Box, Tab, Tabs } from '@mui/material';
import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Navigation: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const handleNavigation = (path: string) => {
    navigate(path);
  };

  const navStyle: React.CSSProperties = {
    borderBottom: '1px solid #333',
    marginBottom: '24px',
    padding: '16px 0'
  };

  const tabStyle: React.CSSProperties = {
    display: 'inline-block',
    padding: '8px 16px',
    margin: '0 8px',
    cursor: 'pointer',
    borderRadius: '4px',
    backgroundColor: '#1e1e1e',
    color: '#fff',
    textDecoration: 'none'
  };

  const activeTabStyle: React.CSSProperties = {
    ...tabStyle,
    backgroundColor: '#00bcd4',
    color: '#000'
  };

  const tabs = [
    { path: '/', label: '📊 题目分析' },
    { path: '/history', label: '📝 历史记录' },
    { path: '/stats', label: '📈 统计信息' }
  ];

  return (
    <div style={navStyle}>
      {tabs.map(tab => (
        <span
          key={tab.path}
          style={location.pathname === tab.path ? activeTabStyle : tabStyle}
          onClick={() => handleNavigation(tab.path)}
        >
          {tab.label}
        </span>
      ))}
    </div>
  );
};

export default Navigation; 