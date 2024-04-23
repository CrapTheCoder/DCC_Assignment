import fitz
import csv


for file_name in ['eb_party', 'eb_company']:
    with open(f'static/{file_name}_.csv', 'w') as file:
        writer = csv.writer(file)
        doc = fitz.open(f'static/{file_name}.pdf')

        writer.writerow(i.replace('\n', ' ').strip() for i in doc[0].find_tables()[0].extract()[0])

        for page in doc:
            writer.writerows(i for i in page.find_tables()[0].extract()[1:])
