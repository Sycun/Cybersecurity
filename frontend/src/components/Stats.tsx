import {
    Lock as CryptoIcon,
    Extension as MiscIcon,
    Security as PwnIcon,
    Code as ReverseIcon,
    Web as WebIcon
} from '@mui/icons-material';
import {
    Alert,
    Box,
    Card,
    CardContent,
    CircularProgress,
    Grid,
    LinearProgress,
    Typography
} from '@mui/material';
import React, { useEffect, useState } from 'react';
import { getStats } from '../services/api';
import { StatsResponse } from '../types';

const Stats: React.FC = () => {
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      const data = await getStats();
      setStats(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '加载统计信息失败');
    } finally {
      setLoading(false);
    }
  };

  const getTypeIcon = (type: string) => {
    const icons: { [key: string]: React.ReactElement } = {
      web: <WebIcon />,
      pwn: <PwnIcon />,
      reverse: <ReverseIcon />,
      crypto: <CryptoIcon />,
      misc: <MiscIcon />
    };
    return icons[type] || <MiscIcon />;
  };

  const getTypeColor = (type: string) => {
    const colors: { [key: string]: string } = {
      web: '#2196f3',
      pwn: '#f44336',
      reverse: '#ff9800',
      crypto: '#00bcd4',
      misc: '#4caf50'
    };
    return colors[type] || '#9e9e9e';
  };

  const getTypeName = (type: string) => {
    const names: { [key: string]: string } = {
      web: 'Web安全',
      pwn: '二进制漏洞',
      reverse: '逆向工程',
      crypto: '密码学',
      misc: '杂项'
    };
    return names[type] || type.toUpperCase();
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        {error}
      </Alert>
    );
  }

  if (!stats) {
    return (
      <Alert severity="info">
        暂无统计数据
      </Alert>
    );
  }

  const maxCount = Math.max(...Object.values(stats.type_stats));

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        统计信息
      </Typography>

      {/* 总体统计 */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            总体统计
          </Typography>
          <Typography variant="h3" color="primary">
            {stats.total_questions}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            总分析题目数
          </Typography>
        </CardContent>
      </Card>

      {/* 分类统计 */}
      <Typography variant="h5" gutterBottom>
        题目类型分布
      </Typography>
      
      <Grid container spacing={3}>
        {Object.entries(stats.type_stats).map(([type, count]) => (
          <Grid item xs={12} sm={6} md={4} key={type}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <Box 
                    sx={{ 
                      color: getTypeColor(type),
                      mr: 2,
                      display: 'flex',
                      alignItems: 'center'
                    }}
                  >
                    {getTypeIcon(type)}
                  </Box>
                  <Typography variant="h6">
                    {getTypeName(type)}
                  </Typography>
                </Box>
                
                <Typography variant="h4" color="primary" gutterBottom>
                  {count}
                </Typography>
                
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  占比: {stats.total_questions > 0 ? ((count / stats.total_questions) * 100).toFixed(1) : 0}%
                </Typography>
                
                <LinearProgress
                  variant="determinate"
                  value={maxCount > 0 ? (count / maxCount) * 100 : 0}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    backgroundColor: 'rgba(0,0,0,0.1)',
                    '& .MuiLinearProgress-bar': {
                      backgroundColor: getTypeColor(type),
                      borderRadius: 4
                    }
                  }}
                />
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* 使用提示 */}
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            使用提示
          </Typography>
          <Typography variant="body2" color="text.secondary">
            • 统计数据实时更新，反映您的CTF学习进度
          </Typography>
          <Typography variant="body2" color="text.secondary">
            • 可以通过分析不同类型的题目来提升综合能力
          </Typography>
          <Typography variant="body2" color="text.secondary">
            • 建议重点关注分析数量较少的题目类型
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Stats; 