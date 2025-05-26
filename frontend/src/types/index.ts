export interface ToolResponse {
  id: number;
  name: string;
  description?: string;
  command_template?: string;
  category?: string;
}

export interface QuestionResponse {
  id: number;
  description: string;
  type: string;
  ai_response?: string;
  recommended_tools: ToolResponse[];
  timestamp: string;
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