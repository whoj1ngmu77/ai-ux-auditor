"use client";
import jsPDF from "jspdf";
import { Download } from "lucide-react";

export default function ExportButton({ report }: { report: any }) {
  const handleExport = () => {
    const pdf = new jsPDF("p", "mm", "a4");
    const pageWidth = pdf.internal.pageSize.getWidth();
    const margin = 20;
    const maxWidth = pageWidth - margin * 2;
    let y = 20;

    const addText = (text: string, size: number, bold = false, color: [number, number, number] = [255, 255, 255]) => {
      pdf.setFontSize(size);
      pdf.setFont("helvetica", bold ? "bold" : "normal");
      pdf.setTextColor(...color);
      const lines = pdf.splitTextToSize(text, maxWidth);
      lines.forEach((line: string) => {
        if (y > 270) { pdf.addPage(); y = 20; }
        pdf.text(line, margin, y);
        y += size * 0.5;
      });
      y += 3;
    };

    const addRect = (color: [number, number, number]) => {
      pdf.setFillColor(...color);
      pdf.rect(margin, y, maxWidth, 0.3, "F");
      y += 6;
    };

    pdf.setFillColor(10, 10, 15);
    pdf.rect(0, 0, pageWidth, 297, "F");

    addText("AI UX Auditor", 24, true, [139, 92, 246]);
    addText(`Report for: ${report.url}`, 11, false, [150, 150, 180]);
    addText(new Date().toLocaleDateString(), 9, false, [100, 100, 130]);
    y += 4;
    addRect([60, 60, 80]);

    addText("SCORES", 13, true, [139, 92, 246]);
    addText(`Overall Score: ${report.overall_score}/100`, 11, false, [200, 200, 220]);
    addText(`UX Score: ${report.ux_score}/100`, 11, false, [6, 182, 212]);
    addText(`Accessibility Score: ${report.accessibility_score}/100`, 11, false, [16, 185, 129]);
    y += 4;
    addRect([60, 60, 80]);

    addText("SUMMARY", 13, true, [139, 92, 246]);
    addText(report.summary, 10, false, [180, 180, 200]);
    y += 4;
    addRect([60, 60, 80]);

    addText("TOP 5 FIXES", 13, true, [139, 92, 246]);
    report.top_fixes.forEach((fix: string, i: number) => {
      addText(`${i + 1}. ${fix}`, 10, false, [180, 180, 200]);
    });
    y += 4;
    addRect([60, 60, 80]);

    addText("UX ISSUES", 13, true, [139, 92, 246]);
    report.ux_issues.forEach((issue: any) => {
      if (y > 260) { pdf.addPage(); pdf.setFillColor(10, 10, 15); pdf.rect(0, 0, pageWidth, 297, "F"); y = 20; }
      const severityColor: Record<string, [number, number, number]> = {
        critical: [248, 113, 113],
        high: [251, 146, 60],
        medium: [250, 204, 21],
        low: [74, 222, 128],
      };
      addText(`[${issue.severity.toUpperCase()}] ${issue.category}`, 10, true, severityColor[issue.severity] || [180, 180, 200]);
      addText(issue.issue, 9, false, [180, 180, 200]);
      addText(`Fix: ${issue.fix}`, 9, false, [120, 120, 150]);
      y += 2;
    });
    y += 4;
    addRect([60, 60, 80]);

    addText("ACCESSIBILITY ISSUES", 13, true, [139, 92, 246]);
    report.accessibility_issues.forEach((issue: any) => {
      if (y > 260) { pdf.addPage(); pdf.setFillColor(10, 10, 15); pdf.rect(0, 0, pageWidth, 297, "F"); y = 20; }
      const severityColor: Record<string, [number, number, number]> = {
        critical: [248, 113, 113],
        high: [251, 146, 60],
        medium: [250, 204, 21],
        low: [74, 222, 128],
      };
      addText(`[${issue.severity.toUpperCase()}] ${issue.rule}`, 10, true, severityColor[issue.severity] || [180, 180, 200]);
      addText(issue.element.substring(0, 80), 9, false, [180, 180, 200]);
      addText(`Fix: ${issue.fix}`, 9, false, [120, 120, 150]);
      y += 2;
    });

    pdf.save("ux-audit-report.pdf");
  };

  return (
    <button
      onClick={handleExport}
      className="flex items-center gap-2 bg-violet-600 hover:bg-violet-500 px-5 py-3 rounded-xl font-semibold text-sm transition"
    >
      <Download className="w-4 h-4" />
      Export PDF
    </button>
  );
}
