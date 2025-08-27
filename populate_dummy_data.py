import os
import django
from datetime import date, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
django.setup()

from my_app.models import Exam, Scheme

# Realistic Indian Exams
exam_names = [
    "UPSC Civil Services", "SSC CGL", "NEET UG", "JEE Main", "CAT", "GATE", "IBPS PO",
    "RRB NTPC", "NDA", "CLAT", "UP Police SI", "Delhi Police Constable",
    "RBI Grade B", "AIIMS Nursing", "UGC NET", "LIC AAO", "DRDO CEPTAM", "SSC CHSL",
    "AFCAT", "TET", "JEECUP", "WBJEE", "KVS PRT", "CSIR NET", "CDS", "EPFO SSA"
]

# Realistic Indian Government Schemes
scheme_data = [
    ("Pradhan Mantri Awas Yojana", "Housing"),
    ("Startup India", "Startup"),
    ("Stand-Up India", "Entrepreneurship"),
    ("Digital India", "Technology"),
    ("Ayushman Bharat", "Healthcare"),
    ("Kisan Credit Card", "Agriculture"),
    ("PM Kisan Samman Nidhi", "Agriculture"),
    ("Beti Bachao Beti Padhao", "Education"),
    ("National Scholarship Portal", "Education"),
    ("Pradhan Mantri Ujjwala Yojana", "Welfare"),
    ("PM SVANidhi", "Employment"),
    ("e-SHRAM Portal", "Employment"),
    ("Jal Jeevan Mission", "Infrastructure"),
    ("Atal Pension Yojana", "Pension"),
    ("Mudra Yojana", "Startup"),
    ("PM Garib Kalyan Yojana", "Welfare"),
    ("Skill India Mission", "Employment"),
    ("Make in India", "Industry"),
    ("Smart Cities Mission", "Urban Development"),
    ("Swachh Bharat Mission", "Sanitation"),
    ("PM Fasal Bima Yojana", "Agriculture"),
    ("Deen Dayal Upadhyaya Grameen Kaushalya Yojana", "Rural Development"),
    ("PM Vaya Vandana Yojana", "Pension"),
    ("Rashtriya Swasthya Bima Yojana", "Healthcare"),
    ("Nai Roshni Scheme", "Minority Welfare"),
    ("National Rural Employment Guarantee Act", "Employment")
]

# Populate Exams
for name in random.sample(exam_names, k=min(30, len(exam_names))):  # pick up to 30
    Exam.objects.create(
        name=name,
        date=date.today() + timedelta(days=random.randint(5, 90))
    )

# Populate Schemes
for name, type_ in random.sample(scheme_data, k=min(30, len(scheme_data))):
    Scheme.objects.create(
        name=name,
        type=type_
    )

print("✅ Dummy Indian exams and schemes added successfully.")
