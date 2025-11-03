import axios from "axios";
import type { RAGResponse } from "@/types/rag";

const API_BASE =
  import.meta.env.VITE_API_BASE || "http://localhost:8000";

/**
 * Send text content to backend for embedding & indexing
 */
export async function indexDocument(content: string): Promise<RAGResponse> {
  const formData = new FormData();
  formData.append("content", content);
  const res = await axios.post(`${API_BASE}/rag/index`, formData);
  return res.data;
}

/**
 * Query the RAG pipeline and receive the generated answer
 */
export async function queryRAG(query: string): Promise<RAGResponse> {
  const formData = new FormData();
  formData.append("query", query);
  const res = await axios.post(`${API_BASE}/rag/query`, formData);
  return res.data;
}
