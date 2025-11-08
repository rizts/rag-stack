import type { UploadPreview } from "@/types/preview";

interface FilePreviewProps {
  preview: UploadPreview | null;
}

export default function FilePreview({ preview }: FilePreviewProps) {
  if (!preview) return null;

  return (
    <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-1 max-w-2xl mx-auto mt-6">
      <div className="bg-white rounded-lg p-5">
        <div className="flex items-center space-x-3 mb-4">
          <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-green-100 text-green-600">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-800">File Preview</h2>
        </div>
        
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="font-medium text-gray-700">Filename:</span>
            <span className="text-gray-900 font-semibold">{preview.filename}</span>
          </div>
          
          <div className="flex justify-between items-center">
            <span className="font-medium text-gray-700">Total Chunks:</span>
            <span className="text-gray-900 font-semibold">{preview.total_chunks}</span>
          </div>
          
          <div className="pt-4">
            <h3 className="font-medium text-gray-700 mb-2">Sample Chunks:</h3>
            <div className="space-y-3">
              {preview.sample_chunks.map((chunk, i) => (
                <div key={i} className="p-3 bg-gray-50 rounded-lg border border-gray-100 text-sm text-gray-600">
                  <p className="truncate" title={chunk}>{chunk.slice(0, 200)}...</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}