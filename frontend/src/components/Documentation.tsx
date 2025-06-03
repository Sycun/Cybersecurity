import {
  ApiTwoTone as ApiIcon,
  CategoryTwoTone as CategoryIcon,
  CloudUploadTwoTone as DeployIcon,
  AssignmentTwoTone as DocumentIcon,
  SchoolTwoTone as FeatureIcon,
  HomeTwoTone as HomeIcon,
  LaunchTwoTone as LaunchIcon,
  ComputerTwoTone as LocalModelIcon,
  TuneTwoTone as OptimizeIcon,
  Search as SearchIcon,
  SettingsTwoTone as SettingsIcon,
  UpdateTwoTone as UpdateIcon
} from '@mui/icons-material';
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Container,
  Divider,
  FormControl,
  Grid,
  InputAdornment,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography
} from '@mui/material';
import React, { useMemo, useState } from 'react';
import DocumentViewer from './DocumentViewer';
import './Documentation.css';

interface DocumentItem {
  title: string;
  description: string;
  filename: string;
  icon: React.ReactNode;
  category: string;
  audience: string[];
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  tags: string[];
  estimatedTime: string;
  lastUpdated: string;
}

const Documentation: React.FC = () => {
  const [viewerOpen, setViewerOpen] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState<DocumentItem | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [audienceFilter, setAudienceFilter] = useState('all');
  const [currentTab, setCurrentTab] = useState(0);

  const documents: DocumentItem[] = [
    {
      title: '📚 文档中心导航',
      description: '文档导航和快速索引，按用户角色和主题分类的完整文档指南，平台功能概览',
      filename: '文档中心导航.md',
      icon: <HomeIcon />,
      category: '导航',
      audience: ['所有用户'],
      difficulty: 'beginner',
      tags: ['导航', '概览', '入门'],
      estimatedTime: '5分钟',
      lastUpdated: '2024-01-01'
    },
    {
      title: '⚙️ 配置管理指南',
      description: '网页端配置管理详细说明，零代码AI服务配置，实时连接测试，安全密钥管理',
      filename: '配置管理指南.md',
      icon: <SettingsIcon />,
      category: '配置',
      audience: ['所有用户'],
      difficulty: 'beginner',
      tags: ['配置', '设置', 'AI服务', '连接测试'],
      estimatedTime: '15分钟',
      lastUpdated: '2024-01-01'
    },
    {
      title: '🎓 用户引导功能',
      description: '智能用户引导系统说明，6步交互式教程，首次访问指引，功能导航',
      filename: '用户引导功能.md',
      icon: <FeatureIcon />,
      category: '功能',
      audience: ['新用户', '所有用户'],
      difficulty: 'beginner',
      tags: ['引导', '教程', '新手', '交互'],
      estimatedTime: '10分钟',
      lastUpdated: '2024-01-01'
    },
    {
      title: '🚀 部署运维指南',
      description: 'Docker容器化部署，云端和本地部署方案，系统运维和监控，故障排除手册',
      filename: '部署指南.md',
      icon: <DeployIcon />,
      category: '运维',
      audience: ['运维人员', '开发者', '系统管理员'],
      difficulty: 'intermediate',
      tags: ['部署', 'Docker', '运维', '监控'],
      estimatedTime: '30分钟',
      lastUpdated: '2024-01-01'
    },
    {
      title: '📡 API接口文档',
      description: '完整的RESTful API参考文档，请求响应示例，SDK使用指南，接口调用规范',
      filename: 'API参考文档.md',
      icon: <ApiIcon />,
      category: '开发',
      audience: ['开发者', '技术集成'],
      difficulty: 'intermediate',
      tags: ['API', '接口', '开发', 'SDK'],
      estimatedTime: '25分钟',
      lastUpdated: '2024-01-01'
    },
    {
      title: '💻 本地模型部署',
      description: '本地AI模型配置和部署指南，transformers集成，GPU优化，离线运行方案',
      filename: '本地模型部署.md',
      icon: <LocalModelIcon />,
      category: '部署',
      audience: ['高级用户', '开发者'],
      difficulty: 'advanced',
      tags: ['本地模型', 'AI', '离线', 'GPU'],
      estimatedTime: '40分钟',
      lastUpdated: '2024-01-01'
    },
    {
      title: '🔧 性能优化总结',
      description: '系统性能优化策略，缓存机制，响应时间优化，资源使用优化指南',
      filename: '性能优化总结.md',
      icon: <OptimizeIcon />,
      category: '优化',
      audience: ['开发者', '运维人员'],
      difficulty: 'advanced',
      tags: ['性能', '优化', '缓存', '监控'],
      estimatedTime: '20分钟',
      lastUpdated: '2024-01-01'
    },
    {
      title: '📋 版本更新日志',
      description: '详细的版本更新记录，功能变更说明，Bug修复列表，未来发展计划',
      filename: '版本更新日志.md',
      icon: <UpdateIcon />,
      category: '版本',
      audience: ['所有用户'],
      difficulty: 'beginner',
      tags: ['更新', '版本', '变更', '历史'],
      estimatedTime: '8分钟',
      lastUpdated: '2024-01-01'
    },
    {
      title: '🔄 中文更新日志',
      description: '中文版本的详细更新记录，新功能介绍，改进说明，中文用户专用版本',
      filename: '更新日志.md',
      icon: <UpdateIcon />,
      category: '版本',
      audience: ['中文用户', '所有用户'],
      difficulty: 'beginner',
      tags: ['更新', '中文', '版本', '功能'],
      estimatedTime: '10分钟',
      lastUpdated: '2024-01-01'
    },
    {
      title: '📚 文档中心优化说明',
      description: '文档中心的全面优化改进说明，新功能介绍，界面优化和用户体验提升',
      filename: '文档中心优化说明.md',
      icon: <OptimizeIcon />,
      category: '功能',
      audience: ['所有用户', '开发者'],
      difficulty: 'intermediate',
      tags: ['优化', '文档', '功能', '界面'],
      estimatedTime: '12分钟',
      lastUpdated: '2024-01-01'
    }
  ];

  // 过滤和搜索逻辑
  const filteredDocuments = useMemo(() => {
    return documents.filter(doc => {
      const matchesSearch = doc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          doc.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          doc.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
      
      const matchesCategory = categoryFilter === 'all' || doc.category === categoryFilter;
      const matchesAudience = audienceFilter === 'all' || doc.audience.includes(audienceFilter);
      
      return matchesSearch && matchesCategory && matchesAudience;
    });
  }, [searchTerm, categoryFilter, audienceFilter]);

  // 按类别分组文档
  const documentsByCategory = useMemo(() => {
    const grouped: { [key: string]: DocumentItem[] } = {};
    filteredDocuments.forEach(doc => {
      if (!grouped[doc.category]) {
        grouped[doc.category] = [];
      }
      grouped[doc.category].push(doc);
    });
    return grouped;
  }, [filteredDocuments]);

  // 获取所有类别
  const categories = useMemo(() => {
    return Array.from(new Set(documents.map(doc => doc.category)));
  }, []);

  // 获取所有受众
  const audiences = useMemo(() => {
    const allAudiences = documents.flatMap(doc => doc.audience);
    return Array.from(new Set(allAudiences));
  }, []);

  const handleOpenDocument = (doc: DocumentItem) => {
    setSelectedDoc(doc);
    setViewerOpen(true);
  };

  const handleOpenInGitHub = (filename: string) => {
    const baseUrl = 'https://github.com/your-repo/blob/main/docs/';
    const url = baseUrl + encodeURIComponent(filename);
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  const getCategoryColor = (category: string) => {
    const colors: { [key: string]: string } = {
      '导航': 'primary',
      '配置': 'secondary',
      '功能': 'info',
      '开发': 'success', 
      '运维': 'warning',
      '部署': 'error',
      '优化': 'success',
      '版本': 'info'
    };
    return colors[category] || 'default';
  };

  const getDifficultyColor = (difficulty: string) => {
    const colors: { [key: string]: string } = {
      'beginner': 'success',
      'intermediate': 'warning',
      'advanced': 'error'
    };
    return colors[difficulty] || 'default';
  };

  const getDifficultyText = (difficulty: string) => {
    const texts: { [key: string]: string } = {
      'beginner': '入门',
      'intermediate': '中级',
      'advanced': '高级'
    };
    return texts[difficulty] || '未知';
  };

  return (
    <Container maxWidth="lg" className="documentation-container">
      <Box className="documentation-header">
        <Typography variant="h3" component="h1" gutterBottom>
          📚 文档中心
        </Typography>
        <Typography variant="h6" color="text.secondary" paragraph>
          CTF智能分析平台完整文档指南 - 涵盖配置、部署、开发和优化的全方位文档
        </Typography>
        
        {/* 搜索和过滤控制 */}
        <Box sx={{ display: 'flex', gap: 2, mb: 3, flexWrap: 'wrap' }}>
          <TextField
            placeholder="搜索文档..."
            variant="outlined"
            size="small"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
            sx={{ minWidth: 250 }}
          />
          
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>类别</InputLabel>
            <Select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              label="类别"
            >
              <MenuItem value="all">全部类别</MenuItem>
              {categories.map(category => (
                <MenuItem key={category} value={category}>{category}</MenuItem>
              ))}
            </Select>
          </FormControl>
          
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>受众</InputLabel>
            <Select
              value={audienceFilter}
              onChange={(e) => setAudienceFilter(e.target.value)}
              label="受众"
            >
              <MenuItem value="all">所有用户</MenuItem>
              {audiences.map(audience => (
                <MenuItem key={audience} value={audience}>{audience}</MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>

        <Divider sx={{ mb: 3 }} />
      </Box>

      {/* 统计信息 */}
      <Box sx={{ mb: 3, p: 2, bgcolor: 'background.paper', borderRadius: 2 }}>
        <Typography variant="body2" color="text.secondary">
          📊 文档统计：共 {documents.length} 个文档，显示 {filteredDocuments.length} 个结果
          {searchTerm && ` | 搜索关键词："${searchTerm}"`}
          {categoryFilter !== 'all' && ` | 类别：${categoryFilter}`}
          {audienceFilter !== 'all' && ` | 受众：${audienceFilter}`}
        </Typography>
      </Box>

      {/* 按类别显示文档 */}
      {Object.entries(documentsByCategory).map(([category, docs]) => (
        <Box key={category} sx={{ mb: 4 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <CategoryIcon color="primary" />
            <Typography variant="h5" component="h2">
              {category} ({docs.length})
            </Typography>
            <Chip 
              label={category}
              color={getCategoryColor(category) as any}
              size="small"
            />
          </Box>
          
          <Grid container spacing={3}>
            {docs.map((doc, index) => (
              <Grid item xs={12} md={6} lg={4} key={index}>
                <Card className="documentation-card" elevation={2}>
                  <CardContent>
                    <Box className="documentation-card-header">
                      <Box className="documentation-icon">
                        {doc.icon}
                      </Box>
                      <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                        <Chip 
                          label={doc.category}
                          color={getCategoryColor(doc.category) as any}
                          size="small"
                          className="documentation-category"
                        />
                        <Chip 
                          label={getDifficultyText(doc.difficulty)}
                          color={getDifficultyColor(doc.difficulty) as any}
                          size="small"
                          variant="outlined"
                        />
                      </Box>
                    </Box>
                    
                    <Typography variant="h6" component="h3" gutterBottom>
                      {doc.title}
                    </Typography>
                    
                    <Typography 
                      variant="body2" 
                      color="text.secondary" 
                      paragraph
                      className="documentation-description"
                    >
                      {doc.description}
                    </Typography>

                    {/* 标签 */}
                    <Box sx={{ mb: 2 }}>
                      {doc.tags.slice(0, 3).map((tag, idx) => (
                        <Chip
                          key={idx}
                          label={tag}
                          size="small"
                          variant="outlined"
                          sx={{ mr: 0.5, mb: 0.5 }}
                        />
                      ))}
                      {doc.tags.length > 3 && (
                        <Chip
                          label={`+${doc.tags.length - 3}`}
                          size="small"
                          variant="outlined"
                          sx={{ mr: 0.5, mb: 0.5 }}
                        />
                      )}
                    </Box>

                    {/* 元信息 */}
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="caption" color="text.secondary" display="block">
                        ⏱️ 预计阅读时间：{doc.estimatedTime}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" display="block">
                        📅 最后更新：{doc.lastUpdated}
                      </Typography>
                    </Box>
                    
                    <Box className="documentation-audience">
                      <Typography variant="caption" color="text.secondary">
                        👥 适用对象：
                      </Typography>
                      {doc.audience.map((audience, idx) => (
                        <Chip
                          key={idx}
                          label={audience}
                          size="small"
                          variant="outlined"
                          className="audience-chip"
                        />
                      ))}
                    </Box>
                    
                    <Box className="documentation-actions">
                      <Button
                        variant="contained"
                        startIcon={<DocumentIcon />}
                        onClick={() => handleOpenDocument(doc)}
                        className="doc-button primary"
                        fullWidth
                      >
                        查看文档
                      </Button>
                      <Button
                        variant="outlined"
                        startIcon={<LaunchIcon />}
                        onClick={() => handleOpenInGitHub(doc.filename)}
                        className="doc-button secondary"
                        size="small"
                        sx={{ mt: 1 }}
                      >
                        在GitHub查看
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      ))}

      {/* 无结果提示 */}
      {filteredDocuments.length === 0 && (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            🔍 没有找到匹配的文档
          </Typography>
          <Typography variant="body2" color="text.secondary">
            尝试调整搜索关键词或过滤条件
          </Typography>
          <Button 
            variant="outlined" 
            onClick={() => {
              setSearchTerm('');
              setCategoryFilter('all');
              setAudienceFilter('all');
            }}
            sx={{ mt: 2 }}
          >
            清除所有过滤条件
          </Button>
        </Box>
      )}

      <Box className="documentation-footer">
        <Divider sx={{ my: 3 }} />
        <Typography variant="body2" color="text.secondary" align="center">
          💡 提示：点击"查看文档"在弹窗中阅读，"在GitHub查看"获取最新版本
        </Typography>
        <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 1 }}>
          📝 如有问题或建议，欢迎提交 Issue 或 Pull Request
        </Typography>
        <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 1 }}>
          🔄 文档持续更新中，感谢您的使用和反馈
        </Typography>
      </Box>

      {/* 文档查看器 */}
      {selectedDoc && (
        <DocumentViewer
          open={viewerOpen}
          onClose={() => setViewerOpen(false)}
          filename={selectedDoc.filename}
          title={selectedDoc.title}
        />
      )}
    </Container>
  );
};

export default Documentation; 