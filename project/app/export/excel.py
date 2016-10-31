from io import BytesIO
import xlsxwriter
from django.utils.translation import ugettext

def WriteToExcel(weather_data, town=None):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)

    # define styles to use
    title = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter'
    })
    header = workbook.add_format({
            'bg_color': '#cfe7f5',
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'border': 1
    })
    cell = workbook.add_format({})
    cell_center = workbook.add_format({'align': 'center'})

    # add a worksheet to work with
    worksheet_s = workbook.add_worksheet("Summary")

    # create title
    title_text = ugettext("Temperature history for %(station)s") % {'station': town}
    # add title to sheet, use merge_range to let title span over multiple columns
    worksheet_s.merge_range('B2:H2', title_text, title)

    # Add headers for data
    worksheet_s.write(4, 0, ugettext("Date"), header)
    worksheet_s.write(4, 1, ugettext("Station"), header)
    worksheet_s.write(4, 2, ugettext(u"Min T. (°C)"), header)
    worksheet_s.write(4, 3, ugettext(u"Mean T. (°C)"), header)
    worksheet_s.write(4, 4, ugettext(u"Max T. (°C)"), header)
    worksheet_s.write(4, 5, ugettext(u"Avg.Min T. (°C)"), header)
    worksheet_s.write(4, 6, ugettext(u"Avg.Mean T. (°C)"), header)
    worksheet_s.write(4, 7, ugettext(u"Avg.Max T. (°C)"), header)

    # write data to cells
    station_name_width = 10
    for idx, data in enumerate(weather_data):
        row_index = 5 + idx
        worksheet_s.write(row_index, 0, data.date.strftime("%Y-%m-%d"), cell_center)
        worksheet_s.write_string(row_index, 1, data.station.name, cell_center)
        worksheet_s.write_number(row_index, 2, data.min, cell)
        worksheet_s.write_number(row_index, 3, data.mean, cell)
        worksheet_s.write_number(row_index, 4, data.max, cell)
        if len(data.station.name) > station_name_width:
            station_name_width = len(data.station.name)

        # add formulas to calc avg. over time
        worksheet_s.write_formula(row_index, 5, '=AVERAGE({0}{1}:{0}{2})'.format('C', 6, row_index+1))
        worksheet_s.write_formula(row_index, 6, '=AVERAGE({0}{1}:{0}{2})'.format('D', 6, row_index+1))
        worksheet_s.write_formula(row_index, 7, '=AVERAGE({0}{1}:{0}{2})'.format('E', 6, row_index+1))

    # resize rows and columns
    worksheet_s.set_column('A:A', 12)
    worksheet_s.set_column('B:B', station_name_width)
    worksheet_s.set_column('C:H', 10)

    # add chart
    worksheet_c = workbook.add_worksheet("Charts")
    worksheet_d = workbook.add_worksheet("Chart data")

    # chart data
    for row_index, data in enumerate(weather_data):
        worksheet_d.write(row_index, 0, data.date.strftime("%Y-%m-%d"))
        worksheet_d.write_number(row_index, 1, data.min)
        worksheet_d.write_number(row_index, 2, data.mean)
        worksheet_d.write_number(row_index, 3, data.max)

    # line chart
    line_chart = workbook.add_chart({'type': 'line'})
    line_chart.add_series({
            'categories': '=Chart data!$A1:$A{0}'.format(len(weather_data)),
            'values': '=Chart data!$B1:$B{0}'.format(len(weather_data)),
            'marker': {'type': 'square'},
            'name': ugettext("Min T.")
    })
    line_chart.add_series({
            'categories': '=Chart data!$A1:$A{0}'.format(len(weather_data)),
            'values': '=Chart data!$C1:$C{0}'.format(len(weather_data)),
            'marker': {'type': 'square'},
            'name': ugettext("Mean T.")
    })
    line_chart.add_series({
            'categories': '=Chart data!$A1:$A{0}'.format(len(weather_data)),
            'values': '=Chart data!$D1:$D{0}'.format(len(weather_data)),
            'marker': {'type': 'square'},
            'name': ugettext("Max T.")
    })
    line_chart.set_title({'name': ugettext("Temperatures")})
    line_chart.set_x_axis({ 'text_axis': True, 'date_axis': False })
    line_chart.set_y_axis({ 'num_format': u'## °C' })
    worksheet_c.insert_chart('B2', line_chart, {'x_scale': 2, 'y_scale': 1})

    workbook.close()
    xlsx_data = output.getvalue()
    # xlsx_data contains the Excel file
    return xlsx_data

