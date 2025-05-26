// 简化的历史记录组件，避免依赖问题
function History() {
  // 模拟数据
  const mockHistory = [
    {
      id: 1,
      type: 'web',
      description: 'SQL注入漏洞分析',
      timestamp: new Date().toISOString(),
      ai_response: '这是一个典型的SQL注入漏洞...'
    },
    {
      id: 2,
      type: 'pwn',
      description: '缓冲区溢出利用',
      timestamp: new Date().toISOString(),
      ai_response: '缓冲区溢出是一种常见的二进制漏洞...'
    }
  ];

  const containerStyle = {
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
    color: '#fff',
    backgroundColor: '#121212'
  };

  const cardStyle = {
    backgroundColor: '#1e1e1e',
    border: '1px solid #333',
    borderRadius: '8px',
    padding: '16px',
    margin: '16px 0',
    boxShadow: '0 2px 4px rgba(0,0,0,0.3)'
  };

  const chipStyle = {
    display: 'inline-block',
    padding: '4px 8px',
    borderRadius: '16px',
    fontSize: '12px',
    fontWeight: 'bold',
    marginBottom: '8px'
  };

  const getTypeColor = (type) => {
    const colors = {
      web: '#2196f3',
      pwn: '#f44336',
      reverse: '#ff9800',
      crypto: '#00bcd4',
      misc: '#4caf50'
    };
    return colors[type] || '#9e9e9e';
  };

  const buttonStyle = {
    padding: '8px 16px',
    margin: '0 4px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px'
  };

  const viewButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#00bcd4',
    color: '#000'
  };

  const deleteButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#f44336',
    color: '#fff'
  };

  // 创建DOM元素
  const container = document.createElement('div');
  Object.assign(container.style, containerStyle);

  const title = document.createElement('h2');
  title.textContent = '历史记录';
  title.style.marginBottom = '24px';
  container.appendChild(title);

  if (mockHistory.length === 0) {
    const emptyMessage = document.createElement('div');
    emptyMessage.textContent = '暂无历史记录';
    emptyMessage.style.textAlign = 'center';
    emptyMessage.style.color = '#666';
    container.appendChild(emptyMessage);
  } else {
    mockHistory.forEach(item => {
      const card = document.createElement('div');
      Object.assign(card.style, cardStyle);

      const chip = document.createElement('span');
      chip.textContent = item.type.toUpperCase();
      Object.assign(chip.style, {
        ...chipStyle,
        backgroundColor: getTypeColor(item.type),
        color: '#000'
      });
      card.appendChild(chip);

      const description = document.createElement('p');
      description.textContent = item.description;
      description.style.margin = '8px 0';
      card.appendChild(description);

      const timestamp = document.createElement('small');
      timestamp.textContent = new Date(item.timestamp).toLocaleString();
      timestamp.style.color = '#999';
      card.appendChild(timestamp);

      const buttonContainer = document.createElement('div');
      buttonContainer.style.marginTop = '12px';

      const viewButton = document.createElement('button');
      viewButton.textContent = '👁️ 查看';
      Object.assign(viewButton.style, viewButtonStyle);
      viewButton.onclick = () => alert(`查看详情:\n${item.ai_response}`);
      buttonContainer.appendChild(viewButton);

      const deleteButton = document.createElement('button');
      deleteButton.textContent = '🗑️ 删除';
      Object.assign(deleteButton.style, deleteButtonStyle);
      deleteButton.onclick = () => {
        if (confirm('确定要删除这条记录吗？')) {
          card.remove();
        }
      };
      buttonContainer.appendChild(deleteButton);

      card.appendChild(buttonContainer);
      container.appendChild(card);
    });
  }

  return container;
}

export default History; 