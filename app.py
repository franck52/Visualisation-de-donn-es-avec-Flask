import pandas as pd
from flask import Flask, render_template, request, send_file
import plotly.express as px
import plotly.io as pio
import io
import pdfkit

app = Flask(__name__)

# Charger les données CSV
df = pd.read_csv("social_media_engagement2.csv", parse_dates=["post_time"])

# Fonction de filtrage
def get_filtered_data(selected_platform, start_date, end_date):
    data = df.copy()

    if selected_platform and selected_platform != "all":
        data = data[data["platform"] == selected_platform]

    if start_date:
        data = data[data["post_time"] >= pd.to_datetime(start_date)]

    if end_date:
        data = data[data["post_time"] <= pd.to_datetime(end_date)]

    return data

@app.route("/", methods=["GET", "POST"])
def dashboard():
    selected_platform = request.form.get("platform", "all")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    filtered_df = get_filtered_data(selected_platform, start_date, end_date)

    # Graphique 1: Répartition des types de posts
    fig1 = px.pie(filtered_df, names='post_type', title="Répartition des types de publications")
    graph1 = pio.to_html(fig1, full_html=False)

    # Graphique 2: Sentiment
    fig2 = px.histogram(filtered_df, x='sentiment_score', title="Nombre de publications par sentiment")
    graph2 = pio.to_html(fig2, full_html=False)

    # Graphique 3: Moyenne des likes par jour
    likes_by_day = filtered_df.groupby("post_day")["likes"].mean().reset_index()
    fig3 = px.bar(likes_by_day, x='post_day', y='likes', title="Moyenne des likes par jour de la semaine")
    graph3 = pio.to_html(fig3, full_html=False)

    # Graphique 4: Moyenne des partages par plateforme
    shares_by_platform = filtered_df.groupby("platform")["shares"].mean().reset_index()
    fig4 = px.bar(shares_by_platform, x="platform", y="shares", title="Moyenne des partages par plateforme")
    graph4 = pio.to_html(fig4, full_html=False)

    # Graphique 5: Moyenne des commentaires par plateforme
    comments_by_platform = filtered_df.groupby("platform")["comments"].mean().reset_index()
    fig5 = px.bar(comments_by_platform, x="platform", y="comments", title="Moyenne des commentaires par plateforme")
    graph5 = pio.to_html(fig5, full_html=False)

    # Graphique 6: Moyenne des likes par plateforme
    fig6 = px.bar(filtered_df.groupby("platform")["likes"].mean().reset_index(),
                  x="platform", y="likes", title="Moyenne des likes par plateforme")
    graph6 = pio.to_html(fig6, full_html=False)

    # Graphique 7: Types de posts par jour
    # Ordre des jours souhaité
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Convertir 'post_day' en type Categorical avec ordre défini
    filtered_df['post_day'] = pd.Categorical(filtered_df['post_day'], categories=days_order, ordered=True)

    # Regrouper les données
    type_by_day = filtered_df.groupby(['post_day', 'post_type']).size().reset_index(name='count')

    # Tracer le graphique avec l'ordre des jours respecté
    fig7 = px.bar(type_by_day, x='post_day', y='count', color='post_type', barmode='group',
              title="Types de publications par jour",
              category_orders={"post_day": days_order})

    graph7 = pio.to_html(fig7, full_html=False)

    

    graphs = [graph1, graph2, graph3, graph4, graph5, graph6, graph7]

    # Moyennes générales
    avg_stats = {
        #"likes": round(filtered_df["likes"].mean(), 2),
        "likes": round(filtered_df["likes"].mean()),
        "comments": round(filtered_df["comments"].mean()),
        "shares": round(filtered_df["shares"].mean())
    }

    platforms = df["platform"].unique().tolist()
    total_posts = len(filtered_df)


    return render_template("index.html",
                           graphs=graphs,
                           selected_platform=selected_platform,
                           start_date=start_date,
                           end_date=end_date,
                           platforms=platforms,
                           avg_stats=avg_stats,
                           total_posts=total_posts)

@app.route("/export-pdf", methods=["GET"])
def export_pdf():
    selected_platform = request.args.get("platform", "all")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    filtered_df = get_filtered_data(selected_platform, start_date, end_date)

    rendered_html = render_template("export_pdf.html", table_data=filtered_df.to_dict(orient="records"))

    # 🔧 Spécifie ici le chemin vers wkhtmltopdf.exe
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # Si tu utilises WeasyPrint ou xhtml2pdf tu peux compléter ici

    pdf = pdfkit.from_string(rendered_html, False, configuration=config)

    return send_file(io.BytesIO(pdf),
                     mimetype="application/pdf",
                     download_name="rapport.pdf")

if __name__ == "__main__":
    app.run(debug=True)
