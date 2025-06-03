import {
    ExpandMore,
    Refresh as RefreshIcon,
    Save as SaveIcon,
    Visibility,
    VisibilityOff
} from '@mui/icons-material';
import {
    Accordion,
    AccordionDetails,
    AccordionSummary,
    Alert,
    Box,
    Button,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    Divider,
    FormControl,
    IconButton,
    InputAdornment,
    InputLabel,
    MenuItem,
    Select,
    TextField,
    Typography
} from '@mui/material';
import React, { useEffect, useState } from 'react';
import { AIConfig, getSettings, testConnection, updateSettings } from '../services/api';
import './Settings.css';

interface SettingsProps {
  open: boolean;
  onClose: () => void;
}

const Settings: React.FC<SettingsProps> = ({ open, onClose }) => {
  const [config, setConfig] = useState<AIConfig>({
    provider: 'deepseek'
  });
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [testing, setTesting] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error' | 'info', text: string } | null>(null);
  const [showPassword, setShowPassword] = useState<{ [key: string]: boolean }>({});

  // 加载当前配置
  const loadSettings = async () => {
    try {
      setLoading(true);
      const settings = await getSettings();
      setConfig(settings);
    } catch (error) {
      setMessage({ type: 'error', text: `加载配置失败: ${error}` });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (open) {
      loadSettings();
    }
  }, [open]);

  // 处理输入变化
  const handleInputChange = (field: keyof AIConfig, value: string | number) => {
    setConfig(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // 切换密码显示
  const togglePasswordVisibility = (field: string) => {
    setShowPassword(prev => ({
      ...prev,
      [field]: !prev[field]
    }));
  };

  // 保存配置
  const handleSave = async () => {
    try {
      setSaving(true);
      await updateSettings(config);
      setMessage({ type: 'success', text: '配置保存成功！' });
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
      const result = await testConnection(config.provider);
      setMessage({ type: 'success', text: `连接测试成功: ${result.message}` });
    } catch (error) {
      setMessage({ type: 'error', text: `连接测试失败: ${error}` });
    } finally {
      setTesting(false);
    }
  };

  // 渲染密码输入框
  const renderPasswordField = (
    label: string,
    field: keyof AIConfig,
    value?: string,
    required?: boolean
  ) => (
    <TextField
      fullWidth
      margin="normal"
      label={label}
      type={showPassword[String(field)] ? 'text' : 'password'}
      value={value || ''}
      onChange={(e) => handleInputChange(field, e.target.value)}
      required={required}
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

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth className="settings-dialog">
      <DialogTitle>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Typography variant="h6">AI服务配置</Typography>
          <IconButton onClick={loadSettings} disabled={loading}>
            <RefreshIcon />
          </IconButton>
        </Box>
      </DialogTitle>
      
      <DialogContent>
        {loading ? (
          <Box className="settings-loading">
            <CircularProgress />
          </Box>
        ) : (
          <Box>
            {message && (
              <Alert 
                severity={message.type} 
                onClose={() => setMessage(null)}
                sx={{ mb: 2 }}
              >
                {message.text}
              </Alert>
            )}

            {/* AI服务选择 */}
            <FormControl fullWidth margin="normal" className="settings-provider-selector">
              <InputLabel>AI服务提供者</InputLabel>
              <Select
                value={config.provider}
                onChange={(e) => handleInputChange('provider', e.target.value)}
              >
                <MenuItem value="deepseek">DeepSeek</MenuItem>
                <MenuItem value="siliconflow">硅基流动</MenuItem>
                <MenuItem value="openai_compatible">OpenAI兼容API</MenuItem>
                <MenuItem value="local">本地模型</MenuItem>
              </Select>
            </FormControl>

            <Divider sx={{ my: 2 }} />

            {/* DeepSeek配置 */}
            {config.provider === 'deepseek' && (
              <Accordion defaultExpanded className="settings-accordion">
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography variant="subtitle1">DeepSeek 配置</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Box className="settings-section">
                    {renderPasswordField('API Key', 'deepseek_api_key', config.deepseek_api_key, true)}
                    <TextField
                      fullWidth
                      margin="normal"
                      label="API URL"
                      value={config.deepseek_api_url || 'https://api.deepseek.com/v1/chat/completions'}
                      onChange={(e) => handleInputChange('deepseek_api_url', e.target.value)}
                      className="settings-field"
                    />
                    <TextField
                      fullWidth
                      margin="normal"
                      label="模型名称"
                      value={config.deepseek_model || 'deepseek-chat'}
                      onChange={(e) => handleInputChange('deepseek_model', e.target.value)}
                      className="settings-field"
                    />
                  </Box>
                </AccordionDetails>
              </Accordion>
            )}

            {/* 硅基流动配置 */}
            {config.provider === 'siliconflow' && (
              <Accordion defaultExpanded className="settings-accordion">
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography variant="subtitle1">硅基流动 配置</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Box className="settings-section">
                    {renderPasswordField('API Key', 'siliconflow_api_key', config.siliconflow_api_key, true)}
                    <TextField
                      fullWidth
                      margin="normal"
                      label="API URL"
                      value={config.siliconflow_api_url || 'https://api.siliconflow.cn/v1/chat/completions'}
                      onChange={(e) => handleInputChange('siliconflow_api_url', e.target.value)}
                      className="settings-field"
                    />
                    <TextField
                      fullWidth
                      margin="normal"
                      label="模型名称"
                      value={config.siliconflow_model || 'Qwen/QwQ-32B'}
                      onChange={(e) => handleInputChange('siliconflow_model', e.target.value)}
                      className="settings-field"
                    />
                  </Box>
                </AccordionDetails>
              </Accordion>
            )}

            {/* OpenAI兼容API配置 */}
            {config.provider === 'openai_compatible' && (
              <Accordion defaultExpanded className="settings-accordion">
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography variant="subtitle1">OpenAI兼容API 配置</Typography>
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
                    />
                    {renderPasswordField('API Key', 'openai_compatible_api_key', config.openai_compatible_api_key)}
                    <TextField
                      fullWidth
                      margin="normal"
                      label="模型名称"
                      value={config.openai_compatible_model || 'gpt-3.5-turbo'}
                      onChange={(e) => handleInputChange('openai_compatible_model', e.target.value)}
                      className="settings-field"
                    />
                  </Box>
                </AccordionDetails>
              </Accordion>
            )}

            {/* 本地模型配置 */}
            {config.provider === 'local' && (
              <Accordion defaultExpanded className="settings-accordion">
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography variant="subtitle1">本地模型 配置</Typography>
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
                    />
                    <TextField
                      fullWidth
                      margin="normal"
                      label="模型类型"
                      value={config.local_model_type || 'auto'}
                      onChange={(e) => handleInputChange('local_model_type', e.target.value)}
                      className="settings-field"
                    />
                    <FormControl fullWidth margin="normal" className="settings-field">
                      <InputLabel>设备</InputLabel>
                      <Select
                        value={config.local_model_device || 'auto'}
                        onChange={(e) => handleInputChange('local_model_device', e.target.value)}
                      >
                        <MenuItem value="auto">自动</MenuItem>
                        <MenuItem value="cpu">CPU</MenuItem>
                        <MenuItem value="cuda">CUDA</MenuItem>
                      </Select>
                    </FormControl>
                    <Box className="settings-field-group">
                      <TextField
                        margin="normal"
                        label="最大长度"
                        type="number"
                        value={config.local_model_max_length || 4096}
                        onChange={(e) => handleInputChange('local_model_max_length', parseInt(e.target.value))}
                      />
                      <TextField
                        margin="normal"
                        label="温度参数"
                        type="number"
                        inputProps={{ step: 0.1, min: 0, max: 2 }}
                        value={config.local_model_temperature || 0.7}
                        onChange={(e) => handleInputChange('local_model_temperature', parseFloat(e.target.value))}
                      />
                    </Box>
                  </Box>
                </AccordionDetails>
              </Accordion>
            )}
          </Box>
        )}
      </DialogContent>

      <DialogActions>
        <Button
          onClick={handleTestConnection}
          disabled={testing || loading}
          startIcon={testing ? <CircularProgress size={16} /> : undefined}
          className="settings-test-button"
        >
          {testing ? '测试中...' : '测试连接'}
        </Button>
        <Button onClick={onClose}>
          取消
        </Button>
        <Button
          onClick={handleSave}
          variant="contained"
          disabled={saving || loading}
          startIcon={saving ? <CircularProgress size={16} /> : <SaveIcon />}
        >
          {saving ? '保存中...' : '保存'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default Settings; 