from models import db, Organization, Company, save_password

# Create the database tables
db.create_all()

# Create an organization
org = Organization(name='Example Org')
db.session.add(org)
db.session.commit()

# Create a company for the organization
company = Company(
    organization=org,
    name='Example Company',
    full_name='Example Company Inc.',
    pricing_option='Option A',
    email='example@example.com',
    password=save_password('example_password')
)
db.session.add(company)
db.session.commit()
