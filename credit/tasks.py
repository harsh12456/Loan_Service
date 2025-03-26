from .models import CreditScore, User
import logging
import asyncio

logger = logging.getLogger(__name__)

async def calculate_credit_score(user_id):
    try:
        user = await asyncio.to_thread(User.objects.get, id=user_id)  
        if user:
            score = (user.annual_income // 1000) + 300
            await asyncio.to_thread(CreditScore.objects.update_or_create, user=user, defaults={'score': score})
            logger.info(f"Credit score calculated for user ID {user.id}: {score}")
        else:
            logger.warning(f"User with ID {user_id} not found")
    except Exception as e:
        logger.error(f"Error calculating credit score for user ID {user_id}: {e}")












