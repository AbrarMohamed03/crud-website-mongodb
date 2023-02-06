from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient


app = Flask(__name__)

app.secret_key= 'key'

# Connect to the MongoDB database
client = MongoClient("mongodb://localhost:27017/")
db = client["Ecole202"]

classes = db["classes"]
modules = db["modules"]
stagiaires = db["stagiaires"]

# ------------------------ Show  classes ---------------------------
@app.route("/")
def Index():
    classes_list = []
    for doc in classes.find():
        classes_list.append(doc)
    return render_template("Index.html", classes=classes_list)


# ------------------------ Insert Classes ---------------------------
@app.route("/insertClasse", methods=["POST"])
def insertClasse():
    if request.method == "POST":

        code_classe = request.form["code_classe"]
        Nom_classe = request.form["Nom_classe"]
        Effectif = request.form["Effectif"]

        document = {
            "code_classe": code_classe,
            "Nom_classe": Nom_classe,
            "Effectif": Effectif
        }
        classes.insert_one(document)


        flash('Classe Inserted successfully')

        return redirect(url_for("Index"))


# ------------------------ Update classes ---------------------------
@app.route("/updateClasse", methods=['POST', 'GET'])
def updateClasse():
    if request.method == "POST":
        code_classe = request.form["code_classe"]
        Nom_classe = request.form["Nom_classe"]
        Effectif = request.form["Effectif"]

        update_query = {
            "code_classe": code_classe
        }

        new_values = {
            "$set": {
                "Nom_classe": Nom_classe,
                "Effectif": Effectif
            }
        }


        classes.update_one(update_query, new_values)


        flash('Classe Updated successfully')

        return redirect(url_for("Index"))

    
# ------------------------ Delete classes ---------------------------
@app.route("/deleteClasse/<code_classe>/", methods=['POST', 'GET'])
def deleteClasse(code_classe):
    delete_query = {
        "code_classe": code_classe
    }

    try:
        classes.delete_one(delete_query)
        print("Document deleted successfully.")
    except Exception as e:
        print("Error deleting document:", e)

    flash('Classe Updated successfully')

    return redirect(url_for("Index"))


# ==============================================================================================================================================
# -------------------------------------------- Modules here ------------------------------------------------------------------------------------
# ==============================================================================================================================================

# ------------------------ Show  modules ---------------------------
@app.route("/modules")
def modules():
    modules_list = []
    for doc in modules.find():
        modules_list.append(doc)
    print(modules_list)
    return render_template("module.html", modules=modules_list)




if __name__ == "__main__":
    app.run(debug=True)
