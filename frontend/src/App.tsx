import { Help as HelpIcon, Security as SecurityIcon, Settings as SettingsIcon } from '@mui/icons-material';
import { AppBar, Box, Container, IconButton, Toolbar, Typography } from '@mui/material';
import { useEffect, useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import ChallengeAnalyzer from './components/ChallengeAnalyzer';
import Documentation from './components/Documentation';
import History from './components/History';
import Navigation from './components/Navigation';
import Performance from './components/Performance';
import Settings from './components/Settings';
import Stats from './components/Stats';
import UserGuide from './components/UserGuide';
import WelcomeTour from './components/WelcomeTour';

function App() {
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [guideOpen, setGuideOpen] = useState(false);

  // 检查是否为首次使用，但不自动打开完整引导
  // 改为通过WelcomeTour组件来处理首次访问体验
  useEffect(() => {
    const hasCompletedGuide = localStorage.getItem('ctf_guide_completed');
    const hasSkippedGuide = localStorage.getItem('ctf_guide_skipped');
    const hasSeenWelcome = localStorage.getItem('ctf_welcome_seen');
    
    // 只有当用户明确点击了"开始教程"时才自动显示完整引导
    // 其他情况由WelcomeTour组件处理
    const shouldAutoStartGuide = localStorage.getItem('ctf_auto_start_guide');
    if (shouldAutoStartGuide === 'true') {
      localStorage.removeItem('ctf_auto_start_guide');
      const timer = setTimeout(() => {
        setGuideOpen(true);
      }, 500);
      
      return () => clearTimeout(timer);
    }
  }, []);

  const handleOpenGuide = () => {
    setGuideOpen(true);
  };

  const handleOpenSettings = () => {
    setSettingsOpen(true);
  };

  return (
    <Box sx={{ flexGrow: 1, minHeight: '100vh', backgroundColor: 'background.default' }}>
      <AppBar position="static" sx={{ mb: 3 }}>
        <Toolbar>
          <SecurityIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            CTF智能分析平台
          </Typography>
          <Typography variant="subtitle1" sx={{ mr: 2 }}>
            多AI提供者支持 v2.1
          </Typography>
          <IconButton 
            color="inherit" 
            onClick={handleOpenGuide}
            aria-label="帮助"
            title="使用指南"
            sx={{ mr: 1 }}
          >
            <HelpIcon />
          </IconButton>
          <IconButton 
            color="inherit" 
            onClick={handleOpenSettings}
            aria-label="设置"
            title="配置设置"
          >
            <SettingsIcon />
          </IconButton>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="xl">
        <Navigation />
        <Routes>
          <Route path="/" element={<ChallengeAnalyzer />} />
          <Route path="/history" element={<History />} />
          <Route path="/stats" element={<Stats />} />
          <Route path="/performance" element={<Performance />} />
          <Route path="/docs" element={<Documentation />} />
        </Routes>
      </Container>

      <Settings 
        open={settingsOpen} 
        onClose={() => setSettingsOpen(false)} 
      />

      <UserGuide
        open={guideOpen}
        onClose={() => setGuideOpen(false)}
      />

      <WelcomeTour onOpenGuide={handleOpenGuide} />
    </Box>
  );
}

export default App; 