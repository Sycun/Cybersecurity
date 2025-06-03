import React, { useEffect, useState } from 'react';
import { getPerformanceStats } from '../services/api';
import './Performance.css';

interface PerformanceStats {
  ai_performance: {
    provider: string;
    provider_stats: {
      request_count: number;
      total_response_time: number;
      average_response_time: number;
    };
    cache_stats: {
      total_items: number;
      hit_count: number;
      miss_count: number;
      hit_rate: number;
      total_requests: number;
    };
  };
  config: {
    cache_enabled: boolean;
    cache_ttl: number;
    request_timeout: number;
  };
}

const Performance: React.FC = () => {
  const [stats, setStats] = useState<PerformanceStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadStats();
    const interval = setInterval(loadStats, 30000); // 每30秒刷新一次
    return () => clearInterval(interval);
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      const data = await getPerformanceStats();
      setStats(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : '加载性能统计失败');
    } finally {
      setLoading(false);
    }
  };

  const getStatusClass = (value: number, thresholds: { good: number; warning: number }) => {
    if (value >= thresholds.good) return 'performance-status-good';
    if (value >= thresholds.warning) return 'performance-status-warning';
    return 'performance-status-error';
  };

  if (loading) {
    return (
      <div className="performance-container">
        <h2>性能监控</h2>
        <div className="performance-loading">加载中...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="performance-container">
        <h2>性能监控</h2>
        <div className="performance-error">{error}</div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="performance-container">
        <h2>性能监控</h2>
        <div className="performance-no-data">暂无数据</div>
      </div>
    );
  }

  return (
    <div className="performance-container">
      <h2>性能监控</h2>
      
      {/* AI提供者性能 */}
      <div className="performance-card">
        <h3>AI提供者性能</h3>
        <div className="performance-stat-item">
          <span>当前提供者</span>
          <span className="performance-provider-tag">
            {stats.ai_performance.provider}
          </span>
        </div>
        <div className="performance-stat-item">
          <span>总请求数</span>
          <span>{stats.ai_performance.provider_stats.request_count}</span>
        </div>
        <div className="performance-stat-item">
          <span>总响应时间</span>
          <span>{stats.ai_performance.provider_stats.total_response_time.toFixed(2)}s</span>
        </div>
        <div className="performance-stat-item">
          <span>平均响应时间</span>
          <span className={getStatusClass(
            stats.ai_performance.provider_stats.average_response_time, 
            { good: 0, warning: 3 }
          )}>
            {stats.ai_performance.provider_stats.average_response_time.toFixed(2)}s
          </span>
        </div>
      </div>

      {/* 缓存性能 */}
      <div className="performance-card">
        <h3>缓存性能</h3>
        <div className="performance-stat-item">
          <span>缓存状态</span>
          <span className={stats.config.cache_enabled ? 'performance-status-enabled' : 'performance-status-disabled'}>
            {stats.config.cache_enabled ? '已启用' : '未启用'}
          </span>
        </div>
        {stats.config.cache_enabled && (
          <>
            <div className="performance-stat-item">
              <span>缓存项数量</span>
              <span>{stats.ai_performance.cache_stats.total_items}</span>
            </div>
            <div className="performance-stat-item">
              <span>缓存命中次数</span>
              <span className="performance-cache-hit">
                {stats.ai_performance.cache_stats.hit_count}
              </span>
            </div>
            <div className="performance-stat-item">
              <span>缓存未命中次数</span>
              <span className="performance-cache-miss">
                {stats.ai_performance.cache_stats.miss_count}
              </span>
            </div>
            <div className="performance-stat-item">
              <span>缓存命中率</span>
              <span className={getStatusClass(
                stats.ai_performance.cache_stats.hit_rate, 
                { good: 70, warning: 30 }
              )}>
                {stats.ai_performance.cache_stats.hit_rate}%
              </span>
            </div>
            <div className="performance-stat-item">
              <span>缓存TTL</span>
              <span>{stats.config.cache_ttl}s</span>
            </div>
          </>
        )}
      </div>

      {/* 系统配置 */}
      <div className="performance-card">
        <h3>系统配置</h3>
        <div className="performance-stat-item">
          <span>请求超时时间</span>
          <span>{stats.config.request_timeout}s</span>
        </div>
      </div>

      {/* 刷新按钮 */}
      <div className="performance-refresh-container">
        <button onClick={loadStats} className="performance-refresh-button">
          刷新数据
        </button>
      </div>
    </div>
  );
};

export default Performance; 