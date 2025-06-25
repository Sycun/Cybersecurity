import { AnalysisHistory, UserConfig } from '../types';

// 数据文件路径常量
const DATA_PATHS = {
  CHALLENGES: 'data/challenges',
  HISTORY: 'data/analysis_history',
  CONFIGS: 'data/configs',
  CACHE: 'data/cache',
  EXPORTS: 'data/exports'
};

// 默认配置
const DEFAULT_CONFIG: UserConfig = {
  aiProvider: 'deepseek',
  apiKey: '',
  model: 'deepseek-chat',
  temperature: 0.7,
  maxTokens: 2000,
  enableCache: true,
  cacheTTL: 3600,
  theme: 'dark',
  language: 'zh-CN'
};

class LocalDataService {
  private static instance: LocalDataService;

  private constructor() {
    this.ensureDataDirectories();
  }

  public static getInstance(): LocalDataService {
    if (!LocalDataService.instance) {
      LocalDataService.instance = new LocalDataService();
    }
    return LocalDataService.instance;
  }

  // 确保数据目录存在
  private async ensureDataDirectories(): Promise<void> {
    const dirs = Object.values(DATA_PATHS);
    for (const dir of dirs) {
      try {
        await this.createDirectory(dir);
      } catch (error) {
        console.warn(`创建目录失败: ${dir}`, error);
      }
    }
  }

  // 创建目录
  private async createDirectory(path: string): Promise<void> {
    try {
      const response = await fetch(`/api/fs/mkdir`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path })
      });
      if (!response.ok) throw new Error(`创建目录失败: ${path}`);
    } catch (error) {
      console.warn(`使用localStorage作为备选存储: ${path}`);
    }
  }

  // 保存分析历史
  async saveAnalysisHistory(history: AnalysisHistory): Promise<void> {
    try {
      const timestamp = new Date().toISOString();
      const filename = `analysis_${timestamp.replace(/[:.]/g, '-')}.json`;
      const filepath = `${DATA_PATHS.HISTORY}/${filename}`;
      
      await this.writeFile(filepath, JSON.stringify(history, null, 2));
      this.saveToLocalStorage('analysis_history', history);
    } catch (error) {
      console.error('保存分析历史失败:', error);
      throw error;
    }
  }

  // 获取分析历史
  async getAnalysisHistory(limit: number = 50): Promise<AnalysisHistory[]> {
    try {
      const response = await fetch(`/api/fs/readdir?path=${DATA_PATHS.HISTORY}`);
      if (response.ok) {
        const files = await response.json();
        const historyFiles = files
          .filter((file: string) => file.endsWith('.json'))
          .sort()
          .reverse()
          .slice(0, limit);

        const histories: AnalysisHistory[] = [];
        for (const file of historyFiles) {
          const content = await this.readFile(`${DATA_PATHS.HISTORY}/${file}`);
          if (content) {
            histories.push(JSON.parse(content));
          }
        }
        return histories;
      }
    } catch (error) {
      console.warn('从文件系统读取历史失败，使用localStorage:', error);
    }

    return this.getFromLocalStorage('analysis_history') || [];
  }

  // 保存用户配置
  async saveUserConfig(config: UserConfig): Promise<void> {
    try {
      await this.writeFile(`${DATA_PATHS.CONFIGS}/user_config.json`, JSON.stringify(config, null, 2));
      this.saveToLocalStorage('user_config', config);
    } catch (error) {
      console.error('保存用户配置失败:', error);
      throw error;
    }
  }

  // 获取用户配置
  async getUserConfig(): Promise<UserConfig> {
    try {
      const content = await this.readFile(`${DATA_PATHS.CONFIGS}/user_config.json`);
      if (content) {
        const config = JSON.parse(content);
        this.saveToLocalStorage('user_config', config);
        return config;
      }
    } catch (error) {
      console.warn('从文件系统读取配置失败，使用localStorage:', error);
    }

    const savedConfig = this.getFromLocalStorage('user_config');
    return savedConfig || DEFAULT_CONFIG;
  }

  // 保存CTF题目
  async saveChallenge(challenge: any, category: string): Promise<void> {
    try {
      const timestamp = new Date().toISOString();
      const filename = `challenge_${timestamp.replace(/[:.]/g, '-')}.json`;
      const filepath = `${DATA_PATHS.CHALLENGES}/${category}/${filename}`;
      
      await this.writeFile(filepath, JSON.stringify(challenge, null, 2));
    } catch (error) {
      console.error('保存题目失败:', error);
      throw error;
    }
  }

  // 获取CTF题目
  async getChallenges(category?: string): Promise<any[]> {
    try {
      const basePath = category ? `${DATA_PATHS.CHALLENGES}/${category}` : DATA_PATHS.CHALLENGES;
      const response = await fetch(`/api/fs/readdir?path=${basePath}`);
      
      if (response.ok) {
        const files = await response.json();
        const challengeFiles = files.filter((file: string) => file.endsWith('.json'));
        
        const challenges: any[] = [];
        for (const file of challengeFiles) {
          const content = await this.readFile(`${basePath}/${file}`);
          if (content) {
            challenges.push(JSON.parse(content));
          }
        }
        return challenges;
      }
    } catch (error) {
      console.warn('从文件系统读取题目失败:', error);
    }

    return [];
  }

  // 缓存AI响应
  async cacheAIResponse(key: string, response: any, ttl: number = 3600): Promise<void> {
    try {
      const cacheData = {
        response,
        timestamp: Date.now(),
        ttl
      };
      
      const filename = `${key.replace(/[^a-zA-Z0-9]/g, '_')}.json`;
      await this.writeFile(`${DATA_PATHS.CACHE}/${filename}`, JSON.stringify(cacheData, null, 2));
    } catch (error) {
      console.error('缓存AI响应失败:', error);
    }
  }

  // 获取缓存的AI响应
  async getCachedAIResponse(key: string): Promise<any | null> {
    try {
      const filename = `${key.replace(/[^a-zA-Z0-9]/g, '_')}.json`;
      const content = await this.readFile(`${DATA_PATHS.CACHE}/${filename}`);
      
      if (content) {
        const cacheData = JSON.parse(content);
        const now = Date.now();
        
        if (now - cacheData.timestamp < cacheData.ttl * 1000) {
          return cacheData.response;
        } else {
          await this.deleteFile(`${DATA_PATHS.CACHE}/${filename}`);
        }
      }
    } catch (error) {
      console.warn('读取缓存失败:', error);
    }

    return null;
  }

  // 导出数据
  async exportData(type: 'history' | 'challenges' | 'config', format: 'json' | 'csv' = 'json'): Promise<string> {
    try {
      let data: any;
      
      switch (type) {
        case 'history':
          data = await this.getAnalysisHistory(1000);
          break;
        case 'challenges':
          data = await this.getChallenges();
          break;
        case 'config':
          data = await this.getUserConfig();
          break;
      }

      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const filename = `export_${type}_${timestamp}.${format}`;
      const filepath = `${DATA_PATHS.EXPORTS}/${filename}`;

      let content: string;
      if (format === 'csv') {
        content = this.convertToCSV(data);
      } else {
        content = JSON.stringify(data, null, 2);
      }

      await this.writeFile(filepath, content);
      return filepath;
    } catch (error) {
      console.error('导出数据失败:', error);
      throw error;
    }
  }

  // 文件操作辅助方法
  private async writeFile(path: string, content: string): Promise<void> {
    try {
      const response = await fetch('/api/fs/write', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path, content })
      });
      
      if (!response.ok) {
        throw new Error(`写入文件失败: ${path}`);
      }
    } catch (error) {
      this.saveToLocalStorage(path, content);
    }
  }

  private async readFile(path: string): Promise<string | null> {
    try {
      const response = await fetch(`/api/fs/read?path=${encodeURIComponent(path)}`);
      
      if (response.ok) {
        return await response.text();
      }
    } catch (error) {
      return this.getFromLocalStorage(path);
    }

    return null;
  }

  private async deleteFile(path: string): Promise<void> {
    try {
      const response = await fetch('/api/fs/delete', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path })
      });
      
      if (!response.ok) {
        throw new Error(`删除文件失败: ${path}`);
      }
    } catch (error) {
      console.warn('删除文件失败:', error);
    }
  }

  // localStorage辅助方法
  private saveToLocalStorage(key: string, value: any): void {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.warn('localStorage保存失败:', error);
    }
  }

  private getFromLocalStorage(key: string): any {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch (error) {
      console.warn('localStorage读取失败:', error);
      return null;
    }
  }

  // CSV转换
  private convertToCSV(data: any[]): string {
    if (!data || data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const csvRows = [headers.join(',')];
    
    for (const row of data) {
      const values = headers.map(header => {
        const value = row[header];
        return typeof value === 'string' ? `"${value.replace(/"/g, '""')}"` : value;
      });
      csvRows.push(values.join(','));
    }
    
    return csvRows.join('\n');
  }

  // 清理过期缓存
  async cleanupExpiredCache(): Promise<void> {
    try {
      const response = await fetch(`/api/fs/readdir?path=${DATA_PATHS.CACHE}`);
      if (response.ok) {
        const files = await response.json();
        
        for (const file of files) {
          if (file.endsWith('.json')) {
            const content = await this.readFile(`${DATA_PATHS.CACHE}/${file}`);
            if (content) {
              const cacheData = JSON.parse(content);
              const now = Date.now();
              
              if (now - cacheData.timestamp >= cacheData.ttl * 1000) {
                await this.deleteFile(`${DATA_PATHS.CACHE}/${file}`);
              }
            }
          }
        }
      }
    } catch (error) {
      console.warn('清理缓存失败:', error);
    }
  }
}

export default LocalDataService.getInstance(); 