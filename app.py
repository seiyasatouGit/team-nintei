import sqlite3

from flask import Flask, render_template , request, redirect

app = Flask(__name__)

@app.route("/")
def top_get():
    conn = sqlite3.connect("graduationwork.db")
    c = conn.cursor() 

    c.execute("Select id,name,photo from facilities")
    facility_list = []
    for row in c.fetchall():
        facility_list.append({"id":row[0],"name":row[1],"photo":row[2]})
    return render_template("topfacilities.html", facility_list = facility_list)



@app.route("/add/<int:id>", methods=["GET"])
def add_get(id):
    conn = sqlite3.connect("graduationwork.db")
    c = conn.cursor() 

    c.execute("Select name from facilities where id = ?",(id,))
    facility_name = c.fetchone()
    facility_name = facility_name[0]
    c.execute("Select id from facilities where id = ?",(id,))
    facility_id = c.fetchone()
    facility_id = facility_id[0]
    c.close()
    return render_template("review.html", facility_name = facility_name,facility_id = facility_id)


@app.route("/add/<int:id>", methods=["POST"])
def add_post(id):
    name = request.form.get("name")
    comment = request.form.get("comment")
    star = request.form.get("star")
    facility_id = request.form.get("facility_id")
    conn = sqlite3.connect("graduationwork.db")
    c = conn.cursor()

    c.execute("insert into comments values (null, ?,?,?,?)" ,(name,comment,star,facility_id))


    conn.commit()
    c.close()
    return render_template("review.html")



@app.route("/bbs/<int:id>")
def lists(id):
    conn = sqlite3.connect("graduationwork.db")
    c = conn.cursor() 
    c.execute("Select name from facilities where id = ?",(id,))
    facility_name = c.fetchone()
    facility_name = facility_name[0]
    c.execute("Select id, name , comment, star from comments where facility_id = ?",(id,))
    comments_list = []
    for row in c.fetchall():
        comments_list.append({"name":row[1],"comment":row[2],"star":row[3]})

    c.close()



    return render_template("comments_list.html",comments_list = comments_list,facility_name = facility_name)



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True,)