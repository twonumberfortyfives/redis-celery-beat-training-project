from celery import shared_task
import requests
import uuid

from django.db import transaction

from celeryredistraining import settings
from main.models import Cat
import logging

logger = logging.getLogger(__name__)

CAT_URL = "https://thecatapi.com/api/images/get?format=src&type=jpeg"


@shared_task
def download_a_cat():
    try:
        response = requests.get(CAT_URL)
        response.raise_for_status()  # Raise an error for bad status codes
        file_extension = response.headers.get('Content-Type').split("/")[1]
        file_name = settings.BASE_DIR / "media" / f"{uuid.uuid4()}.{file_extension}"

        logger.info("Attempting to create Cat object")
        cat = Cat.objects.create(url=str(file_name))
        logger.info(f"Cat object created with ID: {cat.id}")

        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        return True
    except requests.RequestException as e:
        print(f"Error downloading cat image: {e}")
        return False

@shared_task
def process_measurement(measurement):
    print(f"Processing measurement: {measurement}")
