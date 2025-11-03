import type { RAGResponse } from "@/types/rag";

interface AnswerCardProps {
  result: RAGResponse | null;
}

/**
 * AnswerCard displays AI response and context used.
 */
export default function AnswerCard({ result }: AnswerCardProps) {
  if (!result) return null;

  return (
    <div className="w-full">
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-1">
        <div className="bg-white rounded-lg p-6">
          <div className="flex items-center space-x-3 mb-4">
            <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-blue-100 text-blue-600">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-gray-800">Answer</h2>
          </div>
          
          <div className="prose prose-blue max-w-none">
            <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
              {result.answer || "No answer provided"}
            </p>
          </div>

          {result.context_used && result.context_used.length > 0 && (
            <div className="mt-6 pt-6 border-t border-gray-100">
              <h3 className="flex items-center text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Context used
              </h3>
              <div className="space-y-2">
                {result.context_used.map((c: string, i: number) => (
                  <div key={i} className="p-3 bg-gray-50 rounded-lg border border-gray-100 text-sm text-gray-600">
                    <p className="truncate" title={c}>{c}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
