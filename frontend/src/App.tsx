import { Security as SecurityIcon, Settings as SettingsIcon } from '@mui/icons-material';
import { AppBar, Box, Container, IconButton, Toolbar, Typography } from '@mui/material';
import { useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import ChallengeAnalyzer from './components/ChallengeAnalyzer';
import History from './components/History';
import Navigation from './components/Navigation';
import Performance from './components/Performance';
import Settings from './components/Settings';
import Stats from './components/Stats';

function App() {
  const [settingsOpen, setSettingsOpen] = useState(false);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" sx={{ mb: 3 }}>
        <Toolbar>
          <SecurityIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            CTF智能分析平台
          </Typography>
          <Typography variant="subtitle1" sx={{ mr: 2 }}>
            多AI提供者支持 v2.0
          </Typography>
          <IconButton 
            color="inherit" 
            onClick={() => setSettingsOpen(true)}
            aria-label="设置"
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
        </Routes>
      </Container>

      <Settings 
        open={settingsOpen} 
        onClose={() => setSettingsOpen(false)} 
      />
    </Box>
  );
}

export default App; 