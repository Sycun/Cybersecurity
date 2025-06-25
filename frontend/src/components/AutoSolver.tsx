import {
    CheckCircle,
    Code,
    ContentCopy,
    Download,
    Error,
    ExpandMore,
    Flag,
    PlayArrow
} from '@mui/icons-material';
import {
    Accordion,
    AccordionDetails,
    AccordionSummary,
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Chip,
    CircularProgress,
    Divider,
    FormControl,
    IconButton,
    InputLabel,
    MenuItem,
    Select,
    TextField,
    Tooltip,
    Typography
} from '@mui/material';
import React, { useState } from 'react';
import { autoSolveChallenge, getAutoSolveResult } from '../services/api';
import { AutoSolveResponse } from '../types';

interface AutoSolverProps {
  questionId: number;
  questionDescription: string;
  questionType: string;
}

const AutoSolver: React.FC<AutoSolverProps> = ({ questionId, questionDescription, questionType }) => {
  const [loading, setLoading] = useState(false);
  const [solveMethod, setSolveMethod] = useState('ai_generated');
  const [customCode, setCustomCode] = useState('');
  const [solveResult, setSolveResult] = useState<AutoSolveResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [polling, setPolling] = useState(false);

  const solveMethods = [
    { value: 'ai_generated', label: 'AI生成代码', description: '使用AI自动生成解题代码' },
    { value: 'template', label: '使用模板', description: '使用预定义的解题模板' },
    { value: 'custom', label: '自定义代码', description: '手动编写解题代码' }
  ];

  const handleAutoSolve = async () => {
    setLoading(true);
    setError(null);
    setSolveResult(null);

    try {
      const result = await autoSolveChallenge({
        question_id: questionId,
        solve_method: solveMethod,
        custom_code: solveMethod === 'custom' ? customCode : undefined
      });

      setSolveResult(result);
      
      // 如果状态是running，开始轮询
      if (result.status === 'running') {
        setPolling(true);
        pollSolveResult(result.id);
      }
    } catch (err: any) {
      setError(err?.message || '自动解题失败');
    } finally {
      setLoading(false);
    }
  };

  const pollSolveResult = async (solveId: number) => {
    const pollInterval = setInterval(async () => {
      try {
        const result = await getAutoSolveResult(solveId);
        setSolveResult(result);
        
        if (result.status !== 'running') {
          setPolling(false);
          clearInterval(pollInterval);
        }
      } catch (err) {
        console.error('轮询失败:', err);
        setPolling(false);
        clearInterval(pollInterval);
      }
    }, 2000); // 每2秒轮询一次

    // 30秒后停止轮询
    setTimeout(() => {
      setPolling(false);
      clearInterval(pollInterval);
    }, 30000);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const downloadCode = (code: string, filename: string) => {
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'failed':
        return 'error';
      case 'running':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle />;
      case 'failed':
        return <Error />;
      case 'running':
        return <CircularProgress size={20} />;
      default:
        return null;
    }
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            🤖 自动解题
          </Typography>
          
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            使用AI自动生成并执行解题代码，尝试获取flag
          </Typography>

          {/* 解题方法选择 */}
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>解题方法</InputLabel>
            <Select
              value={solveMethod}
              onChange={(e) => setSolveMethod(e.target.value)}
              label="解题方法"
            >
              {solveMethods.map((method) => (
                <MenuItem key={method.value} value={method.value}>
                  <Box>
                    <Typography variant="body2">{method.label}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {method.description}
                    </Typography>
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* 自定义代码输入 */}
          {solveMethod === 'custom' && (
            <TextField
              fullWidth
              multiline
              rows={8}
              label="自定义解题代码"
              value={customCode}
              onChange={(e) => setCustomCode(e.target.value)}
              placeholder="请输入Python解题代码..."
              sx={{ mb: 2 }}
            />
          )}

          {/* 开始解题按钮 */}
          <Button
            variant="contained"
            startIcon={<PlayArrow />}
            onClick={handleAutoSolve}
            disabled={loading || polling}
            sx={{ mb: 2 }}
          >
            {loading ? '正在生成代码...' : polling ? '正在执行...' : '开始自动解题'}
          </Button>

          {/* 错误提示 */}
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {/* 解题结果 */}
          {solveResult && (
            <Box sx={{ mt: 3 }}>
              <Divider sx={{ mb: 2 }} />
              
              <Typography variant="h6" gutterBottom>
                解题结果
              </Typography>

              {/* 状态信息 */}
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Chip
                  icon={getStatusIcon(solveResult.status)}
                  label={solveResult.status}
                  color={getStatusColor(solveResult.status) as any}
                  sx={{ mr: 2 }}
                />
                {solveResult.execution_time && (
                  <Typography variant="body2" color="text.secondary">
                    执行时间: {solveResult.execution_time}秒
                  </Typography>
                )}
              </Box>

              {/* Flag结果 */}
              {solveResult.flag && (
                <Alert 
                  severity="success" 
                  sx={{ mb: 2 }}
                  action={
                    <Tooltip title="复制Flag">
                      <IconButton
                        size="small"
                        onClick={() => copyToClipboard(solveResult.flag!)}
                      >
                        <ContentCopy />
                      </IconButton>
                    </Tooltip>
                  }
                >
                  <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                    🎉 成功获取Flag: {solveResult.flag}
                  </Typography>
                </Alert>
              )}

              {/* 错误信息 */}
              {solveResult.error_message && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  <Typography variant="body2">
                    执行错误: {solveResult.error_message}
                  </Typography>
                </Alert>
              )}

              {/* 生成的代码 */}
              {solveResult.generated_code && (
                <Accordion sx={{ mb: 2 }}>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Code sx={{ mr: 1 }} />
                      <Typography>生成的代码</Typography>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box sx={{ position: 'relative' }}>
                      <TextField
                        fullWidth
                        multiline
                        rows={10}
                        value={solveResult.generated_code}
                        InputProps={{
                          readOnly: true,
                          style: { fontFamily: 'monospace', fontSize: '14px' }
                        }}
                        sx={{ mb: 1 }}
                      />
                      <Box sx={{ display: 'flex', gap: 1 }}>
                        <Button
                          size="small"
                          startIcon={<ContentCopy />}
                          onClick={() => copyToClipboard(solveResult.generated_code!)}
                        >
                          复制代码
                        </Button>
                        <Button
                          size="small"
                          startIcon={<Download />}
                          onClick={() => downloadCode(solveResult.generated_code!, 'solve_script.py')}
                        >
                          下载代码
                        </Button>
                      </Box>
                    </Box>
                  </AccordionDetails>
                </Accordion>
              )}

              {/* 执行结果 */}
              {solveResult.execution_result && (
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Flag sx={{ mr: 1 }} />
                      <Typography>执行输出</Typography>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <TextField
                      fullWidth
                      multiline
                      rows={8}
                      value={solveResult.execution_result}
                      InputProps={{
                        readOnly: true,
                        style: { fontFamily: 'monospace', fontSize: '14px' }
                      }}
                    />
                  </AccordionDetails>
                </Accordion>
              )}
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default AutoSolver; 