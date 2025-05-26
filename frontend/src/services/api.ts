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