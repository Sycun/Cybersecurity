import {
    Close as CloseIcon,
    Launch as LaunchIcon
} from '@mui/icons-material';
import {
    Alert,
    Box,
    CircularProgress,
    Dialog,
    DialogContent,
    DialogTitle,
    IconButton,
    Toolbar,
    Typography
} from '@mui/material';
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import rehypeRaw from 'rehype-raw';
import remarkGfm from 'remark-gfm';
import './DocumentViewer.css';
import './highlight.css';

interface DocumentViewerProps {
  open: boolean;
  onClose: () => void;
  filename: string;
  title: string;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ 
  open, 
  onClose, 
  filename, 
  title 
}) => {
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    if (open && filename) {
      fetchDocument();
    }
  }, [open, filename]);

  const fetchDocument = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.get(`/docs/${encodeURIComponent(filename)}`);
      setContent(response.data);
    } catch (error: any) {
      console.error('Error fetching document:', error);
      if (error.response?.status === 404) {
        setError('文档未找到');
      } else {
        setError('加载文档失败，请稍后重试');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleOpenInGitHub = () => {
    const baseUrl = 'https://github.com/your-repo/blob/main/docs/';
    const url = baseUrl + encodeURIComponent(filename);
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  const customRenderers = {
    // 自定义代码块渲染
    code: ({ node, inline, className, children, ...props }: any) => {
      const match = /language-(\w+)/.exec(className || '');
      return !inline && match ? (
        <pre className={className}>
          <code className={className} {...props}>
            {children}
          </code>
        </pre>
      ) : (
        <code className={className} {...props}>
          {children}
        </code>
      );
    },
    // 自定义链接渲染
    a: ({ href, children, ...props }: any) => {
      const isExternal = href?.startsWith('http');
      return (
        <a 
          href={href} 
          target={isExternal ? '_blank' : undefined}
          rel={isExternal ? 'noopener noreferrer' : undefined}
          {...props}
        >
          {children}
        </a>
      );
    },
    // 自定义表格渲染
    table: ({ children, ...props }: any) => (
      <div className="table-container">
        <table {...props}>{children}</table>
      </div>
    )
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="lg"
      fullWidth
      PaperProps={{
        className: 'document-viewer-dialog'
      }}
    >
      <DialogTitle sx={{ p: 0 }}>
        <Toolbar className="document-viewer-toolbar">
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            📄 {title}
          </Typography>
          <IconButton
            edge="end"
            color="inherit"
            onClick={handleOpenInGitHub}
            aria-label="在GitHub打开"
            title="在GitHub打开"
          >
            <LaunchIcon />
          </IconButton>
          <IconButton
            edge="end"
            color="inherit"
            onClick={onClose}
            aria-label="关闭"
          >
            <CloseIcon />
          </IconButton>
        </Toolbar>
      </DialogTitle>
      
      <DialogContent className="document-viewer-content">
        {loading && (
          <Box display="flex" justifyContent="center" py={4}>
            <CircularProgress />
          </Box>
        )}
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        
        {!loading && !error && content && (
          <div className="markdown-content">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeHighlight, rehypeRaw]}
              components={customRenderers}
            >
              {content}
            </ReactMarkdown>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
};

export default DocumentViewer;