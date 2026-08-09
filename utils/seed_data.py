from datetime import datetime, timedelta
from models import db
from models.user import User
from models.report import DisasterReport
from models.shelter import Shelter
from models.alert import Alert
from models.guideline import SafetyGuideline

def seed_database():
    """Populates initial database entries if empty."""
    # Seed Users
    if User.query.count() == 0:
        admin_user = User(
            username='admin',
            email='admin@disastermanagement.org',
            full_name='System Administrator',
            phone='+1-800-555-0199',
            role='admin'
        )
        admin_user.set_password('admin123')

        demo_user1 = User(
            username='johndoe',
            email='john@example.com',
            full_name='John Doe',
            phone='+1-555-0147',
            role='user'
        )
        demo_user1.set_password('user123')

        demo_user2 = User(
            username='sarah_smith',
            email='sarah@example.com',
            full_name='Sarah Smith',
            phone='+1-555-0188',
            role='user'
        )
        demo_user2.set_password('user123')

        db.session.add_all([admin_user, demo_user1, demo_user2])
        db.session.commit()
        print("-> Users seeded successfully.")

    # Seed Shelters
    if Shelter.query.count() == 0:
        shelters = [
            Shelter(
                name='Central Community High School Relief Shelter',
                address='124 Park Avenue, City Center',
                capacity=500,
                available_space=180,
                contact_number='+1-800-555-7435',
                maps_url='https://maps.google.com/?q=Central+High+School',
                status='Open'
            ),
            Shelter(
                name='St. Jude Sports Complex Evacuation Center',
                address='45 Stadium Drive, Sector 9',
                capacity=800,
                available_space=350,
                contact_number='+1-800-555-8821',
                maps_url='https://maps.google.com/?q=St+Jude+Sports+Complex',
                status='Open'
            ),
            Shelter(
                name='Northside Civic Center Shelter',
                address='88 Northern Boulevard',
                capacity=350,
                available_space=45,
                contact_number='+1-800-555-3390',
                maps_url='https://maps.google.com/?q=Northside+Civic+Center',
                status='Open'
            ),
            Shelter(
                name='West End Primary School Hall',
                address='12 Westside Road',
                capacity=200,
                available_space=0,
                contact_number='+1-800-555-1102',
                maps_url='https://maps.google.com/?q=West+End+School',
                status='Full'
            )
        ]
        db.session.add_all(shelters)
        db.session.commit()
        print("-> Shelters seeded successfully.")

    # Seed Emergency Alerts
    if Alert.query.count() == 0:
        alerts = [
            Alert(
                title='Flash Flood Warning: Riverside Sector 4',
                disaster_type='Flood',
                affected_area='Riverside District, Low-lying coastal zones',
                severity_level='Emergency',
                description='Heavy continuous downpour leading to rapid river overflow. Immediate evacuation ordered for ground floor residents.',
                evacuation_instructions='Move immediately to Central Community Relief Shelter on 124 Park Avenue. Carry essential documents, medications, and bottled water.',
                is_active=True
            ),
            Alert(
                title='Severe Industrial Fire Safety Alert',
                disaster_type='Fire',
                affected_area='Industrial Park, Sector 15',
                severity_level='High',
                description='Toxic smoke advisory due to warehouse fire. Nearby commercial zones evacuated.',
                evacuation_instructions='Close all doors and windows. Turn off air conditioners. Evacuate towards South exit routes.',
                is_active=True
            )
        ]
        db.session.add_all(alerts)
        db.session.commit()
        print("-> Alerts seeded successfully.")

    # Seed Disaster Reports
    if DisasterReport.query.count() == 0:
        john = User.query.filter_by(username='johndoe').first()
        sarah = User.query.filter_by(username='sarah_smith').first()

        user1_id = john.id if john else 1
        user2_id = sarah.id if sarah else 2

        reports = [
            DisasterReport(
                user_id=user1_id,
                disaster_type='Flood',
                location='Riverside District, Sector 4',
                latitude=28.6139,
                longitude=77.2090,
                date_time=datetime.utcnow() - timedelta(days=2),
                description='Water level rising rapidly over the embankment. Main arterial road submerged.',
                image_path='sample_flood.jpg',
                severity='High',
                status='Active',
                risk_level='CRITICAL',
                safety_recommendation='Evacuate to higher ground immediately. Turn off electrical supply. Avoid driving through flooded streets.'
            ),
            DisasterReport(
                user_id=user2_id,
                disaster_type='Fire',
                location='Industrial Park, Building B',
                latitude=28.5355,
                longitude=77.3910,
                date_time=datetime.utcnow() - timedelta(days=1),
                description='Chemical warehouse fire spreading towards nearby commercial units. Heavy smoke visible.',
                image_path='sample_fire.jpg',
                severity='High',
                status='Active',
                risk_level='CRITICAL',
                safety_recommendation='Keep clear of smoke plume. Use N95 masks or wet cloth over nose and mouth. Follow evacuation wardens.'
            ),
            DisasterReport(
                user_id=user1_id,
                disaster_type='Cyclone',
                location='Coastal Boulevard, North Bay',
                latitude=13.0827,
                longitude=80.2707,
                date_time=datetime.utcnow() - timedelta(days=5),
                description='High winds causing power line disruption and fallen trees blocking access roads.',
                image_path='sample_cyclone.jpg',
                severity='Medium',
                status='Resolved',
                risk_level='HIGH',
                safety_recommendation='Stay indoors away from window panes. Store emergency drinking water and flashlights.'
            ),
            DisasterReport(
                user_id=user2_id,
                disaster_type='Landslide',
                location='Highland Pass, Highway 12',
                latitude=31.1048,
                longitude=77.1734,
                date_time=datetime.utcnow() - timedelta(days=3),
                description='Debris flow blocking both lanes of Highway 12. Traffic halted.',
                image_path='sample_landslide.jpg',
                severity='Medium',
                status='Active',
                risk_level='HIGH',
                safety_recommendation='Do not attempt to pass slope. Be alert for falling rocks. Monitor local traffic radio broadcasts.'
            )
        ]
        db.session.add_all(reports)
        db.session.commit()
        print("-> Reports seeded successfully.")

    # Seed Safety Guidelines
    if SafetyGuideline.query.count() == 0:
        guidelines = [
            SafetyGuideline(
                disaster_type='Flood',
                before_tips='Prepare an emergency kit with 3 days of food/water. Identify highest ground level in your home. Install check valves in plumbing.',
                during_tips='Never walk or drive through moving flood water. If trapped in building, move to roof only if necessary. Keep battery radio on.',
                after_tips='Avoid floodwater as it may be contaminated. Check structural safety before entering buildings. Discard food touched by floodwater.',
                first_aid='Treat cuts with clean water and antiseptic. Keep hypothermia risk low by keeping dry.',
                emergency_kit='Water (1 gal/person/day), non-perishable food, flashlight, first aid kit, multi-tool, extra batteries, whistle, emergency blanket.'
            ),
            SafetyGuideline(
                disaster_type='Fire',
                before_tips='Test smoke alarms monthly. Keep fire extinguishers on every level. Plan two escape routes from every room.',
                during_tips='Crawl low under smoke to escape. Touch doors before opening; if hot, use alternate exit. Stop, drop, and roll if clothes catch fire.',
                after_tips='Do not enter burned structure until cleared by fire department. Cool minor burns with cool water. Document property damage.',
                first_aid='Cool burns with cold running water for 10-15 mins. Cover with sterile non-stick bandage. Do not pop blisters.',
                emergency_kit='N95 dust mask, fire-resistant blanket, burn ointment, heavy gloves, flashlight, emergency contact numbers, bottled water.'
            ),
            SafetyGuideline(
                disaster_type='Cyclone',
                before_tips='Trim trees near house. Secure loose outdoor objects. Board up windows with storm shutters or plywood.',
                during_tips='Stay inside away from windows and glass doors. Take shelter in small interior room or closet on lowest level.',
                after_tips='Watch out for fallen power lines. Beware of weakened trees or structures. Drink only bottled or boiled water.',
                first_aid='Clean debris wounds thoroughly. Use pressure dressing for active bleeding.',
                emergency_kit='Battery-powered NOAA weather radio, waterproof pouch for documents, power bank, sturdy boots, rain gear, non-perishable food.'
            ),
            SafetyGuideline(
                disaster_type='Earthquake',
                before_tips='Anchor heavy furniture, appliances, and TVs to walls. Store breakables in low cabinets with latches.',
                during_tips='DROP, COVER, and HOLD ON! Get under sturdy table/desk. Protect head and neck. If outside, move away from buildings.',
                after_tips='Expect aftershocks. Check for gas leaks and turn off gas valve if smelling odor. Inspect home for structural cracks.',
                first_aid='Apply splints to suspected fractures. Do not move severely injured persons unless immediate hazard exists.',
                emergency_kit='Sturdy gloves, dust mask, heavy duty flashlight, whistle, emergency shelter tent, 3-day water supply, first aid manual.'
            ),
            SafetyGuideline(
                disaster_type='Landslide',
                before_tips='Plant ground cover on slopes and build retaining walls. Consult land stability experts before building near hills.',
                during_tips='If inside, stay inside and get under heavy desk or table. If outside, run to nearest high ground away from flow path.',
                after_tips='Stay away from slide area; secondary slides may occur. Check for injured or trapped persons near slide edge without entering hazardous zone.',
                first_aid='Treat crush injuries for shock. Maintain open airway.',
                emergency_kit='Emergency radio, heavy work boots, thick gloves, rope, first aid kit, water, multi-tool knife.'
            )
        ]
        db.session.add_all(guidelines)
        db.session.commit()
        print("-> Safety guidelines seeded successfully.")
