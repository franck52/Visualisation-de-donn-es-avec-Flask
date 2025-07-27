# Visualisation-de-donn-es-avec-Flask
Tableau de Bord - Analyse des Réseaux Sociaux

Ce projet est une application web développée avec Flask permettant d'analyser les performances des publications sur les réseaux sociaux via des visualisations interactives.

Fonctionnalités

	-Filtrage des données par plateforme et plage de dates
	-Visualisations dynamiques avec Plotly
	-Export du rapport filtré en PDF
	-Moyennes des indicateurs clés : likes, commentaires, partages
	-Répartition des types de publications par jour
	-Nombre total de publications filtrées

Arborescence du projet

.
	 app.py                     # Application principale Flask
	social_media_engagement2.csv  # Données d'entrée
	templates/
  		index.html             # Template principal avec les graphiques
  		export_pdf.html        # Template pour le rendu PDF
	

Lancer l'application

1. Installer les dépendances :

    pip install flask pandas plotly pdfkit

2. Installer wkhtmltopdf pour générer le PDF :
   https://wkhtmltopdf.org/downloads.html

   Ensuite, modifie le chemin dans app.py :

    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

3. Démarrer l'application :

    python app.py

4. Accéder à l'application :

    http://127.0.0.1:5000