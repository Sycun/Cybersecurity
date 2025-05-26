// import {
//     Analytics as AnalyticsIcon,
//     History as HistoryIcon,
//     Assessment as StatsIcon
// } from '@mui/icons-material';
// import { Box, Tab, Tabs } from '@mui/material';
// import React from 'react';
// import { useLocation, useNavigate } from 'react-router-dom';

// 临时解决方案：使用简单的文本图标
const AnalyticsIcon = () => '📊';
const HistoryIcon = () => '📝';
const StatsIcon = () => '📈';

// 纯JavaScript导航组件，避免所有依赖问题
function Navigation() {
  const currentPath = window.location.pathname;
  
  const handleNavigation = (path) => {
    window.history.pushState({}, '', path);
    window.dispatchEvent(new PopStateEvent('popstate'));
  };

  const navStyle = {
    borderBottom: '1px solid #333',
    marginBottom: '24px',
    padding: '16px 0'
  };

  const tabStyle = {
    display: 'inline-block',
    padding: '8px 16px',
    margin: '0 8px',
    cursor: 'pointer',
    borderRadius: '4px',
    backgroundColor: '#1e1e1e',
    color: '#fff',
    textDecoration: 'none'
  };

  const activeTabStyle = {
    ...tabStyle,
    backgroundColor: '#00bcd4',
    color: '#000'
  };

  // 创建DOM元素
  const nav = document.createElement('div');
  Object.assign(nav.style, navStyle);

  const tabs = [
    { path: '/', label: '📊 题目分析' },
    { path: '/history', label: '📝 历史记录' },
    { path: '/stats', label: '📈 统计信息' }
  ];

  tabs.forEach(tab => {
    const span = document.createElement('span');
    span.textContent = tab.label;
    Object.assign(span.style, currentPath === tab.path ? activeTabStyle : tabStyle);
    span.onclick = () => handleNavigation(tab.path);
    nav.appendChild(span);
  });

  return nav;
}

export default Navigation; 