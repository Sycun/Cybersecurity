import {
    AutoFixHigh as AutoIcon,
    CheckCircle as CheckIcon,
    Error as ErrorIcon,
    ExpandMore,
    Refresh as RefreshIcon,
    Save as SaveIcon,
    Science as TestIcon,
    Visibility,
    VisibilityOff,
    Warning as WarningIcon
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
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Divider,
    IconButton,
    InputAdornment,
    LinearProgress,
    Snackbar,
    TextField,
    Tooltip,
    Typography
} from '@mui/material';
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { AIConfig, getAIProviders, getAIProviderStatus, getSettings, switchAIProvider, testConnection, updateSettings, validateSettings } from '../services/api';
import './Settings.css';

interface SettingsProps {
  open: boolean;
  onClose: () => void;
}

interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

interface TestResult {
  success: boolean;
  message: string;
  provider: string;
  response_preview?: string;
  error_details?: string;
}

interface AIProvider {
  name: string;
  description: string;
  type: 'cloud' | 'local' | 'local_cloud';
  languages: string[];
  max_tokens: number;
  features: string[];
}

interface AIProvidersData {
  current_provider: string;
  current_provider_info: AIProvider;
  available_providers: Record<string, AIProvider>;
}

const Settings: React.FC<SettingsProps> = ({ open, onClose }) => {
  const [config, setConfig] = useState<AIConfig>({} as AIConfig);
  const [originalConfig, setOriginalConfig] = useState<AIConfig>({} as AIConfig);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [testing, setTesting] = useState(false);
  const [showPassword, setShowPassword] = useState<Record<string, boolean>>({});
  const [message, setMessage] = useState<{ type: 'success' | 'error' | 'warning'; text: string } | null>(null);
  const [validation, setValidation] = useState<ValidationResult | null>(null);
  const [testResult, setTestResult] = useState<TestResult | null>(null);
  const [autoSave, setAutoSave] = useState(true);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  
  // AI Provider相关状态
  const [aiProviders, setAIProviders] = useState<AIProvidersData | null>(null);
  const [aiProviderStatus, setAIProviderStatus] = useState<any>(null);
  const [switchingProvider, setSwitchingProvider] = useState(false);
  const [loadingProviders, setLoadingProviders] = useState(false);

  // 检查是否有未保存的更改
  const checkUnsavedChanges = useCallback(() => {
    const hasChanges = JSON.stringify(config) !== JSON.stringify(originalConfig);
    setHasUnsavedChanges(hasChanges);
    return hasChanges;
  }, [config, originalConfig]);

  // 实时验证配置
  const validateConfig = useCallback(async (configToValidate: AIConfig) => {
    try {
      const result = await validateSettings(configToValidate);
      setValidation(result);
      return result;
    } catch (error) {
      setValidation({
        valid: false,
        errors: [`验证失败: ${error}`],
        warnings: []
      });
      return null;
    }
  }, []);

  // 加载配置
  const loadSettings = async () => {
    try {
      setLoading(true);
      const data = await getSettings();
      setConfig(data);
      setOriginalConfig(data);
      setHasUnsavedChanges(false);
      // 加载后自动验证
      await validateConfig(data);
    } catch (error) {
      setMessage({ type: 'error', text: `加载配置失败: ${error}` });
    } finally {
      setLoading(false);
    }
  };

  // 加载AI Provider信息
  const loadAIProviders = async () => {
    try {
      setLoadingProviders(true);
      const providersData = await getAIProviders();
      setAIProviders(providersData);
      
      // 加载Provider状态
      try {
        const statusData = await getAIProviderStatus();
        setAIProviderStatus(statusData);
      } catch (error) {
        console.warn('获取AI Provider状态失败:', error);
      }
    } catch (error) {
      setMessage({ type: 'error', text: `加载AI提供者失败: ${error}` });
    } finally {
      setLoadingProviders(false);
    }
  };

  // 切换AI Provider
  const handleSwitchProvider = async (providerType: string) => {
    try {
      setSwitchingProvider(true);
      const result = await switchAIProvider(providerType);
      setMessage({ type: 'success', text: result.message });
      
      // 重新加载Provider信息
      await loadAIProviders();
    } catch (error) {
      setMessage({ type: 'error', text: `切换AI提供者失败: ${error}` });
    } finally {
      setSwitchingProvider(false);
    }
  };

  // 初始化
  useEffect(() => {
    if (open) {
      loadSettings();
      loadAIProviders();
    }
  }, [open]);

  // 监听配置变化
  useEffect(() => {
    checkUnsavedChanges();
    
    // 延迟验证，避免频繁调用
    const timer = setTimeout(() => {
      if (config.provider) {
        validateConfig(config);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [config, checkUnsavedChanges, validateConfig]);

  // 处理输入变化
  const handleInputChange = (field: keyof AIConfig, value: string | number) => {
    setConfig(prev => ({ ...prev, [field]: value }));
    
    // 清除之前的测试结果
    if (testResult) {
      setTestResult(null);
    }
  };

  // 切换密码显示
  const togglePasswordVisibility = (field: string) => {
    setShowPassword(prev => ({ ...prev, [field]: !prev[field] }));
  };

  // 保存配置
  const handleSave = async () => {
    try {
      setSaving(true);
      
      // 先验证
      const validationResult = await validateConfig(config);
      if (!validationResult?.valid) {
        setMessage({ 
          type: 'error', 
          text: `配置验证失败: ${validationResult?.errors.join(', ') || '未知错误'}` 
        });
        return;
      }

      const result = await updateSettings(config);
      setOriginalConfig(config);
      setHasUnsavedChanges(false);
      
      setMessage({ 
        type: 'success', 
        text: result.message || '配置保存成功！设置已自动应用到系统中。' 
      });
      
      // 保存成功后清除测试结果，提示用户重新测试
      setTestResult(null);
      
    } catch (error) {
      setMessage({ type: 'error', text: `保存失败: ${error}` });
    } finally {
      setSaving(false);
    }
  };

  // 测试连接
  const handleTestConnection = async () => {
    try {
      setTesting(true);
      setTestResult(null);
      
      // 使用当前配置进行测试，即使未保存
      const result = await testConnection(config.provider, config);
      setTestResult(result);
      
      if (result.success) {
        setMessage({ type: 'success', text: result.message });
      } else {
        setMessage({ type: 'error', text: result.message });
      }
      
    } catch (error) {
      const errorResult: TestResult = {
        success: false,
        message: `连接测试失败: ${error}`,
        provider: config.provider || 'unknown',
        error_details: String(error)
      };
      setTestResult(errorResult);
      setMessage({ type: 'error', text: errorResult.message });
    } finally {
      setTesting(false);
    }
  };

  // 自动填充默认配置
  const handleAutoFill = () => {
    const defaults: Partial<AIConfig> = {
      deepseek_api_url: 'https://api.deepseek.com/v1/chat/completions',
      deepseek_model: 'deepseek-chat',
      siliconflow_api_url: 'https://api.siliconflow.cn/v1/chat/completions',
      siliconflow_model: 'Qwen/QwQ-32B',
      openai_compatible_model: 'gpt-3.5-turbo',
      local_model_type: 'auto',
      local_model_device: 'auto',
      local_model_max_length: 4096,
      local_model_temperature: 0.7
    };

    setConfig(prev => ({ ...prev, ...defaults }));
    setMessage({ type: 'success', text: '已自动填充默认配置，请检查并修改为你的设置' });
  };

  // 渲染密码输入框
  const renderPasswordField = (
    label: string,
    field: keyof AIConfig,
    value?: string,
    required?: boolean,
    helperText?: string
  ) => (
    <TextField
      fullWidth
      margin="normal"
      label={label}
      type={showPassword[String(field)] ? 'text' : 'password'}
      value={value || ''}
      onChange={(e) => handleInputChange(field, e.target.value)}
      required={required}
      helperText={helperText}
      error={validation && validation.errors.some(error => 
        error.toLowerCase().includes(field.toLowerCase().replace('_', ' '))
      )}
      InputProps={{
        endAdornment: (
          <InputAdornment position="end">
            <IconButton
              onClick={() => togglePasswordVisibility(String(field))}
              edge="end"
            >
              {showPassword[String(field)] ? <VisibilityOff /> : <Visibility />}
            </IconButton>
          </InputAdornment>
        )
      }}
    />
  );

  // 获取当前配置的状态指示器
  const getStatusIndicator = useMemo(() => {
    if (validation?.valid && testResult?.success) {
      return <Chip icon={<CheckIcon />} label="配置正常" color="success" size="small" />;
    } else if (validation?.errors.length) {
      return <Chip icon={<ErrorIcon />} label="配置错误" color="error" size="small" />;
    } else if (validation?.warnings.length) {
      return <Chip icon={<WarningIcon />} label="配置警告" color="warning" size="small" />;
    } else if (hasUnsavedChanges) {
      return <Chip label="未保存" color="default" size="small" />;
    }
    return null;
  }, [validation, testResult, hasUnsavedChanges]);

  return (
    <>
      <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth className="settings-dialog">
        <DialogTitle>
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Box display="flex" alignItems="center" gap={2}>
              <Typography variant="h6">AI服务配置</Typography>
              {getStatusIndicator}
            </Box>
            <Box display="flex" alignItems="center" gap={1}>
              <Tooltip title="自动填充默认配置">
                <IconButton onClick={handleAutoFill} disabled={loading}>
                  <AutoIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="刷新配置">
                <IconButton onClick={loadSettings} disabled={loading}>
                  <RefreshIcon />
                </IconButton>
              </Tooltip>
            </Box>
          </Box>
          {hasUnsavedChanges && <LinearProgress sx={{ mt: 1 }} />}
        </DialogTitle>
        
        <DialogContent>
          {loading ? (
            <Box className="settings-loading">
              <CircularProgress />
              <Typography>加载配置中...</Typography>
            </Box>
          ) : (
            <Box>
              {/* 验证结果显示 */}
              {validation && (validation.errors.length > 0 || validation.warnings.length > 0) && (
                <Box sx={{ mb: 2 }}>
                  {validation.errors.map((error, index) => (
                    <Alert key={`error-${index}`} severity="error" sx={{ mb: 1 }}>
                      {error}
                    </Alert>
                  ))}
                  {validation.warnings.map((warning, index) => (
                    <Alert key={`warning-${index}`} severity="warning" sx={{ mb: 1 }}>
                      {warning}
                    </Alert>
                  ))}
                </Box>
              )}

              {/* 测试结果显示 */}
              {testResult && (
                <Alert 
                  severity={testResult.success ? "success" : "error"} 
                  sx={{ mb: 2 }}
                  action={
                    testResult.success && hasUnsavedChanges ? (
                      <Button 
                        color="inherit" 
                        size="small" 
                        onClick={handleSave}
                        disabled={saving}
                      >
                        保存配置
                      </Button>
                    ) : null
                  }
                >
                  <Typography variant="body2">{testResult.message}</Typography>
                  {testResult.response_preview && (
                    <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                      响应预览: {testResult.response_preview}
                    </Typography>
                  )}
                </Alert>
              )}

              {/* AI Provider选择 */}
              <Accordion defaultExpanded className="settings-accordion">
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <AutoIcon />
                    <Typography variant="subtitle1">AI模型选择</Typography>
                    {aiProviders && (
                      <Chip 
                        label={aiProviders.current_provider_info?.name || aiProviders.current_provider}
                        size="small"
                        color="primary"
                        variant="outlined"
                      />
                    )}
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  {loadingProviders ? (
                    <Box display="flex" justifyContent="center" p={2}>
                      <CircularProgress size={24} />
                    </Box>
                  ) : aiProviders ? (
                    <Box>
                      {/* 当前Provider状态 */}
                      <Card variant="outlined" sx={{ mb: 2 }}>
                        <CardContent>
                          <Typography variant="h6" gutterBottom>
                            当前AI模型: {aiProviders.current_provider_info?.name}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" gutterBottom>
                            {aiProviders.current_provider_info?.description}
                          </Typography>
                          <Box display="flex" gap={1} flexWrap="wrap" mt={1}>
                            <Chip 
                              label={aiProviders.current_provider_info?.type === 'cloud' ? '云端' : 
                                    aiProviders.current_provider_info?.type === 'local' ? '本地' : '混合'} 
                              size="small" 
                              color="secondary"
                            />
                            <Chip 
                              label={`最大${aiProviders.current_provider_info?.max_tokens} tokens`} 
                              size="small" 
                              variant="outlined"
                            />
                            {aiProviders.current_provider_info?.features?.map((feature, index) => (
                              <Chip 
                                key={index}
                                label={feature === 'analysis' ? '分析' : 
                                      feature === 'code_generation' ? '代码生成' : feature} 
                                size="small" 
                                variant="outlined"
                              />
                            ))}
                          </Box>
                        </CardContent>
                      </Card>

                      {/* 可用Provider列表 */}
                      <Typography variant="subtitle2" gutterBottom>
                        可用的AI模型:
                      </Typography>
                      <Box display="flex" flexDirection="column" gap={1}>
                        {Object.entries(aiProviders.available_providers).map(([key, provider]) => (
                          <Card 
                            key={key} 
                            variant="outlined"
                            sx={{ 
                              cursor: 'pointer',
                              borderColor: key === aiProviders.current_provider ? 'primary.main' : 'divider',
                              '&:hover': { borderColor: 'primary.main' }
                            }}
                            onClick={() => handleSwitchProvider(key)}
                          >
                            <CardContent sx={{ py: 1.5 }}>
                              <Box display="flex" justifyContent="space-between" alignItems="center">
                                <Box>
                                  <Typography variant="subtitle2">
                                    {provider.name}
                                    {key === aiProviders.current_provider && (
                                      <Chip 
                                        label="当前" 
                                        size="small" 
                                        color="primary" 
                                        sx={{ ml: 1 }}
                                      />
                                    )}
                                  </Typography>
                                  <Typography variant="body2" color="text.secondary">
                                    {provider.description}
                                  </Typography>
                                  <Box display="flex" gap={0.5} mt={0.5}>
                                    <Chip 
                                      label={provider.type === 'cloud' ? '云端' : 
                                            provider.type === 'local' ? '本地' : '混合'} 
                                      size="small" 
                                      variant="outlined"
                                    />
                                    <Chip 
                                      label={`${provider.max_tokens} tokens`} 
                                      size="small" 
                                      variant="outlined"
                                    />
                                  </Box>
                                </Box>
                                <Box display="flex" alignItems="center" gap={1}>
                                  {switchingProvider && key === aiProviders.current_provider ? (
                                    <CircularProgress size={16} />
                                  ) : (
                                    <Button
                                      variant={key === aiProviders.current_provider ? "outlined" : "contained"}
                                      size="small"
                                      disabled={key === aiProviders.current_provider || switchingProvider}
                                    >
                                      {key === aiProviders.current_provider ? "当前使用" : "切换"}
                                    </Button>
                                  )}
                                </Box>
                              </Box>
                            </CardContent>
                          </Card>
                        ))}
                      </Box>

                      {/* Provider状态信息 */}
                      {aiProviderStatus && (
                        <Box mt={2}>
                          <Typography variant="subtitle2" gutterBottom>
                            性能统计:
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            请求次数: {aiProviderStatus.performance_stats?.provider_stats?.request_count || 0} | 
                            平均响应时间: {(aiProviderStatus.performance_stats?.provider_stats?.average_response_time || 0).toFixed(2)}s | 
                            缓存文件: {aiProviderStatus.performance_stats?.cache_files || 0}
                          </Typography>
                        </Box>
                      )}
                    </Box>
                  ) : (
                    <Typography color="error">
                      加载AI提供者信息失败
                    </Typography>
                  )}
                </AccordionDetails>
              </Accordion>

              <Divider sx={{ my: 2 }} />

              {/* DeepSeek配置 */}
              {config.provider === 'deepseek' && (
                <Accordion defaultExpanded className="settings-accordion">
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Box display="flex" alignItems="center" gap={1}>
                      <Typography variant="subtitle1">🤖 DeepSeek 配置</Typography>
                      <Typography variant="caption" color="text.secondary">
                        - 高质量推理，支持中英文
                      </Typography>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box className="settings-section">
                      {renderPasswordField(
                        'API Key', 
                        'deepseek_api_key', 
                        config.deepseek_api_key, 
                        true,
                        '请在DeepSeek官网获取API密钥'
                      )}
                      <TextField
                        fullWidth
                        margin="normal"
                        label="API URL"
                        value={config.deepseek_api_url || 'https://api.deepseek.com/v1/chat/completions'}
                        onChange={(e) => handleInputChange('deepseek_api_url', e.target.value)}
                        className="settings-field"
                        helperText="通常使用默认URL即可"
                      />
                      <TextField
                        fullWidth
                        margin="normal"
                        label="模型名称"
                        value={config.deepseek_model || 'deepseek-chat'}
                        onChange={(e) => handleInputChange('deepseek_model', e.target.value)}
                        className="settings-field"
                        helperText="建议使用 deepseek-chat 模型"
                      />
                    </Box>
                  </AccordionDetails>
                </Accordion>
              )}

              {/* 硅基流动配置 */}
              {config.provider === 'siliconflow' && (
                <Accordion defaultExpanded className="settings-accordion">
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Box display="flex" alignItems="center" gap={1}>
                      <Typography variant="subtitle1">🧠 硅基流动 配置</Typography>
                      <Typography variant="caption" color="text.secondary">
                        - 多模型支持，性价比高
                      </Typography>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box className="settings-section">
                      {renderPasswordField(
                        'API Key', 
                        'siliconflow_api_key', 
                        config.siliconflow_api_key, 
                        true,
                        '请在硅基流动官网获取API密钥'
                      )}
                      <TextField
                        fullWidth
                        margin="normal"
                        label="API URL"
                        value={config.siliconflow_api_url || 'https://api.siliconflow.cn/v1/chat/completions'}
                        onChange={(e) => handleInputChange('siliconflow_api_url', e.target.value)}
                        className="settings-field"
                        helperText="通常使用默认URL即可"
                      />
                      <TextField
                        fullWidth
                        margin="normal"
                        label="模型名称"
                        value={config.siliconflow_model || 'Qwen/QwQ-32B'}
                        onChange={(e) => handleInputChange('siliconflow_model', e.target.value)}
                        className="settings-field"
                        helperText="推荐使用 Qwen/QwQ-32B 模型"
                      />
                    </Box>
                  </AccordionDetails>
                </Accordion>
              )}

              {/* OpenAI兼容API配置 */}
              {config.provider === 'openai_compatible' && (
                <Accordion defaultExpanded className="settings-accordion">
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Box display="flex" alignItems="center" gap={1}>
                      <Typography variant="subtitle1">🔗 OpenAI兼容API 配置</Typography>
                      <Typography variant="caption" color="text.secondary">
                        - 支持各种OpenAI兼容服务
                      </Typography>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box className="settings-section">
                      <TextField
                        fullWidth
                        margin="normal"
                        label="API URL"
                        value={config.openai_compatible_api_url || ''}
                        onChange={(e) => handleInputChange('openai_compatible_api_url', e.target.value)}
                        required
                        className="settings-field"
                        helperText="例如: http://localhost:11434/v1/chat/completions (Ollama)"
                        error={validation && validation.errors.some(error => 
                          error.toLowerCase().includes('url')
                        )}
                      />
                      {renderPasswordField(
                        'API Key', 
                        'openai_compatible_api_key', 
                        config.openai_compatible_api_key,
                        false,
                        '如果服务不需要认证，可以留空'
                      )}
                      <TextField
                        fullWidth
                        margin="normal"
                        label="模型名称"
                        value={config.openai_compatible_model || 'gpt-3.5-turbo'}
                        onChange={(e) => handleInputChange('openai_compatible_model', e.target.value)}
                        className="settings-field"
                        helperText="根据你的服务提供的模型名称填写"
                      />
                    </Box>
                  </AccordionDetails>
                </Accordion>
              )}

              {/* 本地模型配置 */}
              {config.provider === 'local' && (
                <Accordion defaultExpanded className="settings-accordion">
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Box display="flex" alignItems="center" gap={1}>
                      <Typography variant="subtitle1">💻 本地模型 配置</Typography>
                      <Typography variant="caption" color="text.secondary">
                        - 离线使用，数据私密
                      </Typography>
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box className="settings-section">
                      <TextField
                        fullWidth
                        margin="normal"
                        label="模型路径"
                        value={config.local_model_path || ''}
                        onChange={(e) => handleInputChange('local_model_path', e.target.value)}
                        required
                        className="settings-field"
                        helperText="本地模型文件或目录路径"
                      />
                      <Box className="settings-field-group">
                        <TextField
                          margin="normal"
                          label="模型类型"
                          value={config.local_model_type || 'auto'}
                          onChange={(e) => handleInputChange('local_model_type', e.target.value)}
                          className="settings-field"
                          helperText="通常使用 auto 自动检测"
                        />
                        <TextField
                          margin="normal"
                          label="运行设备"
                          value={config.local_model_device || 'auto'}
                          onChange={(e) => handleInputChange('local_model_device', e.target.value)}
                          className="settings-field"
                          helperText="auto/cpu/cuda"
                        />
                      </Box>
                      <Box className="settings-field-group">
                        <TextField
                          margin="normal"
                          label="最大长度"
                          type="number"
                          value={config.local_model_max_length || 4096}
                          onChange={(e) => handleInputChange('local_model_max_length', parseInt(e.target.value))}
                          className="settings-field"
                        />
                        <TextField
                          margin="normal"
                          label="温度参数"
                          type="number"
                          inputProps={{ step: 0.1, min: 0, max: 2 }}
                          value={config.local_model_temperature || 0.7}
                          onChange={(e) => handleInputChange('local_model_temperature', parseFloat(e.target.value))}
                          className="settings-field"
                        />
                      </Box>
                    </Box>
                  </AccordionDetails>
                </Accordion>
              )}

            </Box>
          )}
        </DialogContent>

        <DialogActions sx={{ p: 3, justifyContent: 'space-between' }}>
          <Box>
            <Button
              onClick={handleTestConnection}
              disabled={testing || !config.provider || (validation && !validation.valid)}
              startIcon={testing ? <CircularProgress size={16} /> : <TestIcon />}
              className="settings-test-button"
              variant="outlined"
            >
              {testing ? '测试中...' : '测试连接'}
            </Button>
          </Box>
          
          <Box display="flex" gap={1}>
            <Button onClick={onClose} disabled={saving}>
              取消
            </Button>
            <Button
              onClick={handleSave}
              disabled={saving || !hasUnsavedChanges || (validation && !validation.valid)}
              startIcon={saving ? <CircularProgress size={16} /> : <SaveIcon />}
              variant="contained"
              className="settings-primary-button"
            >
              {saving ? '保存中...' : '保存配置'}
            </Button>
          </Box>
        </DialogActions>
      </Dialog>

      {/* 消息提示 */}
      <Snackbar
        open={!!message}
        autoHideDuration={6000}
        onClose={() => setMessage(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        {message && (
          <Alert 
            onClose={() => setMessage(null)} 
            severity={message.type}
            variant="filled"
            sx={{ width: '100%' }}
          >
            {message.text}
          </Alert>
        )}
      </Snackbar>
    </>
  );
};

export default Settings; 