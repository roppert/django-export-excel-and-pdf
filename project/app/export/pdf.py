from io import BytesIO
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.charts.linecharts import SampleHorizontalLineChart
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.shapes import Drawing

from django.conf import settings


def WriteToPdf(weather_data, town=None):
    buffer = BytesIO()
    report = PdfPrint(buffer)
    pdf = report.report(weather_data, "Weather report")
    return pdf


class PdfPrint:
    def __init__(self, buffer):
        self.buffer = buffer
        self.pageSize = A4
        self.width, self.height = self.pageSize

    def report(self, weather_history, title):
        doc = SimpleDocTemplate(
            self.buffer, rightMargin=72, leftMargin=72,
            topMargin=30, bottomMargin=72,
            pagesize=self.pageSize
        )
        # register fonts
        freesans = settings.BASE_DIR + settings.STATIC_URL + "FreeSans.ttf"
        freesansbold = settings.BASE_DIR + settings.STATIC_URL + "FreeSansBold.ttf"
        pdfmetrics.registerFont(TTFont('FreeSans', freesans))
        pdfmetrics.registerFont(TTFont('FreeSansBold', freesansbold))
        # set up styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name="TableHeader", fontSize=11, alignment=TA_CENTER,
            fontName="FreeSansBold"))
        styles.add(ParagraphStyle(
            name="ParagraphTitle", fontSize=11, alignment=TA_JUSTIFY,
            fontName="FreeSansBold"))
        styles.add(ParagraphStyle(
            name="Justify", alignment=TA_JUSTIFY, fontName="FreeSans"))

        data = []
        data.append(Paragraph(title, styles["Title"]))
        data.append(Spacer(1, 12))
        table_data = []
        # table header
        table_data.append([
            Paragraph('Date', styles['TableHeader']),
            Paragraph('Station', styles['TableHeader']),
            Paragraph('Min temp', styles['TableHeader']),
            Paragraph('Mean temp', styles['TableHeader']),
            Paragraph('Max temp', styles['TableHeader'])
        ])
        for wh in weather_history:
            # add a row to table
            table_data.append([
                wh.date,
                Paragraph(wh.station.name, styles['Justify']),
                u"{0} °C".format(wh.min),
                u"{0} °C".format(wh.mean),
                u"{0} °C".format(wh.max)
            ])
        # create table
        wh_table = Table(table_data, colWidths=[doc.width/5.0]*5)
        wh_table.hAlign = 'LEFT'
        wh_table.setStyle(TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))
        data.append(wh_table)
        data.append(Spacer(1, 48))

        # create line chart
        chart = SampleHorizontalLineChart()
        chart.width = 350
        chart.height = 135
        mins = [float(x.min) for x in weather_history]
        means = [float(x.mean) for x in weather_history]
        maxs = [float(x.max) for x in weather_history]
        chart.data = [mins, means, maxs]
        chart.lineLabels.fontName = 'FreeSans'
        chart.strokeColor = colors.white
        chart.fillColor = colors.lightblue
        chart.lines[0].strokeColor = colors.red
        chart.lines[0].strokeWidth = 2
        chart.lines.symbol = makeMarker('Square')
        chart.lineLabelFormat = '%2.0f'
        chart.categoryAxis.joinAxisMode = 'bottom'
        chart.categoryAxis.labels.fontName = 'FreeSans'
        chart.categoryAxis.labels.angle = 45
        chart.categoryAxis.labels.boxAnchor = 'e'
        chart.categoryAxis.categoryNames = [str(x.date) for x in weather_history]
        chart.valueAxis.labelTextFormat = '%2.0f °C'
        chart.valueAxis.valueStep = 10

        # chart needs to be put in a drawing
        d = Drawing(0, 170)
        d.add(chart)
        # add drawing to data
        data.append(d)

        doc.build(data)
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf
