from django.core.management.base import BaseCommand
from UserApp.models import Job, Employer  # Adjust this import if necessary to match your app and model names
import lxml.etree as ET  # installed with pip install lxml

class Command(BaseCommand):
    help = 'Parse job listings from an XML file and save them to the database'

    def add_arguments(self, parser):
        parser.add_argument('xml_file', type=str, help='The XML file containing the job listings')
    
    def handle(self, *args, **kwargs):
        xml_file = kwargs['xml_file']

        # Open and parse the XML file
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error parsing XML file: {e}'))
            return

        # Here we will iterate over the job listings and create Job objects
        for job_element in root.findall('job'):
            title = job_element.find('jobTitle').text
            description = job_element.find('jobDescription').text
            location = job_element.find('location').text
            apply_url = job_element.find('applyURL').text
        
            # Find the employer object - replace 'your_employer_name' with the actual employer name
            employer, created = Employer.objects.get_or_create(name='your_employer_name')
        
            # Create a new Job object
            job = Job(
                title=title,
                description=description,
                location=location,
                apply_url=apply_url,
                employer=employer
            )
        
            # Save the Job object to the database
            job.save()
    
        self.stdout.write(self.style.SUCCESS('Successfully parsed XML file'))
