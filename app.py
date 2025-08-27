from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "dev"

posts = [
    {
        "id": 1,
        "title": "İlk Yazım",
        "content": "Merhaba dünya! Bu mini blog çalışıyor.",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
]

def next_id():
    return max([p["id"] for p in posts], default=0) + 1

@app.context_processor
def inject_now():
    return {"now": datetime.now}

@app.route("/")
def home():
    ordered = sorted(posts, key=lambda p: p["created_at"], reverse=True)
    return render_template("home.html", posts=ordered)

@app.route("/post/<int:post_id>")
def detail(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        flash("Yazı bulunamadı", "error")
        return redirect(url_for("home"))
    return render_template("detail.html", post=post)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if not title or not content:
            flash("Başlık ve içerik zorunlu", "error")
            return render_template("form.html", mode="create", post={"title": title, "content": content})
        new_post = {
            "id": next_id(),
            "title": title,
            "content": content,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        posts.append(new_post)
        flash("Yazı oluşturuldu", "success")
        return redirect(url_for("detail", post_id=new_post["id"]))
    return render_template("form.html", mode="create", post={})

@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit(post_id):
    post = next((p for p in posts if p["id"] == post_id), None)
    if not post:
        flash("Yazı bulunamadı", "error")
        return redirect(url_for("home"))
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        if not title or not content:
            flash("Başlık ve içerik zorunlu", "error")
            return render_template("form.html", mode="edit", post=post)
        post["title"] = title
        post["content"] = content
        post["updated_at"] = datetime.now()
        flash("Yazı güncellendi", "success")
        return redirect(url_for("detail", post_id=post_id))
    return render_template("form.html", mode="edit", post=post)

@app.route("/delete/<int:post_id>", methods=["POST"])
def delete(post_id):
    global posts
    before = len(posts)
    posts = [p for p in posts if p["id"] != post_id]
    flash("Yazı silindi" if len(posts) < before else "Yazı bulunamadı", "success" if len(posts) < before else "error")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
