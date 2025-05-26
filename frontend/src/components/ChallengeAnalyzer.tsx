// 简化的CTF题目分析组件，避免依赖问题
function ChallengeAnalyzer() {
  let description = '';
  let file = null;
  let loading = false;
  let result = null;
  let error = null;

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
    padding: '20px',
    margin: '20px 0',
    boxShadow: '0 2px 4px rgba(0,0,0,0.3)'
  };

  const inputStyle = {
    width: '100%',
    padding: '12px',
    backgroundColor: '#2e2e2e',
    border: '1px solid #555',
    borderRadius: '4px',
    color: '#fff',
    fontSize: '14px',
    fontFamily: 'inherit'
  };

  const buttonStyle = {
    padding: '12px 24px',
    margin: '8px',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: 'bold'
  };

  const primaryButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#00bcd4',
    color: '#000'
  };

  const secondaryButtonStyle = {
    ...buttonStyle,
    backgroundColor: '#333',
    color: '#fff',
    border: '1px solid #555'
  };

  const handleFileChange = (event) => {
    file = event.target.files?.[0] || null;
    updateFileDisplay();
  };

  const updateFileDisplay = () => {
    const fileDisplay = document.getElementById('file-display');
    if (fileDisplay) {
      fileDisplay.textContent = file ? file.name : '上传文件';
    }
  };

  const handleSubmit = async () => {
    const descInput = document.getElementById('description-input') as HTMLTextAreaElement;
    description = descInput ? descInput.value : '';

    if (!description.trim() && !file) {
      showError('请输入题目描述或上传文件');
      return;
    }

    setLoading(true);
    hideError();

    // 模拟API调用
    setTimeout(() => {
      const mockResult = {
        id: 1,
        type: 'web',
        description: description,
        ai_response: `## 题目分析\n\n这是一个${getTypeFromDescription(description)}类型的CTF题目。\n\n### 分析思路\n1. 检查输入验证\n2. 寻找注入点\n3. 构造payload\n\n### 推荐工具\n- Burp Suite\n- SQLMap\n- Dirb`,
        recommended_tools: [
          { id: 1, name: 'Burp Suite', description: 'Web应用安全测试工具', command_template: 'burpsuite' },
          { id: 2, name: 'SQLMap', description: 'SQL注入检测工具', command_template: 'sqlmap -u "URL"' }
        ],
        timestamp: new Date().toISOString()
      };
      
      setResult(mockResult);
      setLoading(false);
    }, 2000);
  };

  const getTypeFromDescription = (desc) => {
    const lower = desc.toLowerCase();
    if (lower.includes('sql') || lower.includes('web') || lower.includes('xss')) return 'web';
    if (lower.includes('pwn') || lower.includes('buffer') || lower.includes('overflow')) return 'pwn';
    if (lower.includes('reverse') || lower.includes('逆向')) return 'reverse';
    if (lower.includes('crypto') || lower.includes('密码') || lower.includes('rsa')) return 'crypto';
    return 'misc';
  };

  const setLoading = (isLoading) => {
    loading = isLoading;
    const submitBtn = document.getElementById('submit-btn') as HTMLButtonElement;
    if (submitBtn) {
      submitBtn.disabled = isLoading;
      submitBtn.textContent = isLoading ? '分析中...' : '开始分析';
    }
  };

  const setResult = (newResult) => {
    result = newResult;
    displayResult();
  };

  const showError = (message) => {
    error = message;
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
      errorDiv.textContent = message;
      errorDiv.style.display = 'block';
    }
  };

  const hideError = () => {
    error = null;
    const errorDiv = document.getElementById('error-message');
    if (errorDiv) {
      errorDiv.style.display = 'none';
    }
  };

  const displayResult = () => {
    const resultDiv = document.getElementById('result-container');
    if (!resultDiv || !result) return;

    resultDiv.innerHTML = `
      <div style="background-color: #1e1e1e; border: 1px solid #333; border-radius: 8px; padding: 20px; margin: 20px 0;">
        <h3>分析结果</h3>
        <div style="margin: 16px 0;">
          <span style="background-color: #00bcd4; color: #000; padding: 4px 8px; border-radius: 16px; font-size: 12px; font-weight: bold;">
            ${result.type.toUpperCase()}
          </span>
        </div>
        <p><strong>分析时间:</strong> ${new Date(result.timestamp).toLocaleString()}</p>
        
        <h4>推荐工具</h4>
        ${result.recommended_tools.map(tool => `
          <div style="background-color: #2e2e2e; padding: 12px; margin: 8px 0; border-radius: 4px;">
            <strong>${tool.name}</strong><br>
            <small style="color: #999;">${tool.description}</small><br>
            <code style="background-color: #333; padding: 4px; border-radius: 2px; font-family: monospace;">
              ${tool.command_template}
            </code>
          </div>
        `).join('')}
        
        <h4>AI分析结果</h4>
        <div style="background-color: #2e2e2e; padding: 16px; border-radius: 4px; white-space: pre-line;">
          ${result.ai_response}
        </div>
      </div>
    `;
    resultDiv.style.display = 'block';
  };

  // 创建DOM元素
  const container = document.createElement('div');
  Object.assign(container.style, containerStyle);

  container.innerHTML = `
    <h2 style="margin-bottom: 24px;">CTF题目智能分析</h2>
    
    <div style="background-color: #1e1e1e; border: 1px solid #333; border-radius: 8px; padding: 20px; margin: 20px 0;">
      <div style="margin-bottom: 16px;">
        <label style="display: block; margin-bottom: 8px; font-weight: bold;">题目描述</label>
        <textarea 
          id="description-input"
          placeholder="请输入CTF题目的描述、提示信息或相关代码..."
          rows="6"
          style="width: 100%; padding: 12px; background-color: #2e2e2e; border: 1px solid #555; border-radius: 4px; color: #fff; font-family: inherit; resize: vertical;"
        ></textarea>
      </div>
      
      <div style="display: flex; gap: 16px; margin-bottom: 16px;">
        <label style="flex: 1; cursor: pointer;">
          <div id="file-display" style="padding: 12px; background-color: #333; border: 1px solid #555; border-radius: 4px; text-align: center; color: #fff;">
            上传文件
          </div>
          <input 
            type="file" 
            style="display: none;" 
            accept=".txt,.py,.c,.cpp,.js,.php,.html,.pcap,.zip,.exe,.elf,.bin"
            onchange="handleFileChange(event)"
          />
        </label>
        
        <button 
          id="submit-btn"
          onclick="handleSubmit()"
          style="flex: 1; padding: 12px 24px; background-color: #00bcd4; color: #000; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: bold;"
        >
          开始分析
        </button>
      </div>
      
      <div 
        id="error-message" 
        style="display: none; background-color: #f44336; color: #fff; padding: 12px; border-radius: 4px; margin-top: 16px;"
      ></div>
    </div>
    
    <div id="result-container" style="display: none;"></div>
  `;

  // 绑定事件处理函数到全局
  (window as any).handleFileChange = handleFileChange;
  (window as any).handleSubmit = handleSubmit;

  return container;
}

export default ChallengeAnalyzer; 