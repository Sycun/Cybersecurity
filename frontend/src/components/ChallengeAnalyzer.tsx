import React, { useEffect, useState } from 'react';
import { analyzeChallenge, getAIProviders } from '../services/api';
import { QuestionResponse } from '../types';
import './ChallengeAnalyzer.css';

interface AIProvider {
  name: string;
  description: string;
  type: 'cloud' | 'local' | 'local_cloud';
  languages: string[];
  max_tokens: number;
  features: string[];
}

interface AIProvidersData {
  current_provider: string;
  current_provider_info: AIProvider;
  available_providers: Record<string, AIProvider>;
}

interface ChallengeAnalyzerProps {
  onAnalysisComplete?: (result: any) => void;
}

const ChallengeAnalyzer: React.FC<ChallengeAnalyzerProps> = ({ onAnalysisComplete }) => {
  const [description, setDescription] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<QuestionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [aiProviders, setAiProviders] = useState<AIProvidersData | null>(null);
  const [selectedProvider, setSelectedProvider] = useState<string>('');
  const [useContext, setUseContext] = useState(true);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [conversationHistory, setConversationHistory] = useState<any[]>([]);
  const [questionType, setQuestionType] = useState('web');

  useEffect(() => {
    loadAIProviders();
  }, []);

  const loadAIProviders = async () => {
    try {
      const providers = await getAIProviders();
      setAiProviders(providers);
      if (providers && providers.available_providers) {
        const firstProvider = Object.keys(providers.available_providers)[0];
        setSelectedProvider(firstProvider);
      }
    } catch (error) {
      console.error('加载AI提供者失败:', error);
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0] || null;
    setFile(selectedFile);
  };

  const handleSubmit = async () => {
    if (!description.trim()) {
      setError('请输入题目描述');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await analyzeChallenge({
        description,
        question_type: questionType,
        ai_provider: selectedProvider,
        conversation_id: conversationId,
        use_context: useContext
      });

      if (response.success) {
        // 创建QuestionResponse格式的结果
        const questionResult: QuestionResponse = {
          id: conversationId || 'temp-id',
          description: description,
          type: questionType,
          ai_response: response.response,
          recommended_tools: [],
          timestamp: new Date().toISOString(),
          ai_provider: response.ai_provider
        };
        
        setResult(questionResult);
        setConversationId(response.conversation_id || null);
        
        // 更新对话历史
        if (response.conversation_id) {
          setConversationHistory(prev => [...prev, {
            role: 'user',
            content: description
          }, {
            role: 'assistant',
            content: response.response
          }]);
        }

        if (onAnalysisComplete) {
          onAnalysisComplete(questionResult);
        }
      } else {
        setError('分析失败，请重试');
      }
    } catch (err: any) {
      setError(err?.message || '分析失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const getProviderInfo = (provider: string) => {
    const providerInfo = {
      deepseek: { type: '在线API', color: '#00ff88', description: 'DeepSeek AI服务' },
      siliconflow: { type: '在线API', color: '#ff6b6b', description: '硅基流动AI服务' },
      local: { type: '本地模型', color: '#4ecdc4', description: '本地部署的AI模型' },
      openai_compatible: { type: '兼容API', color: '#45b7d1', description: 'OpenAI兼容API服务' }
    };
    return providerInfo[provider as keyof typeof providerInfo] || { type: '未知', color: '#999', description: '未知AI服务' };
  };

  const containerStyle = {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: 'Arial, sans-serif'
  };

  const cardStyle = {
    backgroundColor: '#1e1e1e',
    borderRadius: '8px',
    padding: '24px',
    marginBottom: '20px',
    border: '1px solid #333'
  };

  const inputStyle = {
    width: '100%',
    padding: '12px',
    border: '1px solid #444',
    borderRadius: '4px',
    backgroundColor: '#2a2a2a',
    color: '#fff',
    fontSize: '14px'
  };

  const buttonStyle = {
    backgroundColor: '#007acc',
    color: 'white',
    padding: '12px 24px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: 'bold'
  };

  const resultStyle = {
    backgroundColor: '#2a2a2a',
    borderRadius: '8px',
    padding: '20px',
    marginTop: '20px',
    border: '1px solid #444'
  };

  const clearConversation = () => {
    setConversationId(null);
    setConversationHistory([]);
    setResult(null);
  };

  return (
    <div className="challenge-analyzer">
      <div className="analyzer-header">
        <h2>CTF题目智能分析</h2>
        <div className="analyzer-controls">
          <div className="control-group">
            <label htmlFor="ai-provider-select">AI模型:</label>
            <select
              id="ai-provider-select"
              value={selectedProvider}
              onChange={(e) => setSelectedProvider(e.target.value)}
              disabled={loading}
            >
              {aiProviders && Object.entries(aiProviders.available_providers).map(([key, provider]) => (
                <option key={key} value={key}>
                  {provider.name} {key === aiProviders.current_provider ? '(默认)' : ''}
                </option>
              ))}
            </select>
          </div>
          
          <div className="control-group">
            <label>
              <input
                type="checkbox"
                checked={useContext}
                onChange={(e) => setUseContext(e.target.checked)}
                disabled={loading}
              />
              使用上下文增强
            </label>
          </div>

          {conversationId && (
            <button
              onClick={clearConversation}
              className="clear-conversation-btn"
              disabled={loading}
            >
              清除对话
            </button>
          )}
        </div>
      </div>

      <div className="analyzer-content">
        <div className="input-section">
          <div className="form-group">
            <label htmlFor="question-type-select">题目类型:</label>
            <select
              id="question-type-select"
              value={questionType}
              onChange={(e) => setQuestionType(e.target.value)}
              disabled={loading}
            >
              <option value="web">Web</option>
              <option value="crypto">Crypto</option>
              <option value="pwn">Pwn</option>
              <option value="reverse">Reverse</option>
              <option value="misc">Misc</option>
            </select>
          </div>

          <div className="form-group">
            <label>题目描述:</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="请输入CTF题目的详细描述..."
              rows={6}
              disabled={loading}
            />
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading || !description.trim()}
            className="analyze-btn"
          >
            {loading ? '分析中...' : '开始分析'}
          </button>
        </div>

        <div className="result-section">
          {conversationId && conversationHistory.length > 0 && (
            <div className="conversation-info">
              <h4>对话历史</h4>
              <div className="conversation-history">
                {conversationHistory.map((msg, index) => (
                  <div key={index} className={`history-message ${msg.role}`}>
                    <strong>{msg.role === 'user' ? '用户' : 'AI'}:</strong>
                    <span>{msg.content.substring(0, 100)}...</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {result && (
            <div className="analysis-result">
              <h4>分析结果</h4>
              <div className="result-content">
                <pre>{result.ai_response}</pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChallengeAnalyzer; 