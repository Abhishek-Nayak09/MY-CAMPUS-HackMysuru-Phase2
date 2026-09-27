from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

# Import dependencies so SQLAlchemy knows the full model graph
from app.models.user import User
from app.models.topic import Topic
from app.models.learning_content import LearningContent


router = APIRouter(
    prefix="/content",
    tags=["Learning Content"]
)


# =========================================================
# GET ALL LEARNING CONTENT FOR ONE TOPIC
# =========================================================

@router.get("/topic/{topic_id}")
def get_topic_content(
    topic_id: int,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # FIND TOPIC
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # FIND ACTIVE LEARNING CONTENT
    # -----------------------------------------------------

    contents = (
        db.query(LearningContent)
        .filter(
            LearningContent.topic_id == topic_id,
            LearningContent.is_active == True
        )
        .order_by(
            LearningContent.content_order
        )
        .all()
    )


    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    return {

        "topic": {

            "id":
                topic.id,

            "title":
                topic.title,

            "description":
                topic.description

        },


        "learning_methods": [

            {

                "id":
                    content.id,

                "resource_type":
                    content.resource_type,

                "title":
                    content.title,

                "description":
                    content.description,

                "content_text":
                    content.content_text,

                "resource_url":
                    content.resource_url,

                "content_order":
                    content.content_order

            }

            for content in contents
        ],


        "total_methods":
            len(contents)

    }