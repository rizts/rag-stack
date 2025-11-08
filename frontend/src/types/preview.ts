export interface UploadPreview {
  filename: string;
  total_chunks: number;
  sample_chunks: string[];
}

export interface ChunkPreviewProps {
  preview: UploadPreview | null;
}