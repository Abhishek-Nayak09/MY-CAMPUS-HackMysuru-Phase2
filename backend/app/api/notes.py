import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User
from app.models.topic import Topic
from app.models.note import Note, NoteSection


router = APIRouter(
    prefix="/notes",
    tags=["Rich Notes"]
)


# =========================================================
# GET RICH NOTES FOR A TOPIC
# =========================================================

@router.get("/topic/{topic_id}")
def get_topic_notes(
    topic_id: int,
    db: Session = Depends(get_db)
):

    # =====================================================
    # FIND TOPIC
    # =====================================================

    topic = (
        db.query(Topic)
        .filter(
            Topic.id == topic_id
        )
        .first()
    )


    if not topic:

        raise HTTPException(
            status_code=404,
            detail="Topic not found"
        )


    # =====================================================
    # FIND ACTIVE NOTE
    # =====================================================

    note = (
        db.query(Note)
        .filter(
            Note.topic_id == topic_id,
            Note.is_active == True
        )
        .order_by(
            Note.version.desc()
        )
        .first()
    )


    if not note:

        raise HTTPException(
            status_code=404,
            detail="Notes not available for this topic"
        )


    # =====================================================
    # FIND NOTE SECTIONS
    # =====================================================

    sections = (
        db.query(NoteSection)
        .filter(
            NoteSection.note_id == note.id,
            NoteSection.is_active == True
        )
        .order_by(
            NoteSection.section_order
        )
        .all()
    )


    section_list = []


    for section in sections:

        interactive_data = None


        if section.interactive_data:

            try:

                interactive_data = json.loads(
                    section.interactive_data
                )

            except json.JSONDecodeError:

                interactive_data = None


        section_list.append(
            {
                "id":
                    section.id,

                "order":
                    section.section_order,

                "type":
                    section.section_type,

                "heading":
                    section.heading,

                "body":
                    section.body,

                "media": {
                    "url":
                        section.media_url,

                    "type":
                        section.media_type,

                    "caption":
                        section.caption,

                    "alt_text":
                        section.alt_text
                },

                "interactive":
                    interactive_data
            }
        )


    # =====================================================
    # FACULTY INFO
    # =====================================================

    creator = None


    if note.created_by:

        creator = (
            db.query(User)
            .filter(
                User.id == note.created_by
            )
            .first()
        )


    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "topic": {
            "id":
                topic.id,

            "title":
                topic.title,

            "description":
                topic.description
        },


        "note": {

            "id":
                note.id,

            "title":
                note.title,

            "subtitle":
                note.subtitle,

            "introduction":
                note.introduction,

            "version":
                note.version,

            "pdf_url":
                note.pdf_url,

            "created_by": {

                "id":
                    creator.id
                    if creator
                    else None,

                "name":
                    creator.full_name
                    if creator
                    else "System Demo Content"

            },

            "created_at":
                note.created_at,

            "updated_at":
                note.updated_at
        },


        "sections":
            section_list,


        "total_sections":
            len(section_list)

    }