from app.db.database import SessionLocal
from app.db.models import Document, LegalSection


def seed_data():
    db = SessionLocal()

    existing = db.query(Document).filter(
        Document.title == "नेपालको संविधान"
    ).first()

    if existing:
        print("Seed data already exists. Skipping.")
        db.close()
        return

    constitution = Document(
        title="नेपालको संविधान",
        document_type="constitution",
        language="ne",
        source_url="manual_seed",
    )

    db.add(constitution)
    db.commit()
    db.refresh(constitution)

    sections = [
        LegalSection(
            document_id=constitution.id,
            section_number="१",
            chapter="प्रारम्भिक",
            heading="संविधान मूल कानून",
            content="यो संविधान नेपालको मूल कानून हो। यससँग बाझिने कानून बाझिएको हदसम्म अमान्य हुनेछ।",
        ),
        LegalSection(
            document_id=constitution.id,
            section_number="१६",
            chapter="मौलिक हक",
            heading="सम्मानपूर्वक बाँच्न पाउने हक",
            content="प्रत्येक व्यक्तिलाई सम्मानपूर्वक बाँच्न पाउने हक हुनेछ। मृत्युदण्डको सजाय हुने गरी कुनै कानून बनाइने छैन।",
        ),
        LegalSection(
            document_id=constitution.id,
            section_number="१७",
            chapter="मौलिक हक",
            heading="स्वतन्त्रताको हक",
            content="कानून बमोजिम बाहेक कुनै पनि व्यक्तिलाई वैयक्तिक स्वतन्त्रताबाट वञ्चित गरिने छैन।",
        ),
        LegalSection(
            document_id=constitution.id,
            section_number="१८",
            chapter="मौलिक हक",
            heading="समानताको हक",
            content="सबै नागरिक कानूनको दृष्टिमा समान हुनेछन्। कसैलाई पनि कानूनको समान संरक्षणबाट वञ्चित गरिने छैन।",
        ),
    ]

    db.add_all(sections)
    db.commit()
    db.close()

    print("Seed data inserted successfully.")


if __name__ == "__main__":
    seed_data()