import { useState } from "react";
import QueryForm from "./components/QueryForm";
import AnswerCard from "./components/AnswerCard";
import type { RAGResponse } from "@/types/rag";

/**
 * Main app entry for RAG demo
 */
export default function App() {
  const [result, setResult] = useState<RAGResponse | null>(null);

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 text-gray-800">
      <div className="max-w-4xl mx-auto px-4 py-8 sm:py-12">
        <header className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-3">
            🧠 RAG Playground
          </h1>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Ask questions or index your own text — powered by HuggingFace & Qdrant
          </p>
        </header>

        <main className="space-y-10">
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
            <div className="p-1 bg-gradient-to-r from-blue-500 to-indigo-500">
              <div className="bg-white rounded-xl p-6 sm:p-8">
                <QueryForm onResult={setResult} />
              </div>
            </div>
          </div>

          <div className="transition-all duration-300">
            <AnswerCard result={result} />
          </div>
        </main>

        <footer className="mt-16 pt-8 border-t border-gray-200 text-center">
          <p className="text-gray-500 text-sm">
            Built with ❤️ using FastAPI, LangChain, and React
          </p>
        </footer>
      </div>
    </div>
  );
}
