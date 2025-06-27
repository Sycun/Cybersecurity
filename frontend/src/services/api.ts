import axios from 'axios';
import { QuestionResponse, StatsResponse, ToolResponse } from '../types';

// 从环境变量获取API基础URL，如果没有设置则使用默认值
const API_BASE_URL = process.env.REACT_APP_API_URL || 
                    process.env.REACT_APP_BACKEND_URL || 
                    'http://localhost:8000';

// 创建axios实例，支持环境变量配置
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: parseInt(process.env.REACT_APP_API_TIMEOUT || '60000'), // 默认60秒超时
  headers: {
    'Content-Type': 'application/json',
  },
});

// 添加请求拦截器，用于添加认证头等
api.interceptors.request.use(
  (config) => {
    // 从localStorage获取token（如果实现了认证）
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 分析CTF题目
export const analyzeChallenge = async (request: {
  description: string;
  question_type: string;
  ai_provider?: string;
  user_id?: string;
  conversation_id?: string;
  use_context?: boolean;
}): Promise<{
  success: boolean;
  response: string;
  conversation_id?: string;
  ai_provider?: string;
}> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error('分析失败');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('分析失败:', error);
    throw error;
  }
};

// 获取推荐工具
export const getToolsByType = async (questionType: string): Promise<ToolResponse[]> => {
  const response = await api.get(`/api/tools/${questionType}`);
  return response.data;
};

// 获取历史记录
export const getHistory = async (skip = 0, limit = 20): Promise<QuestionResponse[]> => {
  const response = await api.get('/api/history', {
    params: { skip, limit }
  });
  return response.data;
};

// 删除历史记录
export const deleteHistoryItem = async (questionId: number): Promise<void> => {
  await api.delete(`/api/history/${questionId}`);
};

// 获取统计信息
export const getStats = async (): Promise<StatsResponse> => {
  const response = await api.get('/api/stats');
  return response.data;
};

// 获取性能统计信息
export const getPerformanceStats = async (): Promise<any> => {
  const response = await api.get('/api/stats/performance');
  return response.data;
};

// 获取缓存统计信息
export const getCacheStats = async (): Promise<any> => {
  const response = await api.get('/api/cache/stats');
  return response.data;
};

// 清空缓存
export const clearCache = async (): Promise<void> => {
  await api.post('/api/cache/clear');
};

// 健康检查
export const healthCheck = async (): Promise<any> => {
  const response = await api.get('/health');
  return response.data;
};

// AI提供者相关接口
export interface AIProvider {
  [key: string]: string;
}

export interface AIProvidersResponse {
  available_providers: AIProvider;
  current_provider: string;
  current_provider_name: string;
}

// 获取AI提供者列表
export const getAIProviders = async (): Promise<any> => {
  const response = await fetch(`${API_BASE_URL}/api/ai/providers`);
  if (!response.ok) {
    throw new Error('获取AI提供者失败');
  }
  return response.json();
};

// 切换AI提供者
export const switchAIProvider = async (providerType: string): Promise<any> => {
  const response = await fetch(`${API_BASE_URL}/api/ai/switch`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ provider_type: providerType }),
  });
  if (!response.ok) {
    throw new Error('切换AI提供者失败');
  }
  return response.json();
};

// 获取AI提供者状态
export const getAIProviderStatus = async (): Promise<any> => {
  const response = await fetch(`${API_BASE_URL}/api/ai/status`);
  if (!response.ok) {
    throw new Error('获取AI提供者状态失败');
  }
  return response.json();
};

// 使用指定AI提供者分析CTF题目
export const analyzeChallengeWithProvider = async (
  text: string,
  file?: File | null,
  provider?: string
): Promise<QuestionResponse> => {
  const formData = new FormData();
  
  if (text) {
    formData.append('text', text);
  }
  
  if (file) {
    formData.append('file', file);
  }
  
  if (provider) {
    formData.append('provider', provider);
  }
  
  const response = await api.post('/api/analyze/with-provider', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

// 错误处理拦截器
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // 服务器返回错误状态码
      const message = error.response.data?.detail || error.response.data?.message || '服务器错误';
      throw new Error(message);
    } else if (error.request) {
      // 网络错误
      throw new Error('网络连接失败，请检查网络设置');
    } else {
      // 其他错误
      throw new Error('请求失败，请重试');
    }
  }
);

// 设置相关接口
export interface AIConfig {
  provider: string;
  deepseek_api_key?: string;
  deepseek_api_url?: string;
  deepseek_model?: string;
  siliconflow_api_key?: string;
  siliconflow_api_url?: string;
  siliconflow_model?: string;
  openai_compatible_api_url?: string;
  openai_compatible_api_key?: string;
  openai_compatible_model?: string;
  local_model_path?: string;
  local_model_type?: string;
  local_model_device?: string;
  local_model_max_length?: number;
  local_model_temperature?: number;
}

// 获取设置
export const getSettings = async (): Promise<AIConfig> => {
  const response = await api.get('/api/settings');
  return response.data;
};

// 更新设置
export const updateSettings = async (config: AIConfig): Promise<{
  message: string;
  updated_fields?: string[];
  current_provider?: string;
}> => {
  const response = await api.post('/api/settings', config);
  return response.data;
};

// 验证设置
export const validateSettings = async (config: AIConfig): Promise<{
  valid: boolean;
  errors: string[];
  warnings: string[];
}> => {
  const response = await api.post('/api/settings/validate', config);
  return response.data;
};

// 测试连接
export const testConnection = async (provider?: string, config?: AIConfig): Promise<{
  success: boolean;
  message: string;
  provider: string;
  response_preview?: string;
  error_details?: string;
}> => {
  const response = await api.post('/api/settings/test-connection', {
    provider,
    config
  });
  return response.data;
};

// 自动解题相关接口
export const autoSolveChallenge = async (request: {
  question_id: number;
  solve_method?: string;
  custom_code?: string;
  parameters?: Record<string, any>;
}): Promise<any> => {
  const response = await api.post('/api/auto-solve', request);
  return response.data;
};

export const getAutoSolveResult = async (solveId: number): Promise<any> => {
  const response = await api.get(`/api/auto-solve/${solveId}`);
  return response.data;
};

// 代码执行接口
export const executeCode = async (request: {
  code: string;
  language: string;
  input_data?: string;
  timeout?: number;
}): Promise<any> => {
  const response = await api.post('/api/execute-code', request);
  return response.data;
};

// 解题模板接口
export const getSolveTemplates = async (category?: string): Promise<any> => {
  const response = await api.get('/api/solve-templates', {
    params: { category }
  });
  return response.data;
};

export const createSolveTemplate = async (template: {
  name: string;
  category: string;
  description?: string;
  template_code: string;
  parameters?: Record<string, any>;
}): Promise<any> => {
  const response = await api.post('/api/solve-templates', template);
  return response.data;
};

// 对话相关接口
export const createConversation = async (userId?: string, initialContext?: any): Promise<string | null> => {
  try {
    const response = await api.post('/api/conversations', {
      user_id: userId,
      initial_context: initialContext
    });
    return response.data.conversation_id;
  } catch (error) {
    console.error('创建对话失败:', error);
    return null;
  }
};

export const getConversation = async (conversationId: string): Promise<any | null> => {
  try {
    const response = await api.get(`/api/conversations/${conversationId}`);
    return response.data;
  } catch (error) {
    console.error('获取对话失败:', error);
    return null;
  }
};

export const getUserConversations = async (userId: string, limit: number = 10): Promise<any[]> => {
  try {
    const response = await api.get(`/api/conversations/user/${userId}`, {
      params: { limit }
    });
    return response.data;
  } catch (error) {
    console.error('获取用户对话列表失败:', error);
    return [];
  }
};

export const deleteConversation = async (conversationId: string): Promise<boolean> => {
  try {
    await api.delete(`/api/conversations/${conversationId}`);
    return true;
  } catch (error) {
    console.error('删除对话失败:', error);
    return false;
  }
};

export const addMessage = async (conversationId: string, role: string, content: string, metadata?: any): Promise<boolean> => {
  try {
    await api.post(`/api/conversations/${conversationId}/messages`, {
      role,
      content,
      metadata
    });
    return true;
  } catch (error) {
    console.error('添加消息失败:', error);
    return false;
  }
};

// 导出API基础URL，供其他模块使用
export { API_BASE_URL };
