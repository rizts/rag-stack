import { useState } from "react";
import type { FormEvent } from "react";
import { queryRAG, indexDocument } from "../api/rag";
import type { RAGResponse } from "@/types/rag";

interface QueryFormProps {
  onResult: (res: RAGResponse) => void;
}

/**
 * QueryForm allows user to either ask questions or index new text.
 */
export default function QueryForm({ onResult }: QueryFormProps) {
  const [mode, setMode] = useState<"query" | "index">("query");
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const result =
        mode === "query" ? await queryRAG(input) : await indexDocument(input);
      onResult(result);
    } catch (err: any) {
      console.error(err);
      alert("Error: " + (err.message || "Unknown error"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-700">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
            </svg>
          </span>
          <h3 className="font-medium text-gray-800">Query Settings</h3>
        </div>
        <div className="flex items-center space-x-2">
          <label className="text-sm font-medium text-gray-600">Mode:</label>
          <select
            value={mode}
            onChange={(e) => setMode(e.target.value as "query" | "index")}
            className="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
          >
            <option value="query">Ask</option>
            <option value="index">Index</option>
          </select>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={
            mode === "query"
              ? "🔍 Ask something about your indexed data..."
              : "📄 Paste or write content to index..."
          }
          className="w-full border border-gray-300 rounded-lg p-4 h-36 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition resize-none shadow-sm"
        />

        <button
          type="submit"
          disabled={loading || !input}
          className={`w-full py-3 px-4 rounded-lg text-white font-medium transition ${
            loading || !input
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700 active:bg-blue-800"
          } shadow-sm`}
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processing...
            </span>
          ) : mode === "query" ? (
            "Ask Question"
          ) : (
            "Index Content"
          )}
        </button>
      </form>
    </div>
  );
}
