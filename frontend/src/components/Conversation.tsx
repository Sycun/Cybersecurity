import React, { useEffect, useRef, useState } from 'react';
import {
    addMessage,
    analyzeChallenge,
    createConversation,
    deleteConversation,
    getAIProviders,
    getConversation,
    getUserConversations
} from '../services/api';
import { AIProviderInfo, Conversation } from '../types';
import './Conversation.css';

interface ConversationProps {
  userId?: string;
}

const ConversationComponent: React.FC<ConversationProps> = ({ userId }) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversation, setCurrentConversation] = useState<Conversation | null>(null);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [aiProviders, setAiProviders] = useState<AIProviderInfo[]>([]);
  const [selectedProvider, setSelectedProvider] = useState<string>('');
  const [useContext, setUseContext] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadConversations();
    loadAIProviders();
  }, [userId]);

  useEffect(() => {
    scrollToBottom();
  }, [currentConversation?.messages]);

  const loadConversations = async () => {
    if (!userId) return;
    try {
      const userConversations = await getUserConversations(userId);
      setConversations(userConversations);
    } catch (error) {
      console.error('加载对话列表失败:', error);
    }
  };

  const loadAIProviders = async () => {
    try {
      const providers = await getAIProviders();
      setAiProviders(providers);
      if (providers.length > 0) {
        setSelectedProvider(providers[0].type);
      }
    } catch (error) {
      console.error('加载AI提供者失败:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const createNewConversation = async () => {
    try {
      const conversationId = await createConversation(userId, {
        question_type: 'general',
        created_at: new Date().toISOString()
      });
      
      if (conversationId) {
        await loadConversations();
        await selectConversation(conversationId);
      }
    } catch (error) {
      console.error('创建对话失败:', error);
    }
  };

  const selectConversation = async (conversationId: string) => {
    try {
      const conversation = await getConversation(conversationId);
      if (conversation) {
        setCurrentConversation(conversation);
      }
    } catch (error) {
      console.error('获取对话失败:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || !currentConversation) return;

    setIsLoading(true);
    try {
      // 添加用户消息到对话
      await addMessage(
        currentConversation.id,
        'user',
        inputMessage,
        {
          question_type: 'general',
          ai_provider: selectedProvider
        }
      );

      // 调用AI分析
      const response = await analyzeChallenge({
        description: inputMessage,
        question_type: 'general',
        ai_provider: selectedProvider,
        user_id: userId,
        conversation_id: currentConversation.id,
        use_context: useContext
      });

      // 添加AI响应到对话
      if (response.conversation_id) {
        await addMessage(
          response.conversation_id,
          'assistant',
          response.response,
          { ai_provider: response.ai_provider }
        );

        // 重新加载当前对话
        await selectConversation(response.conversation_id);
      }

      setInputMessage('');
    } catch (error) {
      console.error('发送消息失败:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const deleteConversationHandler = async (conversationId: string) => {
    try {
      await deleteConversation(conversationId);
      await loadConversations();
      
      if (currentConversation?.id === conversationId) {
        setCurrentConversation(null);
      }
    } catch (error) {
      console.error('删除对话失败:', error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString('zh-CN');
  };

  return (
    <div className="conversation-container">
      <div className="conversation-sidebar">
        <div className="sidebar-header">
          <h3>对话列表</h3>
          <button 
            className="new-conversation-btn"
            onClick={createNewConversation}
          >
            新建对话
          </button>
        </div>
        
        <div className="conversation-list">
          {conversations.map((conversation) => (
            <div
              key={conversation.id}
              className={`conversation-item ${
                currentConversation?.id === conversation.id ? 'active' : ''
              }`}
              onClick={() => selectConversation(conversation.id)}
            >
              <div className="conversation-title">
                {conversation.messages.length > 0 
                  ? conversation.messages[0].content.substring(0, 30) + '...'
                  : '新对话'
                }
              </div>
              <div className="conversation-meta">
                <span>{formatTimestamp(conversation.updated_at)}</span>
                <button
                  className="delete-btn"
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteConversationHandler(conversation.id);
                  }}
                >
                  删除
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="conversation-main">
        {currentConversation ? (
          <>
            <div className="conversation-header">
              <h3>对话详情</h3>
              <div className="conversation-controls">
                <select
                  value={selectedProvider}
                  onChange={(e) => setSelectedProvider(e.target.value)}
                  className="provider-select"
                >
                  {aiProviders.map((provider) => (
                    <option key={provider.type} value={provider.type}>
                      {provider.name}
                    </option>
                  ))}
                </select>
                <label className="context-toggle">
                  <input
                    type="checkbox"
                    checked={useContext}
                    onChange={(e) => setUseContext(e.target.checked)}
                  />
                  使用上下文
                </label>
              </div>
            </div>

            <div className="messages-container">
              {currentConversation.messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.role === 'user' ? 'user' : 'assistant'}`}
                >
                  <div className="message-header">
                    <span className="message-role">
                      {message.role === 'user' ? '用户' : 'AI助手'}
                    </span>
                    <span className="message-time">
                      {formatTimestamp(message.timestamp)}
                    </span>
                  </div>
                  <div className="message-content">
                    {message.content}
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            <div className="message-input">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="输入您的问题..."
                disabled={isLoading}
                rows={3}
              />
              <button
                onClick={sendMessage}
                disabled={isLoading || !inputMessage.trim()}
                className="send-btn"
              >
                {isLoading ? '发送中...' : '发送'}
              </button>
            </div>
          </>
        ) : (
          <div className="no-conversation">
            <h3>选择或创建一个对话开始聊天</h3>
            <p>AI助手将记住对话历史，提供更精准的分析</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ConversationComponent; 