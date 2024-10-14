from flask import Flask, redirect, request, url_for, abort
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from models import Influencer, TrackingLink, Visit
import os
import re

app = Flask(__name__)

# Database setup using environment variables for security
DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql+psycopg2://tracking_user:your_password@localhost/tracking_app_db')

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

def generate_unique_id():
    import uuid
    return str(uuid.uuid4())

def generate_unique_code():
    import uuid
    return uuid.uuid4().hex[:6].upper()

def is_valid_url(url):
    # Simple regex for URL validation
    regex = re.compile(
        r'^(?:http|https)://'  # http:// or https://
        r'\w+(?:\.\w+)+.*$'    # Domain...
    )
    return re.match(regex, url) is not None

@app.route('/generate_link/<influencer_name>', methods=['POST'])
def generate_link(influencer_name):
    try:
        # Get destination_url from POST data
        destination_url = request.form.get('destination_url')
        if not destination_url or not is_valid_url(destination_url):
            return 'Invalid or missing destination URL.', 400

        # Check if influencer exists
        influencer = session.query(Influencer).filter_by(name=influencer_name).first()
        if not influencer:
            influencer = Influencer(name=influencer_name, unique_id=generate_unique_id())
            session.add(influencer)
            session.commit()

        # Generate unique tracking link
        unique_code = generate_unique_code()
        tracking_link = TrackingLink(
            influencer_id=influencer.id,
            destination_url=destination_url,
            unique_code=unique_code
        )
        session.add(tracking_link)
        session.commit()

        full_link = url_for('redirect_link', unique_code=unique_code, _external=True)
        return f'Generated link for {influencer_name}: {full_link}'
    except SQLAlchemyError as e:
        session.rollback()
        app.logger.error(f"Database error: {e}")
        return 'An error occurred while generating the link.', 500
    finally:
        session.close()

@app.route('/link/<unique_code>')
def redirect_link(unique_code):
    try:
        tracking_link = session.query(TrackingLink).filter_by(unique_code=unique_code).first()
        if not tracking_link:
            abort(404)

        # Log the visit
        visit = Visit(
            tracking_link_id=tracking_link.id,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        session.add(visit)
        session.commit()

        # Redirect to destination URL
        return redirect(tracking_link.destination_url)
    except SQLAlchemyError as e:
        session.rollback()
        app.logger.error(f"Database error: {e}")
        return 'An error occurred while processing your request.', 500
    finally:
        session.close()

@app.route('/influencer_visits/<influencer_name>', methods=['GET'])
def influencer_visits(influencer_name):
    try:
        # Check if the influencer exists
        influencer = session.query(Influencer).filter_by(name=influencer_name).first()
        if not influencer:
            return f'Influencer {influencer_name} not found.', 404

        # Get all tracking links for this influencer
        tracking_links = session.query(TrackingLink).filter_by(influencer_id=influencer.id).all()
        if not tracking_links:
            return f'No tracking links found for {influencer_name}.', 404

        # Initialize a list to store visit counts
        visits_data = []
        total_visits = 0

        # Loop through all tracking links to collect visits
        for link in tracking_links:
            visit_count = session.query(Visit).filter_by(tracking_link_id=link.id).count()
            total_visits += visit_count
            visits_data.append({
                'tracking_link': link.destination_url,
                'unique_code': link.unique_code,
                'visit_count': visit_count
            })

        # Return influencer visit information as JSON
        return {
            'influencer_name': influencer_name,
            'total_visits': total_visits,
            'visit_details': visits_data
        }, 200
    except SQLAlchemyError as e:
        session.rollback()
        app.logger.error(f"Database error: {e}")
        return 'An error occurred while fetching visits.', 500
    finally:
        session.close()




if __name__ == '__main__':
    app.run(debug=True)
