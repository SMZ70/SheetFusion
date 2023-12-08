import PyPDF3


# Function to create individual PDFs
def create_pdf_per_cover_sheet(cover_sheets_file, exam_file):
    # Open the cover sheets and exam PDFs
    with open(cover_sheets_file, "rb") as covers, open(exam_file, "rb") as exam:
        cover_reader = PyPDF3.PdfFileReader(covers)
        exam_reader = PyPDF3.PdfFileReader(exam)

        # Iterate over each cover sheet
        for i in range(cover_reader.numPages):
            writer = PyPDF3.PdfFileWriter()

            # Add the cover sheet
            writer.addPage(cover_reader.getPage(i))

            # Add all pages of the exam
            for j in range(exam_reader.numPages):
                writer.addPage(exam_reader.getPage(j))

            # Save the new PDF
            with open(f"student_{i+1}_exam.pdf", "wb") as output_pdf:
                writer.write(output_pdf)


if __name__ == "__main__":
    create_pdf_per_cover_sheet("cover_sheet.pdf", "exam.pdf")
