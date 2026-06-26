"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { RadialBarChart, RadialBar, ResponsiveContainer } from "recharts";
import { ArrowLeft, AlertTriangle, CheckCircle, Info, XCircle, ExternalLink } from "lucide-react";
import ExportButton from "../components/AuditReport";

const severityConfig: Record<string, { color: string; icon: React.ReactNode }> = {
  critical: { color: "text-red-400 bg-red-400/10 border-red-400/20", icon: <XCircle className="w-4 h-4 text-red-400" /> },
  high: { color: "text-orange-400 bg-orange-400/10 border-orange-400/20", icon: <AlertTriangle className="w-4 h-4 text-orange-400" /> },
  medium: { color: "text-yellow-400 bg-yellow-400/10 border-yellow-400/20", icon: <Info className="w-4 h-4 text-yellow-400" /> },
  low: { color: "text-green-400 bg-green-400/10 border-green-400/20", icon: <CheckCircle className="w-4 h-4 text-green-400" /> },
};

function ScoreRing({ score, label, color }: { score: number; label: string; color: string }) {
  const data = [{ value: score, fill: color }, { value: 100 - score, fill: "transparent" }];
  return (
    <div className="flex flex-col items-center">
      <div className="relative w-28 h-28">
        <ResponsiveContainer width="100%" height="100%">
          <RadialBarChart cx="50%" cy="50%" innerRadius="70%" outerRadius="100%" data={data} startAngle={90} endAngle={-270}>
            <RadialBar dataKey="value" cornerRadius={10} background={{ fill: "#ffffff10" }} />
          </RadialBarChart>
        </ResponsiveContainer>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-2xl font-bold text-white">{score}</span>
        </div>
      </div>
      <p className="text-gray-400 text-sm mt-2">{label}</p>
    </div>
  );
}

function ScoreBadge({ score }: { score: number }) {
  if (score >= 80) return <span className="text-green-400 text-sm font-semibold">Good</span>;
  if (score >= 60) return <span className="text-yellow-400 text-sm font-semibold">Needs Work</span>;
  return <span className="text-red-400 text-sm font-semibold">Poor</span>;
}

export default function Results() {
  const [report, setReport] = useState<any>(null);
  const [tab, setTab] = useState<"ux" | "accessibility">("ux");
  const router = useRouter();

  useEffect(() => {
    const stored = localStorage.getItem("auditReport");
    if (stored) setReport(JSON.parse(stored));
    else router.push("/");
  }, [router]);

  if (!report) return (
    <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center">
      <p className="text-gray-400">Loading report...</p>
    </div>
  );

  return (
    <main className="min-h-screen bg-[#0a0a0f] text-white px-4 py-10">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <button onClick={() => router.push("/")} className="flex items-center gap-2 text-gray-400 hover:text-white transition">
            <ArrowLeft className="w-4 h-4" /> New Audit
          </button>
          <ExportButton report={report} />
        </div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="bg-white/5 border border-white/10 rounded-2xl p-6 mb-6">
            <p className="text-gray-400 text-sm mb-1">Audit Report for</p>
            <div className="flex items-center gap-2">
              <p className="text-violet-400 font-semibold text-lg break-all">{report.url}</p>
              <a href={report.url} target="_blank" rel="noopener noreferrer">
                <ExternalLink className="w-4 h-4 text-gray-500 hover:text-violet-400 transition" />
              </a>
            </div>
          </div>

          <div className="bg-white/5 border border-white/10 rounded-2xl p-6 mb-6">
            <h2 className="text-lg font-semibold mb-6 text-center">Scores</h2>
            <div className="flex justify-around flex-wrap gap-6">
              <div className="flex flex-col items-center gap-1">
                <ScoreRing score={report.overall_score} label="Overall" color="#8b5cf6" />
                <ScoreBadge score={report.overall_score} />
              </div>
              <div className="flex flex-col items-center gap-1">
                <ScoreRing score={report.ux_score} label="UX" color="#06b6d4" />
                <ScoreBadge score={report.ux_score} />
              </div>
              <div className="flex flex-col items-center gap-1">
                <ScoreRing score={report.accessibility_score} label="Accessibility" color="#10b981" />
                <ScoreBadge score={report.accessibility_score} />
              </div>
            </div>
          </div>

          <div className="bg-white/5 border border-white/10 rounded-2xl p-6 mb-6">
            <h2 className="text-lg font-semibold mb-3">Summary</h2>
            <p className="text-gray-300 leading-relaxed">{report.summary}</p>
          </div>

          <div className="bg-white/5 border border-white/10 rounded-2xl p-6 mb-6">
            <h2 className="text-lg font-semibold mb-4">Top 5 Fixes</h2>
            <div className="space-y-3">
              {report.top_fixes.map((fix: string, i: number) => (
                <div key={i} className="flex items-start gap-3">
                  <span className="bg-violet-600/20 text-violet-400 border border-violet-500/30 rounded-lg w-7 h-7 flex items-center justify-center text-sm font-bold shrink-0">{i + 1}</span>
                  <p className="text-gray-300 text-sm pt-1">{fix}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white/5 border border-white/10 rounded-2xl p-6">
            <div className="flex gap-3 mb-6 flex-wrap">
              {(["ux", "accessibility"] as const).map((t) => (
                <button key={t} onClick={() => setTab(t)}
                  className={`px-4 py-2 rounded-lg text-sm font-semibold transition ${tab === t ? "bg-violet-600 text-white" : "text-gray-400 hover:text-white"}`}>
                  {t === "ux" ? `UX Issues (${report.ux_issues.length})` : `Accessibility Issues (${report.accessibility_issues.length})`}
                </button>
              ))}
            </div>

            <div className="space-y-3">
              {(tab === "ux" ? report.ux_issues : report.accessibility_issues).map((issue: any, i: number) => {
                const config = severityConfig[issue.severity] || severityConfig.low;
                return (
                  <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
                    className={`border rounded-xl p-4 ${config.color}`}>
                    <div className="flex items-start gap-3">
                      <div className="mt-0.5 shrink-0">{config.icon}</div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1 flex-wrap">
                          <span className="font-semibold text-sm">{issue.category || issue.rule}</span>
                          <span className={`text-xs px-2 py-0.5 rounded-full border ${config.color}`}>{issue.severity}</span>
                        </div>
                        <p className="text-sm opacity-80 mb-2">{issue.issue || issue.element}</p>
                        <p className="text-xs opacity-60">Fix: {issue.fix}</p>
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </div>
        </motion.div>
      </div>
    </main>
  );
}
