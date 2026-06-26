"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Search, Zap, Eye, Shield } from "lucide-react";

export default function Home() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const handleAudit = async () => {
    if (!url) return;
    setError("");
    setLoading(true);
    try {
      let auditUrl = url;
      if (!auditUrl.startsWith("http")) auditUrl = "https://" + auditUrl;
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 120000);
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/audit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: auditUrl }),
        signal: controller.signal,
      });
      clearTimeout(timeoutId);
      const data = await res.json();
      if (data.status === "success") {
        localStorage.setItem("auditReport", JSON.stringify(data.report));
        router.push("/results");
      } else {
        setError("Audit failed. Please try another URL.");
      }
    } catch (e: any) {
      if (e.name === "AbortError") {
        setError("Request timed out. The site may be too heavy. Try again.");
      } else {
        setError("Something went wrong. Make sure the backend is running.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#0a0a0f] text-white flex flex-col items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center max-w-2xl w-full"
      >
        <div className="flex justify-center mb-6">
          <div className="bg-violet-600/20 border border-violet-500/30 rounded-2xl p-4">
            <Eye className="w-10 h-10 text-violet-400" />
          </div>
        </div>

        <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-violet-400 to-cyan-400 bg-clip-text text-transparent">
          AI UX Auditor
        </h1>
        <p className="text-gray-400 text-lg mb-10">
          Paste any website URL and get an instant AI-powered UX & accessibility audit report
        </p>

        <div className="flex gap-3 mb-4">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAudit()}
            placeholder="https://yourwebsite.com"
            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-5 py-4 text-white placeholder-gray-500 focus:outline-none focus:border-violet-500 transition"
          />
          <button
            onClick={handleAudit}
            disabled={loading || !url}
            className="bg-violet-600 hover:bg-violet-500 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-4 rounded-xl font-semibold flex items-center gap-2 transition"
          >
            <Search className="w-5 h-5" />
            {loading ? "Auditing..." : "Audit"}
          </button>
        </div>

        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="bg-white/5 border border-white/10 rounded-xl p-6 mb-6"
          >
            <div className="flex items-center gap-3 mb-3">
              <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce" />
              <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce delay-100" />
              <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce delay-200" />
              <span className="text-gray-400 text-sm">AI agents are analyzing your site...</span>
            </div>
            <div className="text-xs text-gray-500 space-y-1 text-left">
              <p>🌐 Browser agent crawling the site...</p>
              <p>👁️ Visual UX analyst reviewing screenshots...</p>
              <p>♿ Accessibility checker scanning HTML...</p>
              <p>📋 Report generator synthesizing findings...</p>
              <p className="text-yellow-500/70 mt-2">⏳ Complex sites may take up to 2 minutes...</p>
            </div>
          </motion.div>
        )}

        <div className="grid grid-cols-3 gap-4 mt-8">
          {[
            { icon: <Eye className="w-5 h-5 text-violet-400" />, label: "UX Analysis", desc: "Visual design & flow" },
            { icon: <Shield className="w-5 h-5 text-cyan-400" />, label: "Accessibility", desc: "WCAG compliance check" },
            { icon: <Zap className="w-5 h-5 text-yellow-400" />, label: "Instant Report", desc: "Scores & actionable fixes" },
          ].map((item, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + i * 0.1 }}
              className="bg-white/5 border border-white/10 rounded-xl p-4 text-center"
            >
              <div className="flex justify-center mb-2">{item.icon}</div>
              <p className="font-semibold text-sm">{item.label}</p>
              <p className="text-gray-500 text-xs mt-1">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </main>
  );
}
