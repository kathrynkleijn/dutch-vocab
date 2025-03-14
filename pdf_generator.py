from datetime import date, timedelta
from fpdf import FPDF


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297

    def header(self):
        if self.page_no() != 1:
            self.set_font("Helvetica", "", 10)
            self.set_text_color(128)
            self.cell(self.WIDTH - 80)
            self.cell(60, 1, f"{date.today().strftime('%d/%m/%Y')}", 0, 0, "R")

            self.ln(20)

    def footer(self):
        if self.page_no() != 1:
            self.set_y(-15)
            self.set_font("Helvetica", "", 10)
            self.set_text_color(128)
            page_no = self.page_no() - 1
            self.cell(0, 10, "%s" % page_no, 0, 0, "C")

    def page_body(self, *args):
        content = [item for item in args][0]
        self.set_y(30)
        self.set_font("Helvetica", "", 12)
        if "/" not in content[0]:
            self.cell(40, 1, content[0], 0, 0, "C")
            for i in range(len(content) - 1):
                self.image(content[i + 1], 15, 40 + i * 120, self.WIDTH - 30)
        else:
            for i in range(len(content)):
                self.image(content[i], 15, 40 + i * 120, self.WIDTH - 30)

    def title_page(self, report_type):
        self.add_page()
        self.set_y(80)
        if report_type == "Monthly":
            date_stamp = date.today().strftime("%B %Y")
        elif report_type == "Weekly":
            date_stamp = (
                date.today() - timedelta(days=date.today().weekday())
            ).strftime("%d/%m/%Y")
        else:
            date_stamp = date.today().strftime("%d/%m/%Y")
        self.set_font("Helvetica", "B", 16)
        self.cell(self.WIDTH / 2 - 45)
        self.cell(60, 1, "Learning Log", 0, 0, "C")
        self.ln(10)
        self.set_font("Helvetica", "", 14)
        self.cell(self.WIDTH / 2 - 45)
        self.cell(60, 1, f"{report_type} Report", 0, 0, "C")
        self.ln(20)
        self.set_font("Helvetica", "I", 14)
        self.cell(self.WIDTH / 2 - 45)
        self.cell(60, 1, f"{date_stamp}", 0, 0, "C")

    def page_one(self, page_one_content):
        self.add_page()
        self.set_font("Helvetica", "B", 14)
        self.set_y(40)
        self.cell(10)
        self.cell(40, 1, "Summary", 0, 0, "L")
        self.set_y(60)
        self.set_font("Helvetica", "", 12)
        for text in page_one_content[:2]:
            self.cell(10)
            self.cell(40, 1, text, 0, 0, "L")
            self.ln(10)
        modules_content = page_one_content[2:]

        def pairs():
            for i in range(0, len(modules_content), 2):
                yield modules_content[i : i + 2]

        for pair in pairs():
            text1, text2 = pair[0], pair[1]
            self.cell(10)
            self.cell(40, 1, text1, 0, 0, "L")
            self.cell(80, 1, text2, 0, 0, "L")
            self.ln(10)

    def print_page(self, *args):
        self.add_page()
        self.page_body(*args)
