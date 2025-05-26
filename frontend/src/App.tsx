import { Security as SecurityIcon } from '@mui/icons-material';
import { AppBar, Box, Container, Toolbar, Typography } from '@mui/material';
import React from 'react';
import { Route, Routes } from 'react-router-dom';
import ChallengeAnalyzer from './components/ChallengeAnalyzer';
import History from './components/History';
import Navigation from './components/Navigation';
import Stats from './components/Stats';

function App() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" sx={{ mb: 3 }}>
        <Toolbar>
          <SecurityIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            CTF智能分析平台
          </Typography>
          <Typography variant="subtitle1" sx={{ mr: 2 }}>
            Powered by DeepSeek AI
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="xl">
        <Navigation />
        <Routes>
          <Route path="/" element={<ChallengeAnalyzer />} />
          <Route path="/history" element={<History />} />
          <Route path="/stats" element={<Stats />} />
        </Routes>
      </Container>
    </Box>
  );
}

export default App; 