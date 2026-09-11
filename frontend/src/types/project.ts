import { z } from 'zod';

export const projectSchema = z.object({
  name: z.string().min(2, "Project name must be at least 2 characters"),
  description: z.string().optional(),
  framework: z.enum(["PyTorch", "TensorFlow", "Ultralytics YOLO"]),
  model_name: z.string().min(1, "Model name is required"),
  dataset_path: z.string().min(1, "Dataset path is required"),
  training_script_path: z.string().min(1, "Training script path is required"),
  output_dir: z.string().min(1, "Output directory is required"),
  checkpoint_dir: z.string().min(1, "Checkpoint directory is required"),
  automation_enabled: z.boolean().default(true),
});

export type ProjectFormData = z.infer<typeof projectSchema>;

export interface Project extends ProjectFormData {
  id: string;
  created_at: string;
  updated_at: string;
}

export interface AppSettings {
  theme: string;
  app_env: string;
  default_output_folder: string;
  default_checkpoint_folder: string;
  postgres_server: string;
  postgres_port: string;
  postgres_db: string;
}
