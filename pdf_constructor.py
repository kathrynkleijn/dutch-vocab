import os
import pdf_generator
import figure_generator


def construct(report_title):

    headings = ["By Module", "By Lesson"]
    pages_data = []

    files_used = 0
    for index, heading in enumerate(headings):
        temp = [heading]
        files = [
            f"plots/{report_title.lower()}/{file}"
            for file in os.listdir(f"plots/{report_title.lower()}")
        ]
        temp.extend(files[3 * index : 3 * index + 2])
        pages_data.append(temp)
        if heading == "By Module":
            pages_data.append([files[3 * index + 2]])
            files_used += 3
        else:
            files_used += 2

    if report_title == "Progress":
        pages_data.append([files[files_used]])
        temp = ["By Month"]
        for file in files[files_used + 1 :]:
            temp.append(file)
            pages_data.append(temp)
            temp = []
    else:
        counter = 0
        temp = []
        for file in files[files_used:]:
            if counter == 2:
                pages_data.append(temp)
                temp = []
                counter = 0
            temp.append(file)
            counter += 1

    return [*pages_data, temp] if temp else [*pages_data]


def build_pdf(log, report_title):
    pdf = pdf_generator.PDF()
    logs = figure_generator.log_maker(report_title, log)
    figure_generator.generate_figures(report_title, logs)
    plots_per_page = construct(report_title)

    pdf.title_page(report_title)
    text = figure_generator.text_generator(report_title, logs)
    pdf.page_one(text)
    for element in plots_per_page:
        pdf.print_page(element)

    return pdf
