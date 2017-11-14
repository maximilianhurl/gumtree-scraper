from project.emails import send_email
from project.models import Advert
from project.settings import create_sqlalchemy_engine, commit_session


def generate_report():
    engine, Session = create_sqlalchemy_engine()
    session = Session()

    non_processed_adverts = session.query(Advert).filter_by(processed=False).all()

    if not non_processed_adverts:
        return

    message = ["New gumtree adverts: \n\n"]
    for advert in non_processed_adverts:
        message.append(f"Title: {advert.title}\n£{advert.price}\nLink: {advert.url}\n\n")
        advert.processed = True

    send_email("New gumtree adverts!", "".join(message))

    commit_session(session)
