export interface Project {
  id: string;
  name: string;
  description?: string;
  framework: 'PyTorch' | 'TensorFlow' | 'Ultralytics YOLO';
  model_name: string;
  dataset_path: string;
  training_script_path: string;
  output_dir: string;
  checkpoint_dir: string;
  created_at: string;
  updated_at: string;
}

export interface TrainingSession {
  id: string;
  project_id: string;
  session_name: string;
  status: 'INITIALIZING' | 'RUNNING' | 'PAUSED' | 'COMPLETED' | 'FAILED' | 'CANCELLED';
  pid?: number;
  start_time?: string;
  end_time?: string;
  exit_code?: number;
  hyperparameters: Record<string, any>;
  created_at: string;
}

export interface SystemTelemetry {
  cpu_utilization_pct: number;
  ram_used_bytes: number;
  ram_total_bytes: number;
  gpu_utilization_pct?: number;
  gpu_memory_used_mb?: number;
  gpu_memory_total_mb?: number;
  gpu_temperature_c?: number;
  gpu_power_draw_watts?: number;
  disk_free_space_bytes: number;
  timestamp: string;
}

export interface Metric {
  epoch: number;
  step: number;
  loss?: number;
  val_loss?: number;
  accuracy?: number;
  learning_rate?: number;
  timestamp: string;
}

export interface AutomationRule {
  id: string;
  project_id?: string;
  name: string;
  trigger_event: 'ON_SUCCESS' | 'ON_FAILED' | 'ON_OVERHEATING' | 'ON_NAN';
  actions_sequence: Array<{
    action_type: string;
    params: Record<string, any>;
  }>;
  is_active: boolean;
  created_at: string;
}
