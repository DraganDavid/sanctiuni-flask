from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fines.db"
db = SQLAlchemy(app)


class Fine(db.Model):
    __tablename__ = "fine"
    id: Mapped[int] = mapped_column(primary_key=True)
    abatere: Mapped[str] = mapped_column(String(100))
    data: Mapped[str] = mapped_column(String(100))
    autoritate: Mapped[str] = mapped_column(String(100))


@app.post("/fines")
def create():
    global id_fine
    abatere = request.json.get("abatere")
    data = request.json.get("data")
    autoritate = request.json.get("autoritate")
    new_fine = Fine(abatere=abatere, data=data, autoritate=autoritate)
    db.session.add(new_fine)
    db.session.commit()
    return {"mesage": "you've introduced a new fine"}, 201


@app.get("/fines")
@app.get("/fines/<int:id>")
def read(id=None):
    if id is None:
        all_fines = Fine.query.all()
        serialized_fines = []
        for element in all_fines:
            serialized_fines.append(
                {
                    "id": element.id,
                    "abatere": element.abatere,
                    "data": element.data,
                    "autoritate": element.autoritate,
                }
            )
        return serialized_fines
    else:
        fine = Fine.query.get(id)
        if fine:
            return {
                "id": fine.id,
                "abatere": fine.abatere,
                "data": fine.data,
                "autoritate": fine.autoritate,
            }
        else:
            return {"mesage": "fine not found"}, 404


@app.put("/fines/<int:id>")
def update(id):
    abatere = request.json.get("abatere")
    data = request.json.get("data")
    autoritate = request.json.get("autoritate")
    fine = Fine.query.get(id)
    if fine:
        fine.abatere = abatere
        fine.data = data
        fine.autoritate = autoritate
        db.session.commit()
        return {"mesage": "fine updates"}, 200
    else:
        return {"mesage": "fine not found"}, 404


@app.delete("/fines/<int:id>")
def delete(id):
    fine = Fine.query.get(id)
    if fine:
        db.session.delete(fine)
        db.session.commit()
        return {"mesage": "fine deleted"}, 200
    else:
        return {"mesage": "fine not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)
