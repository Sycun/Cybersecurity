import {
    Analytics as AnalyticsIcon,
    NavigateBefore as BackIcon,
    CheckCircle as CheckIcon,
    Close as CloseIcon,
    Description as DocsIcon,
    Help as HelpIcon,
    History as HistoryIcon,
    NavigateNext as NextIcon,
    Speed as PerformanceIcon,
    PlayArrow as PlayIcon,
    Security as SecurityIcon,
    Settings as SettingsIcon,
    EmojiEvents as TrophyIcon
} from '@mui/icons-material';
import {
    Box,
    Button,
    Chip,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Fade,
    IconButton,
    LinearProgress,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Paper,
    Slide,
    Step,
    StepContent,
    StepLabel,
    Stepper,
    Typography
} from '@mui/material';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserGuide.css';

interface UserGuideProps {
  open: boolean;
  onClose: () => void;
  autoStart?: boolean;
}

interface GuideStep {
  label: string;
  title: string;
  content: React.ReactNode;
  action?: string;
  actionRoute?: string;
}

const UserGuide: React.FC<UserGuideProps> = ({ open, onClose, autoStart = false }) => {
  const [activeStep, setActiveStep] = useState(0);
  const [completed, setCompleted] = useState<Set<number>>(new Set());
  const navigate = useNavigate();

  const steps: GuideStep[] = [
    {
      label: '欢迎使用',
      title: '欢迎来到 CTF智能分析平台！ 🎉',
      content: (
        <Box className="user-guide-fade-in">
          <Typography variant="body1" paragraph>
            CTF智能分析平台是一个强大的多AI提供者CTF题目分析工具，专为CTF学习者和参赛者设计。
          </Typography>
          <div className="user-guide-feature-list">
            <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold', mb: 2 }}>
              🚀 平台特色功能：
            </Typography>
            <div className="user-guide-feature-item">
              <div className="user-guide-feature-icon">
                <SecurityIcon color="primary" />
              </div>
              <div>
                <Typography variant="body2" sx={{ fontWeight: 600 }}>
                  全题型覆盖
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  Web、Pwn、Reverse、Crypto、Misc 五大类别完整支持
                </Typography>
              </div>
            </div>
            <div className="user-guide-feature-item">
              <div className="user-guide-feature-icon">
                <AnalyticsIcon color="success" />
              </div>
              <div>
                <Typography variant="body2" sx={{ fontWeight: 600 }}>
                  多AI智能分析
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  DeepSeek、硅基流动、本地模型、OpenAI兼容API多重选择
                </Typography>
              </div>
            </div>
            <div className="user-guide-feature-item">
              <div className="user-guide-feature-icon">
                <CheckIcon color="info" />
              </div>
              <div>
                <Typography variant="body2" sx={{ fontWeight: 600 }}>
                  智能工具推荐
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  根据题目类型自动推荐合适的CTF工具和解题思路
                </Typography>
              </div>
            </div>
          </div>
        </Box>
      )
    },
    {
      label: '配置AI服务',
      title: '第一步：配置您的AI服务 ⚙️',
      content: (
        <Box className="user-guide-slide-in">
          <Typography variant="body1" paragraph>
            点击右上角的 <SettingsIcon sx={{ fontSize: 16, verticalAlign: 'middle', mx: 0.5 }} /> 
            设置图标来配置AI服务提供者。
          </Typography>
          <Paper elevation={2} sx={{ p: 2.5, mb: 2, borderRadius: 2 }}>
            <Typography variant="subtitle2" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <PlayIcon color="primary" />
              支持的AI服务：
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 1.5 }}>
              <Chip 
                label="DeepSeek" 
                color="primary" 
                size="small" 
                icon={<PlayIcon />}
                variant="outlined"
              />
              <Chip 
                label="硅基流动" 
                color="success" 
                size="small" 
                icon={<PlayIcon />}
                variant="outlined"
              />
              <Chip 
                label="本地模型" 
                color="warning" 
                size="small" 
                icon={<PlayIcon />}
                variant="outlined"
              />
              <Chip 
                label="OpenAI兼容" 
                color="secondary" 
                size="small" 
                icon={<PlayIcon />}
                variant="outlined"
              />
            </Box>
          </Paper>
          <div className="user-guide-tip-box">
            <Typography variant="body2">
              <strong>建议：</strong>首次使用时推荐配置DeepSeek或硅基流动API，它们提供稳定可靠的分析服务，
              只需填入API密钥即可开始使用。
            </Typography>
          </div>
        </Box>
      ),
      action: '立即配置',
      actionRoute: 'settings'
    },
    {
      label: '分析题目',
      title: '第二步：开始分析CTF题目 🎯',
      content: (
        <Box className="user-guide-fade-in">
          <Typography variant="body1" paragraph>
            在主页面，您可以通过两种方式提交题目进行分析：
          </Typography>
          <List sx={{ bgcolor: 'background.paper', borderRadius: 2, mt: 2 }}>
            <ListItem sx={{ border: '1px solid', borderColor: 'divider', borderRadius: 1, mb: 1 }}>
              <ListItemIcon>
                <Box sx={{ fontSize: '1.5rem' }}>📝</Box>
              </ListItemIcon>
              <ListItemText 
                primary={
                  <Typography variant="body1" sx={{ fontWeight: 600 }}>
                    输入文本描述
                  </Typography>
                }
                secondary="直接在文本框中输入题目描述、提示信息或源代码，支持中英文混合输入"
              />
            </ListItem>
            <ListItem sx={{ border: '1px solid', borderColor: 'divider', borderRadius: 1 }}>
              <ListItemIcon>
                <Box sx={{ fontSize: '1.5rem' }}>📁</Box>
              </ListItemIcon>
              <ListItemText 
                primary={
                  <Typography variant="body1" sx={{ fontWeight: 600 }}>
                    上传题目文件
                  </Typography>
                }
                secondary="支持各种格式：源码文件(.c, .py, .js)、二进制文件、图片、压缩包等"
              />
            </ListItem>
          </List>
          <div className="user-guide-tip-box">
            <Typography variant="body2">
              <strong>智能识别：</strong>系统会自动分析内容特征，识别题目类型并调用相应的AI模型进行深度分析。
              描述越详细，分析结果越精准！
            </Typography>
          </div>
        </Box>
      ),
      action: '开始分析',
      actionRoute: '/'
    },
    {
      label: '查看结果',
      title: '第三步：获取分析结果和工具推荐 💡',
      content: (
        <Box className="user-guide-slide-in">
          <Typography variant="body1" paragraph>
            AI分析完成后，您将获得全面的解题指导：
          </Typography>
          <List sx={{ bgcolor: 'background.paper', borderRadius: 2 }}>
            <ListItem>
              <ListItemIcon>
                <Box sx={{ fontSize: '1.5rem' }}>🎯</Box>
              </ListItemIcon>
              <ListItemText 
                primary={<Typography sx={{ fontWeight: 600 }}>智能题型识别</Typography>}
                secondary="自动识别为Web、Pwn、Reverse、Crypto或Misc类型，准确率95%+"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <Box sx={{ fontSize: '1.5rem' }}>💡</Box>
              </ListItemIcon>
              <ListItemText 
                primary={<Typography sx={{ fontWeight: 600 }}>详细解题思路</Typography>}
                secondary="提供完整的分析过程、攻击向量、关键步骤和注意事项"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <Box sx={{ fontSize: '1.5rem' }}>🛠️</Box>
              </ListItemIcon>
              <ListItemText 
                primary={<Typography sx={{ fontWeight: 600 }}>专业工具推荐</Typography>}
                secondary="推荐最适合的CTF工具，提供具体的命令行用法和参数说明"
              />
            </ListItem>
          </List>
        </Box>
      )
    },
    {
      label: '管理记录',
      title: '第四步：管理您的学习历程 📊',
      content: (
        <Box className="user-guide-fade-in">
          <Typography variant="body1" paragraph>
            使用导航栏探索更多功能，让学习更有条理：
          </Typography>
          <div className="user-guide-navigation-demo">
            <div className="user-guide-nav-item">
              <HistoryIcon fontSize="small" />
              历史记录
            </div>
            <div className="user-guide-nav-item">
              <AnalyticsIcon fontSize="small" />
              统计信息
            </div>
            <div className="user-guide-nav-item">
              <PerformanceIcon fontSize="small" />
              性能监控
            </div>
            <div className="user-guide-nav-item">
              <DocsIcon fontSize="small" />
              文档中心
            </div>
          </div>
          <List sx={{ mt: 2 }}>
            <ListItem>
              <ListItemIcon><HistoryIcon color="primary" /></ListItemIcon>
              <ListItemText 
                primary="历史记录" 
                secondary="查看所有分析记录，支持搜索和分类浏览"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon><AnalyticsIcon color="success" /></ListItemIcon>
              <ListItemText 
                primary="统计信息" 
                secondary="了解你的学习进度和题目类型分布"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon><PerformanceIcon color="warning" /></ListItemIcon>
              <ListItemText 
                primary="性能监控" 
                secondary="实时监控AI服务状态和平台性能"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon><DocsIcon color="info" /></ListItemIcon>
              <ListItemText 
                primary="文档中心" 
                secondary="查看详细使用指南、API文档和最佳实践"
              />
            </ListItem>
          </List>
        </Box>
      ),
      action: '查看记录',
      actionRoute: '/history'
    },
    {
      label: '完成',
      title: '🎉 恭喜！您已经掌握了所有基本功能',
      content: (
        <Box className="user-guide-fade-in">
          <div className="user-guide-completion-box">
            <TrophyIcon sx={{ fontSize: 48, color: '#ffd700', mb: 2 }} />
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
              欢迎加入CTF学习之旅！
            </Typography>
            <Typography variant="body1" paragraph>
              您现在已经准备好使用CTF智能分析平台了！
            </Typography>
          </div>
          
          <Paper elevation={1} sx={{ p: 2.5, mt: 2, backgroundColor: 'primary.light', color: 'primary.contrastText' }}>
            <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ fontSize: '1.2rem' }}>💡</Box>
              专家小贴士
            </Typography>
            <Typography variant="body2" component="div">
              • <strong>详细描述</strong>：提供越详细的题目信息，AI分析结果越准确<br/>
              • <strong>多种尝试</strong>：可以尝试不同的AI提供者，获得多角度的分析视角<br/>
              • <strong>组合使用</strong>：支持同时输入文本描述和上传文件<br/>
              • <strong>历史回顾</strong>：所有分析记录都会自动保存，方便后续学习回顾
            </Typography>
          </Paper>
          
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2, textAlign: 'center' }}>
            如需再次查看教程，可随时点击右上角的 <HelpIcon sx={{ fontSize: 16, verticalAlign: 'middle' }} /> 帮助按钮
          </Typography>
        </Box>
      )
    }
  ];

  const handleNext = () => {
    const newCompleted = new Set(completed);
    newCompleted.add(activeStep);
    setCompleted(newCompleted);
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleStep = (step: number) => () => {
    setActiveStep(step);
  };

  const handleComplete = () => {
    // 标记用户已完成引导
    localStorage.setItem('ctf_guide_completed', 'true');
    localStorage.setItem('ctf_guide_completed_time', new Date().toISOString());
    onClose();
  };

  const handleSkip = () => {
    localStorage.setItem('ctf_guide_skipped', 'true');
    onClose();
  };

  const handleAction = (step: GuideStep) => {
    if (step.actionRoute) {
      if (step.actionRoute === 'settings') {
        // 这里可以触发设置对话框打开
        console.log('打开设置');
      } else {
        navigate(step.actionRoute);
        onClose();
      }
    }
  };

  const isStepCompleted = (step: number) => {
    return completed.has(step);
  };

  const totalSteps = () => {
    return steps.length;
  };

  const completedSteps = () => {
    return completed.size;
  };

  const isLastStep = () => {
    return activeStep === totalSteps() - 1;
  };

  const allStepsCompleted = () => {
    return completedSteps() === totalSteps();
  };

  const getProgress = () => {
    return ((activeStep + 1) / totalSteps()) * 100;
  };

  return (
    <Dialog 
      open={open} 
      onClose={onClose} 
      maxWidth="md" 
      fullWidth
      className="user-guide-dialog"
      TransitionComponent={Fade}
      transitionDuration={300}
    >
      <DialogTitle className="user-guide-header">
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <HelpIcon sx={{ mr: 1 }} />
            CTF智能分析平台 - 使用指南
          </Box>
          <IconButton onClick={onClose} size="small" sx={{ color: 'white' }}>
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>
      
      <DialogContent className="user-guide-content">
        <div className="user-guide-step-indicator">
          <Typography variant="body2" color="text.secondary">
            第 {activeStep + 1} 步，共 {totalSteps()} 步
          </Typography>
          <Box sx={{ width: '200px' }}>
            <LinearProgress 
              variant="determinate" 
              value={getProgress()} 
              sx={{ height: 6, borderRadius: 3 }}
            />
          </Box>
        </div>

        <Stepper activeStep={activeStep} orientation="vertical" className="user-guide-stepper">
          {steps.map((step, index) => (
            <Step key={step.label} completed={isStepCompleted(index)}>
              <StepLabel
                onClick={handleStep(index)}
                sx={{ 
                  cursor: 'pointer',
                  '&:hover': { backgroundColor: 'action.hover', borderRadius: 1, px: 1 }
                }}
              >
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                  {step.label}
                </Typography>
              </StepLabel>
              <StepContent>
                <Slide direction="right" in={true} mountOnEnter unmountOnExit>
                  <Box>
                    <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                      {step.title}
                    </Typography>
                    <Box className="user-guide-step-content">
                      {step.content}
                    </Box>
                    <div className="user-guide-action-buttons">
                      <Button
                        variant="contained"
                        onClick={isLastStep() ? handleComplete : handleNext}
                        startIcon={isLastStep() ? <TrophyIcon /> : <NextIcon />}
                        size="large"
                      >
                        {isLastStep() ? '开始使用平台' : '下一步'}
                      </Button>
                      {activeStep > 0 && (
                        <Button
                          onClick={handleBack}
                          startIcon={<BackIcon />}
                          size="large"
                        >
                          上一步
                        </Button>
                      )}
                      {step.action && !isLastStep() && (
                        <Button
                          variant="outlined"
                          onClick={() => handleAction(step)}
                          size="large"
                        >
                          {step.action}
                        </Button>
                      )}
                    </div>
                  </Box>
                </Slide>
              </StepContent>
            </Step>
          ))}
        </Stepper>

        {allStepsCompleted() && (
          <Fade in={true}>
            <Paper elevation={3} sx={{ p: 3, mt: 3, textAlign: 'center', backgroundColor: 'success.light' }}>
              <TrophyIcon sx={{ fontSize: 48, color: 'success.main', mb: 1 }} />
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
                🎉 教程完成！
              </Typography>
              <Typography variant="body1">
                您已经完成了所有引导步骤，现在可以开始您的CTF学习之旅了！
              </Typography>
            </Paper>
          </Fade>
        )}
      </DialogContent>

      <DialogActions sx={{ p: 3, justifyContent: 'space-between' }}>
        <Button onClick={handleSkip} color="inherit" size="large">
          跳过教程
        </Button>
        <Button onClick={onClose} variant="outlined" size="large">
          关闭
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default UserGuide; 