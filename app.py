import os

from flask import (
    Flask,
    render_template,
    request
)

from werkzeug.utils import secure_filename

from PyPDF2 import PdfReader

from matcher import calculate_match, rank_candidates
from database import init_db, save_analysis, get_history


app = Flask(__name__)


UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf"}


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

init_db()


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


def extract_pdf_text(filepath):

    reader = PdfReader(filepath)

    text_parts = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text_parts.append(page_text)

    if not text_parts:
        return ""

    return "\n".join(text_parts) + "\n"


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    resume = request.files.get(
        "resume"
    )

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()


    if not resume:

        return "Please upload a resume."


    if not allowed_file(
        resume.filename
    ):

        return (
            "Only PDF files are "
            "currently supported."
        )


    if not job_description:

        return (
            "Please enter a job description."
        )


    filename = secure_filename(
        resume.filename
    )


    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )


    resume.save(filepath)


    resume_text = extract_pdf_text(
        filepath
    )


    if not resume_text.strip():

        return (
            "Could not extract text "
            "from this PDF."
        )


    result = calculate_match(
        resume_text,
        job_description
    )


    save_analysis(
        filename,
        result
    )


    return render_template(
        "results.html",
        result=result,
        filename=filename
    )

@app.route("/screening")
def screening_page():

    return render_template(
        "screening.html"
    )

@app.route(
    "/screen",
    methods=["POST"]
)
def screen_candidates():

    resumes = request.files.getlist(
        "resumes"
    )

    job_description = request.form.get(
        "job_description",
        ""
    ).strip()


    if not resumes:

        return "Please upload at least one resume."


    if not job_description:

        return "Please enter a job description."


    candidates = []


    for resume in resumes:

        if not resume.filename:

            continue


        if not allowed_file(
            resume.filename
        ):

            continue


        filename = secure_filename(
            resume.filename
        )


        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )


        resume.save(filepath)


        resume_text = extract_pdf_text(
            filepath
        )


        if not resume_text.strip():

            continue


        candidates.append({

            "filename": filename,

            "text": resume_text

        })


    if not candidates:

        return "Could not extract text from the uploaded resumes."


    ranked_candidates = rank_candidates(
        candidates,
        job_description
    )


    return render_template(
        "ranking.html",
        candidates=ranked_candidates,
        job_description=job_description
    )

@app.route("/history")
def history():

    analyses = get_history()

    return render_template(
        "history.html",
        analyses=analyses
    )


if __name__ == "__main__":

    app.run(
        debug=True
    )