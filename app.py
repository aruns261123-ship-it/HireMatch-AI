import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from werkzeug.utils import secure_filename

from PyPDF2 import PdfReader

from matcher import calculate_match, rank_candidates
from database import (
    init_db,
    save_analysis,
    get_history_parsed,
    delete_history
)


app = Flask(__name__)

# Needed for flash messages
app.secret_key = "hirematch-ai-dev-secret-key"


UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf"}

# Reject accidental huge uploads (e.g. a whole folder selected at once)
MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25 MB


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


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
    """
    Extract text from a PDF. Returns an empty string
    instead of crashing on encrypted or corrupt files.
    """

    try:
        reader = PdfReader(filepath)
    except Exception:
        return ""

    text = ""

    for page in reader.pages:

        try:
            page_text = page.extract_text()
        except Exception:
            page_text = None

        if page_text:
            text += page_text + "\n"

    return text


def score_color(score):
    """
    Map a 0-100 match score to a color class
    used for badges and progress bars.
    """

    if score >= 80:
        return "high"
    if score >= 60:
        return "good"
    if score >= 40:
        return "mid"
    return "low"


@app.context_processor
def template_context():
    """
    Expose the active page (for navbar highlighting)
    and the score color helper to all templates.
    """

    path = request.path

    if path.startswith("/screening") or path.startswith("/screen"):
        active_page = "screening"
    elif path.startswith("/history"):
        active_page = "history"
    else:
        active_page = "analyze"

    return {
        "active_page": active_page,
        "score_color": score_color
    }


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


    if not resume or not resume.filename:

        flash(
            "Please upload a resume.",
            "error"
        )
        return redirect(url_for("home"))


    if not allowed_file(
        resume.filename
    ):

        flash(
            "Only PDF files are currently supported.",
            "error"
        )
        return redirect(url_for("home"))


    if not job_description:

        flash(
            "Please enter a job description.",
            "error"
        )
        return redirect(url_for("home"))


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

        flash(
            "Could not extract text from this PDF. "
            "Make sure it is a text-based resume, not a scan.",
            "error"
        )
        return redirect(url_for("home"))


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


    if not job_description:

        flash(
            "Please enter a job description.",
            "error"
        )
        return redirect(url_for("screening_page"))

    if not resumes or all(
        not resume.filename for resume in resumes
    ):

        flash(
            "Please upload at least one resume.",
            "error"
        )
        return redirect(url_for("screening_page"))

    candidates = []
    skipped = []


    candidates = []


    for resume in resumes:

        if not resume.filename:

            continue


        if not allowed_file(
            resume.filename
        ):
            skipped.append(resume.filename)
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
            skipped.append(resume.filename)
            continue


        candidates.append({

            "filename": filename,

            "text": resume_text

        })


    if not candidates:

        flash(
            "Could not extract text from the uploaded resumes. "
            "Make sure they are text-based PDFs.",
            "error"
        )
        return redirect(url_for("screening_page"))


    ranked_candidates = rank_candidates(
        candidates,
        job_description
    )


    return render_template(
        "ranking.html",
        candidates=ranked_candidates,
        job_description=job_description,
        skipped=skipped
    )

@app.route("/history")
def history():

    analyses = get_history_parsed()

    return render_template(
        "history.html",
        analyses=analyses
    )


@app.route(
    "/history/clear",
    methods=["POST"]
)
def clear_history():

    delete_history()

    flash(
        "Analysis history cleared.",
        "success"
    )

    return redirect(url_for("history"))


if __name__ == "__main__":

    app.run(
        debug=os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    )