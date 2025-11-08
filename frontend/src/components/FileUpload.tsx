import { useState } from "react";
import type { FormEvent } from "react";
import axios from "axios";
import type { UploadPreview } from "@/types/preview";

interface FileUploadProps {
  onPreview: (data: UploadPreview) => void;
}

export default function FileUpload({ onPreview }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleUpload(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError("");
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await axios.post<UploadPreview>(
        `${import.meta.env.VITE_API_BASE}/rag/upload`,
        formData
      );
      onPreview(res.data);
    } catch (err: any) {
      setError(`Upload failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="border p-4 rounded-md max-w-xl mx-auto my-6">
      <h2 className="text-lg font-semibold mb-3">Upload PDF or TXT</h2>
      <form onSubmit={handleUpload} className="flex flex-col gap-3">
        <input
          type="file"
          accept=".pdf,.txt"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button
          type="submit"
          disabled={!file || loading}
          className="bg-green-600 text-white px-3 py-2 rounded"
        >
          {loading ? "Uploading..." : "Upload & Preview"}
        </button>
      </form>
      {error && <p className="text-red-600 mt-2">{error}</p>}
    </div>
  );
}
