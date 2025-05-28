import axios from 'axios';
import { QuestionResponse, StatsResponse, ToolResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60秒超时
});

// 分析CTF题目
export const analyzeChallenge = async (
  text: string, 
  file?: File | null
): Promise<QuestionResponse> => {
  const formData = new FormData();
  
  if (text) {
    formData.append('text', text);
  }
  
  if (file) {
    formData.append('file', file);
  }
  
  const response = await api.post('/api/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
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
export const getAIProviders = async (): Promise<AIProvidersResponse> => {
  const response = await api.get('/api/ai/providers');
  return response.data;
};

// 切换AI提供者
export const switchAIProvider = async (providerType: string): Promise<void> => {
  const formData = new FormData();
  formData.append('provider_type', providerType);
  
  await api.post('/api/ai/switch', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
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