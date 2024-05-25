import base64
import dataframe_image as dfi
from io import BytesIO

# Creates Util functions
def string_to_dict(string):
    
    if string == None:
        return dict()
    
    pairs = string.split(", ")
    dictionary = {}
    for pair in pairs:
        if len(pair.split(": ")) < 2:
            continue
        key, value = pair.split(": ")
        if not value.isnumeric():
            continue
        dictionary[key.strip()] = int(value.strip())
    return dictionary

def matplotlib_fig_to_img(fig):
    
    # Saves it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    
    # Encodes as base64 and adds to buffer
    fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    fig_matplotlib = f'data:image/png;base64,{fig_data}'
    
    return fig_matplotlib

def dataframe_table_to_img(table):
    
    # Saves it to a temporary buffer.
    buf = BytesIO()
    dfi.export(table, buf)
    
    # Encodes as base64 and adds to buffer
    img_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    img_table = f'data:image/png;base64,{img_data}'
    
    return img_table

def toggle_images(n_clicks, img1_style, img2_style):
    if n_clicks is None:
        # No button click yet, returns current styles
        return img1_style, img2_style
    
    # Toggles visibility based on current state
    if img1_style.get('display') == 'none':
        # image-1 is hidden, shows it and hides image-2
        return {'display': 'block', 'width': '100%', 'height': 'auto'}, {'display': 'none'}
    else:
        # image-1 is visible, hides it and shows image-2
        return {'display': 'none'}, {'display': 'block', 'width': '100%', 'height': 'auto'}
    
def build_pdf(pdf, context):
    
    def extract_img_bytes(base64string):
        return base64.b64decode(base64string.split(',')[1])
    
    # In order to embed into PDF, we must first save all figures as PNGs
    context['fig_1'].write_image("fig_individual.png")
    context['fig_2'].write_image("fig_portfolio_benchmark.png")
    with open("bars_current_value_dividends.png", "wb") as img1:
        img1.write(extract_img_bytes(context['fig_7']))
    with open("fig_current_allocation.png", "wb") as img1:
        img1.write(extract_img_bytes(context['fig_3_2']))
    with open("fig_current_industry_allocation.png", "wb") as img1:
        img1.write(extract_img_bytes(context['fig_5_2']))
    with open("overview_table.png", "wb") as img1:
        img1.write(extract_img_bytes(context['table_1']))
    with open("bars_current_country_allocation.png", "wb") as img1:
        img1.write(extract_img_bytes(context['fig_4_2']))
    with open("bars_current_country_industry.png", "wb") as img1:
        img1.write(extract_img_bytes(context['fig_6_2']))
    
    WIDTH = 297
    HEIGHT = 210
    
    ''' First Page '''
    pdf.add_page()
    pdf.set_font('Arial', 'B', 40)  
    pdf.set_fill_color(0, 0, 255)  # Blue color
    pdf.set_text_color(255, 255, 255)  # White color
    pdf.cell(0, 17,'Portfolio Overview',ln=1,fill=1)
    pdf.set_font('Arial', '', 20)
    pdf.cell(0, 10, context['start_date'] +' to '+ context['end_date'],ln=1,fill=1)
    pdf.set_fill_color(255, 255, 255)  # Resets fill color to white for other cells
    pdf.set_text_color(0, 0, 0)  # Resets text color to black
    pdf.set_font('Arial', '', 20)
    pdf.cell(3*WIDTH/5+5, 10,'',ln=1)
    pdf.cell(3*WIDTH/5+5, 10,'Portfolio Update',ln=1)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(3*WIDTH/5-5,5,'The present document reports the performance of the selected stocks for the period  '+ context['start_date'] +' to '+ context['end_date'] +'. It compares the portfolio performance with the selected benchmark. It provides useful information including Capital Gains, Net Profit, Total Dividends and the Current Value of the Portfolio and the Stocks. Further it provides analysis regarding the allocation on the levels of Stocks, Geography and Industry. The information on the present report concerns only the values of the current/latest prices. For similar historical analysis we recommend the use of the interface. This report should be used only for educational reasons and to help the user track his/her investment with ease.'+ '\n' + 'IT IS NOT RECOMMENDED TO USE THE INFORMATION PROVIDED IN THIS REPORT TO INFORM YOUR DECISIONS FOR FUTURE INVESTMENTS!')
    pdf.image("bars_current_value_dividends.png",5,115,3*WIDTH/5,h=90)
    pdf.image("fig_current_allocation.png",3*WIDTH/5+10,50,2*WIDTH/5-10,h=75)
    pdf.image("fig_current_industry_allocation.png",3*WIDTH/5+10,130,2*WIDTH/5-10,h=75)
    
    ''' Second Page '''
    pdf.add_page()
    pdf.set_font('Arial', '', 20)
    pdf.cell(3*WIDTH/5+5, 8,'News',ln=1)    
    pdf.set_font('Arial', '', 12)
    for headline in context['headlines']:
        encoded_headline = headline['title'].encode('ascii', 'ignore').decode('ascii')
        pdf.cell(3*WIDTH/5, 6, "- " + encoded_headline,ln=1)
    pdf.image("fig_individual.png",75,67,WIDTH/2,78) 
    pdf.image("fig_portfolio_benchmark.png",75,137,WIDTH/2,78)
    
    ''' Third Page '''
    pdf.add_page()
    pdf.image("overview_table.png",75,10,WIDTH/2,h=70)
    pdf.image("bars_current_country_allocation.png",0,90,WIDTH/2,h=80)
    pdf.image("bars_current_country_industry.png",WIDTH/2,90,WIDTH/2,h=84)
