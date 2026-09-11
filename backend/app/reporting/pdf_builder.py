import os
import csv
import logging
from typing import List, Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

logger = logging.getLogger(__name__)

class PDFReportGenerator:
    @staticmethod
    def generate_pdf(
        output_filepath: str,
        session_info: Dict[str, Any],
        metrics_summary: Dict[str, Any],
        hardware_summary: Dict[str, Any],
        recommendations: List[Dict[str, Any]]
    ) -> str:
        doc = SimpleDocTemplate(output_filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor("#1e293b"),
            spaceAfter=12
        )

        subtitle_style = ParagraphStyle(
            'SubtitleStyle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = styles['BodyText']

        # Header
        story.append(Paragraph("Zombie Run Cost Killer - Training Performance Report", title_style))
        story.append(Paragraph(f"Project Name: <b>{session_info.get('project_name', 'N/A')}</b>", body_style))
        story.append(Paragraph(f"Session ID: <b>{session_info.get('session_id', 'N/A')}</b> | Status: <b>{session_info.get('status', 'N/A')}</b>", body_style))
        story.append(Spacer(1, 12))

        # Metrics Summary Table
        story.append(Paragraph("Training Performance Summary", subtitle_style))
        table_data = [
            ["Metric", "Value"],
            ["Total Epochs", str(metrics_summary.get("total_epochs", 0))],
            ["Final Loss", f"{metrics_summary.get('final_loss', 0.0):.4f}"],
            ["Best Validation Loss", f"{metrics_summary.get('best_val_loss', 0.0):.4f}"],
            ["Final Accuracy", f"{metrics_summary.get('final_accuracy', 0.0)*100:.2f}%" if metrics_summary.get('final_accuracy') else "N/A"],
            ["Total Training Duration", f"{session_info.get('duration_sec', 0)/60.0:.1f} minutes"]
        ]
        t = Table(table_data, colWidths=[200, 250])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (1,0), colors.HexColor('#0f172a')),
            ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ]))
        story.append(t)
        story.append(Spacer(1, 14))

        # Hardware Efficiency Summary
        story.append(Paragraph("Hardware Utilization", subtitle_style))
        hw_data = [
            ["Resource", "Average Utilization"],
            ["CPU Utilization", f"{hardware_summary.get('avg_cpu_pct', 0.0):.1f}%"],
            ["RAM Used", f"{hardware_summary.get('avg_ram_gb', 0.0):.1f} GB"],
            ["GPU Utilization", f"{hardware_summary.get('avg_gpu_pct', 0.0):.1f}%"],
            ["Peak GPU VRAM", f"{hardware_summary.get('peak_vram_mb', 0.0):.0f} MB"],
            ["Peak GPU Temp", f"{hardware_summary.get('peak_gpu_temp', 0.0):.1f}°C"]
        ]
        ht = Table(hw_data, colWidths=[200, 250])
        ht.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (1,0), colors.HexColor('#334155')),
            ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ]))
        story.append(ht)
        story.append(Spacer(1, 14))

        # AI Recommendations
        if recommendations:
            story.append(Paragraph("AI Diagnostics & Recommendations", subtitle_style))
            for rec in recommendations:
                p_text = f"• <b>[{rec.get('priority')}] {rec.get('title')}</b>: {rec.get('description')}"
                story.append(Paragraph(p_text, body_style))
                story.append(Spacer(1, 4))

        doc.build(story)
        logger.info(f"Generated PDF Training Report at {output_filepath}")
        return output_filepath

class CSVExporter:
    @staticmethod
    def export_metrics_csv(output_filepath: str, metrics: List[Dict[str, Any]]) -> str:
        if not metrics:
            return output_filepath
        keys = metrics[0].keys()
        with open(output_filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(metrics)
        return output_filepath
