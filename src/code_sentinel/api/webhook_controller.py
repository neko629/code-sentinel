import logging

from fastapi import APIRouter, BackgroundTasks, Header, HTTPException, Request

from code_sentinel.core.git_service import git_service
from code_sentinel.core.review_service import review_service
from code_sentinel.utils.crypto_utils import verify_signature
from code_sentinel.core.database import add_feedback

router = APIRouter()
logger = logging.getLogger(__name__)

async def process_comment_event(payload: dict):
    """
    handle user feedback
    :param payload:
    :return:
    """
    comment = payload.get("comment", {})
    body = comment.get("body", "").lower()

    triggers = [
        "false positive",
        "wrong",
        "误报"
    ]

    if not any(t in body for t in triggers):
        return

    logger.info(">>>> [User Feedback] 收到用户反馈, 正在记录...")

    diff_hunk = comment.get("diff_hunk", "")
    path = comment.get("path", "")

    add_feedback(
        file_path=path,
        code=diff_hunk,
        comment="AI Previous Comment", # TODO: get ai comment by github API
        feedback=body
    )
    logger.info(">>>> [User Feedback] 反馈记录完成.")

async def process_pr_event(payload: dict):
    """
    async task
    :param payload:
    :return:
    """

    try:
        pr_number = payload["pull_request"]["number"]
        repo_name = payload["repository"]["full_name"]
        action = payload["action"]

        logger.info(f"start to process PR event: "
                    f"{action} for PR #{pr_number} in repo {repo_name}")

        # git diff
        diff_content = git_service.get_pr_diff(repo_name, pr_number)

        # TODO: handle huge diff, substring it temporarily
        if len(diff_content) > 10000:
            diff_content = (diff_content[:10000]
                            + "\n\n... Diff truncated due to size ...\n\n")
        # call review service
        ai_comment = await review_service.review_code_async(diff_content, language='Python')
        # post review comment
        git_service.post_comment(repo_name, pr_number, ai_comment)
        logger.info(f"finish to process PR event: "
                    f"{action} for PR #{pr_number} in repo {repo_name}")
    except Exception as e:
        logger.error(f"failed to process PR event: {payload}, error: {str(e)}"
                     , exc_info=True)


@router.post("/webhook")
async def handle_github_webhook(
        request: Request,
        background_tasks: BackgroundTasks,
        x_hub_signature_256: str = Header(None)
):
    """receive github webhook event"""
    body_bytes = await request.body()

    if not verify_signature(body_bytes, x_hub_signature_256):
        logger.error("signature verification failed")
        raise HTTPException(status_code=400, detail="signature verification failed")

    payload = await request.json()

    # filter event, only handle opened and synchronize event
    event_type = request.headers.get("X-GitHub-Event")
    action = payload.get("action")

    if event_type == "pull_request" and action in ["opened", "synchronize"]:
        logger.info(f"receive pr event, type: {action}")
        background_tasks.add_task(process_pr_event, payload)
    elif event_type == "pull_request_review_comment" and payload.get("action") == "created":
        background_tasks.add_task(process_comment_event, payload)
    else:
        logger.info(f"ignore event type: {event_type}, action: {action}")

    return {"status": "accepted"}
