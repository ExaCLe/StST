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


def format_survey_results_html(survey, responses, processed_images):
    html = f"""
    <html>
    <head>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                margin: 2rem;
                line-height: 1.5;
                color: #1f2937;
            }}
            h1 {{ 
                color: #4f46e5;
                font-size: 2.25rem;
                font-weight: bold;
                margin-bottom: 1rem;
            }}
            h2 {{ 
                color: #374151;
                font-size: 1.8rem;
                font-weight: 600;
                margin-top: 2rem;
                margin-bottom: 1rem;
            }}
            h3 {{ 
                color: #4b5563;
                font-size: 1.25rem;
                font-weight: 600;
                margin-top: 1.5rem;
                margin-bottom: 0.75rem;
            }}
            .participant {{ 
                margin: 2.5rem 0; 
                padding: 2rem;
                border: 1px solid #e5e7eb;
                border-radius: 0.75rem;
                background-color: #ffffff;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            .question {{ 
                margin: 1.5rem 0;
                padding-left: 1rem;
                border-left: 4px solid #e5e7eb;
            }}
            .answer {{ 
                margin: 0.75rem 0 1.5rem 1.5rem;
                color: #374151;
                font-size: 1.1rem;
            }}
            .image-response {{ 
                margin: 1.5rem 0;
                text-align: center;
            }}
            img {{ 
                max-width: 800px;
                width: 100%;
                height: auto;
                border-radius: 0.5rem;
                margin: 1rem auto;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <h1>Survey Results: {survey.name}</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    """

    for i, response in enumerate(responses, 1):
        html += f'<div class="participant"><h2>Participant {i}</h2>'

        for question in survey.questions:
            q_id = str(survey.questions.index(question))
            answer = response.answers.get(q_id)

            html += f'<div class="question">'
            html += f'<h3>Question {int(q_id) + 1}: {question["text"]}</h3>'

            if question["type"] == "ImageQuestion":
                # Find corresponding processed image
                image_filename = f"participant_{i}_question_{int(q_id) + 1}.jpg"
                image_data = next(
                    (
                        img["data"]
                        for img in processed_images
                        if img["filename"] == image_filename
                    ),
                    None,
                )

                if image_data:
                    b64_image = base64.b64encode(image_data).decode("utf-8")
                    html += f'<div class="image-response">'
                    html += f'<img src="data:image/jpeg;base64,{b64_image}" alt="Response image" />'
                    html += "</div>"
            else:
                html += f'<div class="answer">{answer}</div>'

            html += "</div>"

        html += "</div>"

    html += "</body></html>"
    return html


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
    result_html = format_survey_results_html(survey, responses, image_files)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("results.txt", result_text)
        zip_file.writestr("results.html", result_html)
        for img in image_files:
            zip_file.writestr(img["filename"], img["data"])

    has_images = len(image_files) > 0

    return {
        "text": result_text,
        "html": result_html,
        "zip_data": base64.b64encode(zip_buffer.getvalue()).decode("utf-8"),
        "has_images": has_images,
    }
