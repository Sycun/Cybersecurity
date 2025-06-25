export interface ToolResponse {
  id: number;
  name: string;
  description?: string;
  command?: string;
  category?: string;
}

export interface QuestionResponse {
  id: string;
  description: string;
  type: string;
  ai_response: string;
  recommended_tools: any[];
  file_name?: string;
  timestamp: string;
  ai_provider?: string;
}

export interface StatsResponse {
  total_questions: number;
  type_stats: {
    [key: string]: number;
  };
}

export interface AnalysisRequest {
  text?: string;
  file?: File;
}

export interface AIProvidersResponse {
  current_provider: string;
  available_providers: Record<string, string>;
}

export interface AutoSolveRequest {
  question_id: number;
  solve_method?: string;
  custom_code?: string;
  parameters?: Record<string, any>;
}

export interface AutoSolveResponse {
  id: number;
  question_id: number;
  status: string;
  solve_method?: string;
  generated_code?: string;
  execution_result?: string;
  flag?: string;
  error_message?: string;
  execution_time?: number;
  created_at: string;
  completed_at?: string;
}

export interface SolveTemplateResponse {
  id: number;
  name: string;
  category: string;
  description?: string;
  template_code: string;
  parameters?: Record<string, any>;
  is_active: boolean;
  created_at: string;
}

export interface CodeExecutionRequest {
  code: string;
  language: string;
  input_data?: string;
  timeout?: number;
}

export interface CodeExecutionResponse {
  success: boolean;
  output?: string;
  error?: string;
  execution_time: number;
  memory_usage?: number;
}

export interface AIProvider {
  name: string;
  description: string;
  type: 'cloud' | 'local' | 'local_cloud';
  languages: string[];
  max_tokens: number;
  features: string[];
}

export interface AIProvidersData {
  current_provider: string;
  current_provider_info: AIProvider;
  available_providers: Record<string, AIProvider>;
}

export interface AIProviderInfo {
  name: string;
  type: string;
  status: string;
  description: string;
  config: Record<string, any>;
}

export interface Conversation {
  id: string;
  user_id?: string;
  created_at: string;
  updated_at: string;
  messages: Message[];
  context: Record<string, any>;
  metadata: Record<string, any>;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  metadata: Record<string, any>;
}

export interface ConversationCreateRequest {
  user_id?: string;
  initial_context?: Record<string, any>;
}

export interface MessageRequest {
  role: 'user' | 'assistant';
  content: string;
  metadata?: Record<string, any>;
} 