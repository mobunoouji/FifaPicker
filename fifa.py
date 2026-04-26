from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Daftar club
clubs = [
    # Inggris (Premier League)
    "Liverpool", "Manchester United", "Manchester City", "Chelsea",
    "Arsenal", "Tottenham Hotspur", "Newcastle United", "Aston Villa",
    "Everton", "Leicester City", "Nottingham Forest", "Crystal Palace", "Brighton & Hove Albion",

    # Spanyol (La Liga)
    "Barcelona", "Real Madrid", "Atletico Madrid", "Sevilla",
    "Valencia", "Villarreal", "Real Sociedad", "Athletic Bilbao",
    "Real Betis",

    # Italia (Serie A)
    "Juventus", "Inter Milan", "AC Milan", "AS Roma",
    "Napoli", "Lazio", 

    # Jerman (Bundesliga)
    "Bayern Munich", "Borussia Dortmund", "RB Leipzig", "Bayer Leverkusen",

    # Prancis (Ligue 1)
    "PSG", "Olympique Lyon", "Marseille", "Monaco",

    # Portugal
    "Sporting CP", "Benfica", "Porto",

    # Belanda
    "Ajax", "PSV Eindhoven", "Feyenoord",

    # Turki
    "Galatasaray", "Fenerbahce", "Besiktas"
]


# Daftar formasi
formasi_fifa = ["4-4-2", "4-3-3", "3-5-2", "5-3-2", "4-2-3-1"]

# Daftar pemain per posisi
pemain_posisi = {

    "GK": [
        "Alisson", "Ederson", "Courtois", "Ter Stegen", "Maignan",
        "Onana", "Raya", "Oblak", "Pickford", "Livakovic",
        "Sommer", "Emiliano Martinez", "Kobel", "Trubin",
        "Vicario", "Leno", "Areola", "Meret",
        "Donnarumma", "Mamardashvili"
    ],

    "LB": [
        "Robertson", "Theo Hernandez", "Alphonso Davies", "Grimaldo",
        "Balde", "Chilwell", "Luke Shaw", "Estupiñán",
        "Cucurella", "Tierney", "Gaya",
        "Nuno Mendes", "Destiny Udogie",
        "Miguel Gutierrez", "Fran Garcia",
        "Lucas Digne", "Renan Lodi",
        "Angelino", "Tagliafico", "Mendy"
    ],

    "RB": [
        "Alexander-Arnold", "Reece James", "Hakimi", "Walker",
        "Frimpong", "Cancelo", "Trippier", "Mazraoui",
        "Dumfries", "Di Lorenzo", "Dalot",
        "Pavard", "Pedro Porro", "Mukiele",
        "Malo Gusto", "Ben White",
        "Kounde", "Vanderson", "Carvajal",
        "Aarons"
    ],

    "CB": [
        "Van Dijk", "Ruben Dias", "Militao", "Saliba",
        "Upamecano", "Bastoni", "Lisandro Martinez",
        "Araujo", "Konate", "Gvardiol",
        "Botman", "Timber", "Gabriel Magalhaes",
        "Christensen", "Skriniar", "De Ligt",
        "Kim Min-jae", "Tomori",
        "Badiashile", "Akanji"
    ],

    "CDM": [
        "Rodri", "Declan Rice", "Casemiro", "Kimmich",
        "Tonali", "Caicedo", "Bruno Guimaraes",
        "Locatelli", "Palhinha",
        "Camavinga", "Tchouameni",
        "Zubimendi", "Ugarte",
        "Edson Alvarez", "Hojbjerg",
        "Bissouma", "Guido Rodriguez",
        "Fofana", "Laimer", "Onana"
    ],

    "CM": [
        "De Bruyne", "Pedri", "Bellingham",
        "Valverde", "Enzo Fernandez",
        "Barella", "Modric", "Gundogan",
        "Vitinha", "Szoboszlai",
        "Mac Allister", "Bentancur",
        "Eriksen", "Xhaka",
        "Tielemans", "Kovacic",
        "Frenkie de Jong", "Gravenberch",
        "Loftus-Cheek", "Gallagher"
    ],

    "RM": [
        "Saka", "Chiesa", "Olise",
        "Kulusevski", "Bernardo Silva",
        "Rodrygo", "Ferran Torres",
        "Diaby", "Sancho",
        "Bailey", "Berardi",
        "Politano", "Asensio",
        "Under", "Shaqiri",
        "Raphinha", "Nico Williams",
        "Madueke", "Takefusa Kubo",
        "Doku"
    ],

    "LM": [
        "Vinicius Jr", "Luis Diaz",
        "Son Heung-min", "Rashford",
        "Kvaratskhelia", "Grealish",
        "Coman", "Trossard",
        "Carrasco", "Gnabry",
        "Saint-Maximin", "Mitoma",
        "Leao", "Fati",
        "Mudryk", "Barcola",
        "Nico Williams", "Martinelli",
        "Doku", "Khvicha Kvaratskhelia"
    ],

    "CAM": [
        "Bruno Fernandes", "Odegaard",
        "Wirtz", "Musiala",
        "Paqueta", "Havertz",
        "Eriksen", "Dybala",
        "Mount", "De Ketelaere",
        "Nkunku", "Foden",
        "Julian Brandt", "Maddison",
        "Simons", "Cherki",
        "Kudus", "Reus",
        "Gerson", "Pellegrini"
    ],

    "RW": [
        "Messi", "Salah",
        "Dembele", "Raphinha",
        "Lamine Yamal", "Sterling",
        "Rodrygo", "Chiesa",
        "Kulusevski", "Sancho",
        "Antony", "Bernardo Silva",
        "Ferran Torres", "Politano",
        "Diaby", "Olise",
        "Saka", "Nico Williams",
        "Kubo", "Madueke"
    ],

    "LW": [
        "Mbappe", "Neymar",
        "Leao", "Vinicius Jr",
        "Luis Diaz", "Son",
        "Kvaratskhelia", "Coman",
        "Grealish", "Ansu Fati",
        "Gnabry", "Trossard",
        "Mitoma", "Doku",
        "Mudryk", "Rashford",
        "Saint-Maximin", "Barcola",
        "Martinelli", "Nico Williams"
    ],

    "ST": [
        "Haaland", "Harry Kane",
        "Lautaro Martinez", "Vlahovic",
        "Osimhen", "Darwin Nunez",
        "Griezmann", "Morata",
        "Immobile", "Gabriel Jesus",
        "Richarlison", "Tammy Abraham",
        "Giroud", "Lukaku",
        "Jonathan David", "Isak",
        "Hojlund", "Gyokeres",
        "Ollie Watkins", "Benjamin Sesko"
    ]
}


# Helper mapping formasi → posisi
def formasi_fifa_map(formasi):
    if formasi == "4-4-2":
        return ["GK","LB","RB","CB","CB","CM","CM","LM","RM","ST","ST"]
    elif formasi == "4-3-3":
        return ["GK","LB","RB","CB","CB","CM","CM","CM","LW","RW","ST"]
    elif formasi == "3-5-2":
        return ["GK","CB","CB","CB","LM","RM","CM","CM","CAM","ST","ST"]
    elif formasi == "5-3-2":
        return ["GK","LB","RB","CB","CB","CB","CM","CM","CM","ST","ST"]
    elif formasi == "4-2-3-1":
        return ["GK","LB","RB","CB","CB","CDM","CDM","CAM","LM","RM","ST"]
    return []

# Route menu utama
@app.route("/")
def menu():
    return render_template("menu.html")

# Route pemilihan club
@app.route("/club", methods=["GET", "POST"])
def pilih_club():
    hasil = None
    if request.method == "POST":
        # Mengambil 2 nama klub secara acak dari list 'clubs' yang ada di atas
        clubs_selected = random.sample(clubs, 2)
        
        # Menyusun data dalam bentuk list of dictionaries agar Jinja2 bisa baca hasil[0]['logo']
        hasil = [
            {
                "name": clubs_selected[0], 
                "logo": club_logos.get(clubs_selected[0], "default.png")
            },
            {
                "name": clubs_selected[1], 
                "logo": club_logos.get(clubs_selected[1], "default.png")
            }
        ]
    return render_template("club.html", hasil=hasil)

# Satukan semua data pendukung di satu tempat (atau pastikan sudah ada di atas)
club_logos = {
    "Liverpool": "Liverpool.png",
    "Manchester City": "City.png",
    "Manchester United": "MU.png",
    "Chelsea": "Chelsea.png",
    "Arsenal": "Arsenal.png",
    "Barcelona": "Barcelona.png",
    "Real Madrid": "RM.png",
    "PSG": "PSG.png",
    "Tottenham Hotspur" : "tottenham.png",
    "Aston Villa" : "aston.png",
    "Newcastle United" : "newcastle.png",
    "Everton" : "everton.png",
    "Leicester City" : "leicester.png",
    "Nottingham Forest" : "forest.png",
    "Crystal Palace" : "palace.png",
    "Brighton & Hove Albion" : "albion.png",
    "Atletico Madrid" : "atletico.png",
    "Sevilla" : "sevilla.png",
    "Valencia" : "valencia.png",
    "Villarreal" : "villareal.png",
    "Real Sociedad" : "sociedad.png",
    "Athletic Bilbao" : "bilbao.png",
    "Real Betis" : "betis.png",
    "Juventus" : "juventus.png",
    "Inter Milan" : "inter.png",
    "AC Milan" : "AC.png",
    "AS Roma" : "roma.png",
    "Napoli" : "napoli.png",
    "Lazio" : "lazio.png",
    "Bayern Munich" : "bayern.png",
    "Borussia Dortmund" : "dortmund.png",
    "RB Leipzig" : "leipizig.png",
    "Bayer Leverkusen" : "leverkusen.png",
    "Olympique Lyon" : "lyon.png",
    "Marseille" : "marseille.png", 
    "Monaco" : "monaco.png",
    # Portugal
    "Sporting CP" : "sporting.png",
    "Benfica" : "benfica.png", 
    "Porto" : "porto.png",
    # Belanda
    "Ajax", "PSV Eindhoven", "Feyenoord",
    # Turki
    "Galatasaray", "Fenerbahce", "Besiktas"
    # Tambahkan yang lain di sini...
}

# Route pemilihan player (formasi → generate pemain sesuai formasi, unik antar Player)
@app.route("/player", methods=["GET", "POST"])
def pilih_player():
    hasil = None
    if request.method == "POST":
        formasi1 = request.form.get("formasi1")
        formasi2 = request.form.get("formasi2")

        hasil = {
            "Player 1": [],
            "Player 2": []
        }

        used_players = set()

        # Player 1
        for pos in formasi_fifa_map(formasi1):
            kandidat = [p for p in pemain_posisi[pos] if p not in used_players]
            if kandidat:
                pemain = random.choice(kandidat)
                hasil["Player 1"].append((pos, pemain))
                used_players.add(pemain)
            else:
                hasil["Player 1"].append((pos, "Tidak tersedia"))

        # Player 2
        for pos in formasi_fifa_map(formasi2):
            kandidat = [p for p in pemain_posisi[pos] if p not in used_players]
            if kandidat:
                pemain = random.choice(kandidat)
                hasil["Player 2"].append((pos, pemain))
                used_players.add(pemain)
            else:
                hasil["Player 2"].append((pos, "Tidak tersedia"))

    return render_template("player.html", hasil=hasil, formasi_list=formasi_fifa)

# Route pemilihan pemain (1 posisi → generate 1 pemain tiap player, unik antar Player)
@app.route("/pemain_posisi", methods=["GET", "POST"])
def pilih_pemain_posisi():
    hasil = None
    if request.method == "POST":
        posisi = request.form.get("posisi")

        used_players = set()

        kandidat1 = pemain_posisi[posisi]
        pemain1 = random.choice(kandidat1)
        hasil = {"Player 1": pemain1}
        used_players.add(pemain1)

        kandidat2 = [p for p in pemain_posisi[posisi] if p not in used_players]
        if kandidat2:
            pemain2 = random.choice(kandidat2)
            hasil["Player 2"] = pemain2
        else:
            hasil["Player 2"] = "Tidak tersedia"

    return render_template("pemain_posisi.html", hasil=hasil, posisi_list=pemain_posisi.keys())

# Route pemilihan formasi (random formasi untuk tiap player)
@app.route("/formasi", methods=["GET", "POST"])
def pilih_formasi():
    hasil = None
    if request.method == "POST":
        hasil = {
            "Player 1": random.choice(formasi_fifa),
            "Player 2": random.choice(formasi_fifa)
        }
    return render_template("formasi.html", hasil=hasil)

if __name__ == "__main__":
    app.run(debug=True)

