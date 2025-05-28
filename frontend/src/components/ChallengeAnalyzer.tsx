import React, { useEffect, useState } from 'react';
import { AIProvidersResponse, analyzeChallenge, analyzeChallengeWithProvider, getAIProviders } from '../services/api';
import { QuestionResponse } from '../types';

const ChallengeAnalyzer: React.FC = () => {
  const [description, setDescription] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QuestionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [aiProviders, setAiProviders] = useState<AIProvidersResponse | null>(null);
  const [selectedProvider, setSelectedProvider] = useState<string>('');

  useEffect(() => {
    loadAIProviders();
  }, []);

  const loadAIProviders = async () => {
    try {
      const providers = await getAIProviders();
      setAiProviders(providers);
      setSelectedProvider(providers.current_provider);
    } catch (err) {
      console.error('加载AI提供者失败:', err);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0] || null;
    setFile(selectedFile);
  };

  const handleSubmit = async () => {
    if (!description.trim() && !file) {
      setError('请输入题目描述或上传文件');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      let response: QuestionResponse;
      if (selectedProvider && selectedProvider !== aiProviders?.current_provider) {
        response = await analyzeChallengeWithProvider(description, file, selectedProvider);
      } else {
        response = await analyzeChallenge(description, file);
      }
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : '分析失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const containerStyle: React.CSSProperties = {
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
    color: '#fff',
    backgroundColor: '#121212'
  };

  const cardStyle: React.CSSProperties = {
    backgroundColor: '#1e1e1e',
    border: '1px solid #333',
    borderRadius: '8px',
    padding: '20px',
    margin: '20px 0',
    boxShadow: '0 2px 4px rgba(0,0,0,0.3)'
  };

  const inputStyle: React.CSSProperties = {
    width: '100%',
    padding: '12px',
    backgroundColor: '#2e2e2e',
    border: '1px solid #555',
    borderRadius: '4px',
    color: '#fff',
    fontSize: '14px',
    fontFamily: 'inherit'
  };

  const buttonStyle: React.CSSProperties = {
    padding: '12px 24px',
    margin: '8px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: 'bold'
  };

  const primaryButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    backgroundColor: '#00bcd4',
    color: '#000'
  };

  return (
    <div style={containerStyle}>
      <h2 style={{ marginBottom: '24px' }}>CTF题目智能分析</h2>
      
      <div style={cardStyle}>
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
            AI提供者
          </label>
          <select
            value={selectedProvider}
            onChange={(e) => setSelectedProvider(e.target.value)}
            title="选择AI提供者"
            style={{
              ...inputStyle,
              marginBottom: '16px'
            }}
          >
            {aiProviders && Object.entries(aiProviders.available_providers).map(([key, name]) => (
              <option key={key} value={key}>
                {name} {key === aiProviders.current_provider ? '(当前默认)' : ''}
              </option>
            ))}
          </select>
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
            题目描述
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="请输入CTF题目的描述、提示信息或相关代码..."
            rows={6}
            style={{
              ...inputStyle,
              resize: 'vertical'
            }}
          />
        </div>
        
        <div style={{ display: 'flex', gap: '16px', marginBottom: '16px' }}>
          <label style={{ flex: 1, cursor: 'pointer' }}>
            <div style={{
              padding: '12px',
              backgroundColor: '#333',
              border: '1px solid #555',
              borderRadius: '4px',
              textAlign: 'center',
              color: '#fff'
            }}>
              {file ? file.name : '上传文件'}
            </div>
            <input
              type="file"
              style={{ display: 'none' }}
              accept=".txt,.py,.c,.cpp,.js,.php,.html,.pcap,.zip,.exe,.elf,.bin"
              onChange={handleFileChange}
            />
          </label>
          
          <button
            onClick={handleSubmit}
            disabled={loading}
            style={{
              ...primaryButtonStyle,
              flex: 1,
              opacity: loading ? 0.6 : 1
            }}
          >
            {loading ? '分析中...' : '开始分析'}
          </button>
        </div>
        
        {error && (
          <div style={{
            backgroundColor: '#f44336',
            color: '#fff',
            padding: '12px',
            borderRadius: '4px',
            marginTop: '16px'
          }}>
            {error}
          </div>
        )}
      </div>
      
      {result && (
        <div style={cardStyle}>
          <h3>分析结果</h3>
          <div style={{ margin: '16px 0' }}>
            <span style={{
              backgroundColor: '#00bcd4',
              color: '#000',
              padding: '4px 8px',
              borderRadius: '16px',
              fontSize: '12px',
              fontWeight: 'bold'
            }}>
              {result.type.toUpperCase()}
            </span>
          </div>
          <p><strong>分析时间:</strong> {new Date(result.timestamp).toLocaleString()}</p>
          
          <h4>推荐工具</h4>
          {result.recommended_tools.map(tool => (
            <div key={tool.id} style={{
              backgroundColor: '#2e2e2e',
              padding: '12px',
              margin: '8px 0',
              borderRadius: '4px'
            }}>
              <strong>{tool.name}</strong><br />
              <small style={{ color: '#999' }}>{tool.description}</small><br />
              <code style={{
                backgroundColor: '#333',
                padding: '4px',
                borderRadius: '2px',
                fontFamily: 'monospace'
              }}>
                {tool.command_template}
              </code>
            </div>
          ))}
          
          <h4>AI分析结果</h4>
          <div style={{
            backgroundColor: '#2e2e2e',
            padding: '16px',
            borderRadius: '4px',
            whiteSpace: 'pre-line'
          }}>
            {result.ai_response}
          </div>
        </div>
      )}
    </div>
  );
};

export default ChallengeAnalyzer; 