from PIL import Image as PILImage, ImageDraw
import io
import zipfile
from datetime import datetime
import base64


def format_survey_results(survey, responses):
    formatted_text = f"Survey Results: {survey.name}\n"
    formatted_text += (
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    )

    for i, response in enumerate(responses, 1):
        formatted_text += f"Participant {i}\n{'='*50}\n"

        # Access answers from the dictionary
        for question in survey.questions:
            q_id = str(survey.questions.index(question))  # Get question index as string
            answer = response.answers.get(q_id)  # Get answer using question index

            formatted_text += f"\nQuestion {int(q_id) + 1}: {question['text']}\n"

            if question["type"] == "ImageQuestion":
                formatted_text += f"Image coordinates saved in: participant_{i}_question_{int(q_id) + 1}.jpg\n"
            else:
                formatted_text += f"Answer: {answer}\n"

        formatted_text += "\n\n"

    return formatted_text


def process_image_responses(survey, responses, image_data):
    print(f"Processing images for survey: {survey.name}")
    print(f"Number of responses: {len(responses)}")
    print(f"Number of available images: {len(image_data)}")

    image_files = []

    for i, response in enumerate(responses, 1):
        for q_idx, question in enumerate(survey.questions):
            if question["type"] == "ImageQuestion":
                answer = response.answers.get(str(q_idx))
                if not answer:
                    continue

                image_name = question["imageName"]
                img_record = next(
                    (img for img in image_data if img.image_name == image_name), None
                )

                if img_record and isinstance(answer, list):
                    img = PILImage.open(io.BytesIO(img_record.image_data))
                    draw = ImageDraw.Draw(img)

                    # Draw all points in the answer list
                    point_size = 5
                    for point in answer:
                        if isinstance(point, dict) and "x" in point and "y" in point:
                            draw.ellipse(
                                [
                                    point["x"] - point_size,
                                    point["y"] - point_size,
                                    point["x"] + point_size,
                                    point["y"] + point_size,
                                ],
                                fill="red",
                            )

                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format="JPEG", optimize=True, quality=85)

                    image_files.append(
                        {
                            "filename": f"participant_{i}_question_{q_idx + 1}.jpg",
                            "data": img_byte_arr.getvalue(),
                        }
                    )

    return image_files


def create_results_package(survey, responses, images):
    print("\nCreating results package")
    result_text = format_survey_results(survey, responses)
    image_files = process_image_responses(survey, responses, images)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("results.txt", result_text)
        for img in image_files:
            zip_file.writestr(img["filename"], img["data"])

    has_images = len(image_files) > 0
    print(f"Package created with {len(image_files)} images, has_images={has_images}")

    return {
        "text": result_text,
        "zip_data": base64.b64encode(zip_buffer.getvalue()).decode("utf-8"),
        "has_images": has_images,
    }
