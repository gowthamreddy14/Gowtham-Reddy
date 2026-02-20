# ================= GENERATE LETTER =================

@app.route("/generate", methods=["POST"])
@login_required
def generate():

    job = request.form["job_title"]
    company = request.form["company"]
    details = request.form["details"]

    letter = f"""
Dear Hiring Manager,

I am excited to apply for the {job} position at {company}.

{details}

I am eager to contribute and grow within your organization.

Sincerely,
{current_user.name}
"""

    session["letter"] = letter
    return redirect("/downloads")


@app.route("/downloads")
@login_required
def downloads():
    return render_template("downloads.html", letter=session.get("letter",""))


@app.route("/download/docx")
@login_required
def download_docx():
    doc = Document()
    doc.add_heading("Cover Letter", 0)
    doc.add_paragraph(session.get("letter",""))

    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    return send_file(file_stream,
                     as_attachment=True,
                     download_name="cover_letter.docx")


@app.route("/download/pdf")
@login_required
def download_pdf():
    html = f"<pre>{session.get('letter','')}</pre>"
    pdf = pdfkit.from_string(html, False)

    return send_file(io.BytesIO(pdf),
                     as_attachment=True,
                     download_name="cover_letter.pdf")
