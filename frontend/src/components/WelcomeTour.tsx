import {
    Close as CloseIcon,
    Help as HelpIcon,
    Lightbulb as TipIcon
} from '@mui/icons-material';
import {
    Alert,
    AlertTitle,
    Box,
    Button,
    Fab,
    Snackbar,
    Tooltip,
    Typography,
    Zoom
} from '@mui/material';
import React, { useEffect, useState } from 'react';

interface WelcomeTourProps {
  onOpenGuide: () => void;
}

const WelcomeTour: React.FC<WelcomeTourProps> = ({ onOpenGuide }) => {
  const [showWelcome, setShowWelcome] = useState(false);
  const [showTip, setShowTip] = useState(false);
  const [showFloatingButton, setShowFloatingButton] = useState(false);

  useEffect(() => {
    const hasSeenWelcome = localStorage.getItem('ctf_welcome_seen');
    const hasCompletedGuide = localStorage.getItem('ctf_guide_completed');
    const hasSkippedGuide = localStorage.getItem('ctf_guide_skipped');

    // 如果用户从未看过欢迎提示且没有完成引导，显示欢迎消息
    if (!hasSeenWelcome && !hasCompletedGuide && !hasSkippedGuide) {
      const timer = setTimeout(() => {
        setShowWelcome(true);
      }, 2000); // 2秒后显示欢迎消息

      return () => clearTimeout(timer);
    }

    // 如果用户已经使用过但没有完成完整引导，显示提示
    if (hasSeenWelcome && !hasCompletedGuide && !hasSkippedGuide) {
      const tipTimer = setTimeout(() => {
        setShowTip(true);
      }, 5000); // 5秒后显示提示

      // 显示浮动帮助按钮
      setShowFloatingButton(true);

      return () => clearTimeout(tipTimer);
    }

    // 如果用户已完成引导，仍然显示浮动按钮但不那么明显
    if (hasCompletedGuide || hasSkippedGuide) {
      const buttonTimer = setTimeout(() => {
        setShowFloatingButton(true);
      }, 10000); // 10秒后显示，不那么突兀

      return () => clearTimeout(buttonTimer);
    }
  }, []);

  const handleWelcomeClose = () => {
    setShowWelcome(false);
    localStorage.setItem('ctf_welcome_seen', 'true');
    // 延迟显示浮动按钮
    setTimeout(() => {
      setShowFloatingButton(true);
    }, 3000);
  };

  const handleStartGuide = () => {
    setShowWelcome(false);
    localStorage.setItem('ctf_welcome_seen', 'true');
    localStorage.setItem('ctf_auto_start_guide', 'true');
    onOpenGuide();
  };

  const handleTipClose = () => {
    setShowTip(false);
  };

  const hasCompletedGuide = localStorage.getItem('ctf_guide_completed');
  const isFirstTime = !localStorage.getItem('ctf_welcome_seen') && !hasCompletedGuide;

  return (
    <>
      {/* 首次访问欢迎消息 */}
      <Snackbar
        open={showWelcome}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        sx={{ mt: 8 }}
      >
        <Alert
          severity="info"
          variant="filled"
          sx={{ 
            minWidth: { xs: 300, sm: 450 },
            borderRadius: 2,
            boxShadow: 3
          }}
          action={
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              <Button 
                size="small" 
                color="inherit" 
                variant="outlined"
                onClick={handleStartGuide}
                sx={{ 
                  borderColor: 'white', 
                  color: 'white',
                  '&:hover': { 
                    backgroundColor: 'rgba(255,255,255,0.1)',
                    borderColor: 'white'
                  }
                }}
              >
                开始教程
              </Button>
              <Button 
                size="small" 
                color="inherit"
                onClick={handleWelcomeClose}
                sx={{ 
                  color: 'white',
                  minWidth: 'auto',
                  '&:hover': { 
                    backgroundColor: 'rgba(255,255,255,0.1)'
                  }
                }}
              >
                <CloseIcon fontSize="small" />
              </Button>
            </Box>
          }
        >
          <AlertTitle sx={{ fontWeight: 'bold' }}>
            🎉 欢迎来到CTF智能分析平台！
          </AlertTitle>
          <Typography variant="body2">
            这是您第一次使用我们的平台。我们为您准备了详细的使用指南，帮助您快速上手所有功能。
          </Typography>
        </Alert>
      </Snackbar>

      {/* 帮助提示 */}
      <Snackbar
        open={showTip}
        onClose={handleTipClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
        autoHideDuration={8000}
      >
        <Alert
          severity="success"
          variant="standard"
          onClose={handleTipClose}
          sx={{ 
            borderRadius: 2,
            boxShadow: 2
          }}
          icon={<TipIcon />}
        >
          <AlertTitle>💡 小提示</AlertTitle>
          点击右上角的 <HelpIcon sx={{ fontSize: 16, verticalAlign: 'middle', mx: 0.5 }} /> 
          帮助按钮或右下角的悬浮按钮可以随时查看完整使用指南
        </Alert>
      </Snackbar>

      {/* 浮动帮助按钮 */}
      <Zoom in={showFloatingButton && !showWelcome}>
        <Tooltip title="查看使用指南" placement="left">
          <Fab
            color="primary"
            onClick={onOpenGuide}
            size={isFirstTime ? "large" : "medium"}
            sx={{
              position: 'fixed',
              bottom: 24,
              right: 24,
              zIndex: 1000,
              ...(isFirstTime && {
                animation: 'pulse 2s infinite',
                '@keyframes pulse': {
                  '0%': {
                    transform: 'scale(1)',
                    boxShadow: '0 0 0 0 rgba(25, 118, 210, 0.7)'
                  },
                  '70%': {
                    transform: 'scale(1.05)',
                    boxShadow: '0 0 0 10px rgba(25, 118, 210, 0)'
                  },
                  '100%': {
                    transform: 'scale(1)',
                    boxShadow: '0 0 0 0 rgba(25, 118, 210, 0)'
                  }
                }
              }),
              '&:hover': {
                transform: 'scale(1.1)',
                transition: 'transform 0.2s ease-in-out'
              }
            }}
          >
            <HelpIcon />
          </Fab>
        </Tooltip>
      </Zoom>
    </>
  );
};

export default WelcomeTour; 