import type { ChunkPreviewProps } from "@/types/preview";


export default function ChunkPreview({ preview }: ChunkPreviewProps) {
  if (!preview) return null;

  return (
    <div className="border p-4 rounded-md bg-gray-50 max-w-2xl mx-auto mt-4">
      <h2 className="font-semibold mb-2">Chunk Preview: {preview.filename}</h2>
      <p className="text-sm text-gray-700 mb-3">
        Total chunks: {preview.total_chunks}
      </p>
      <div className="space-y-2 text-gray-800 text-sm">
        {preview.sample_chunks.map((chunk, i) => (
          <p key={i} className="border-b pb-1 mb-2">
            {chunk.slice(0, 200)}...
          </p>
        ))}
      </div>
    </div>
  );
}
