import React, { useEffect, useState } from 'react';
import { deleteHistoryItem, getHistory } from '../services/api';
import { QuestionResponse } from '../types';

const History: React.FC = () => {
  const [history, setHistory] = useState<QuestionResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const data = await getHistory();
      setHistory(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '加载历史记录失败');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('确定要删除这条记录吗？')) {
      try {
        await deleteHistoryItem(id);
        setHistory(history.filter(item => item.id !== id));
      } catch (err) {
        setError(err instanceof Error ? err.message : '删除失败');
      }
    }
  };

  const handleView = (item: QuestionResponse) => {
    window.alert(`查看详情:\n${item.ai_response}`);
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
    padding: '16px',
    margin: '16px 0',
    boxShadow: '0 2px 4px rgba(0,0,0,0.3)'
  };

  const chipStyle: React.CSSProperties = {
    display: 'inline-block',
    padding: '4px 8px',
    borderRadius: '16px',
    fontSize: '12px',
    fontWeight: 'bold',
    marginBottom: '8px'
  };

  const buttonStyle: React.CSSProperties = {
    padding: '8px 16px',
    margin: '0 4px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px'
  };

  const viewButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    backgroundColor: '#00bcd4',
    color: '#000'
  };

  const deleteButtonStyle: React.CSSProperties = {
    ...buttonStyle,
    backgroundColor: '#f44336',
    color: '#fff'
  };

  if (loading) {
    return (
      <div style={containerStyle}>
        <h2 style={{ marginBottom: '24px' }}>历史记录</h2>
        <div style={{ textAlign: 'center', color: '#666' }}>加载中...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={containerStyle}>
        <h2 style={{ marginBottom: '24px' }}>历史记录</h2>
        <div style={{ backgroundColor: '#f44336', color: '#fff', padding: '12px', borderRadius: '4px' }}>
          {error}
        </div>
      </div>
    );
  }

  return (
    <div style={containerStyle}>
      <h2 style={{ marginBottom: '24px' }}>历史记录</h2>
      
      {history.length === 0 ? (
        <div style={{ textAlign: 'center', color: '#666' }}>
          暂无历史记录
        </div>
      ) : (
        history.map(item => (
          <div key={item.id} style={cardStyle}>
            <span style={{
              ...chipStyle,
              backgroundColor: getTypeColor(item.type),
              color: '#000'
            }}>
              {item.type.toUpperCase()}
            </span>
            
            <p style={{ margin: '8px 0' }}>{item.description}</p>
            
            <small style={{ color: '#999' }}>
              {new Date(item.timestamp).toLocaleString()}
            </small>
            
            <div style={{ marginTop: '12px' }}>
              <button
                style={viewButtonStyle}
                onClick={() => handleView(item)}
              >
                👁️ 查看
              </button>
              
              <button
                style={deleteButtonStyle}
                onClick={() => handleDelete(item.id)}
              >
                🗑️ 删除
              </button>
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default History; 