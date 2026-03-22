import urllib.request
import urllib.parse
import json
import time
import sys

# Search terms: (artist, title) -> search query for Wikipedia
artworks = [
    ("Berlinghieri", "Saint Francis Altarpiece Berlinghieri"),
    ("Cimabue", "Cimabue Madonna Enthroned Santa Trinita"),
    ("Giotto", "Giotto Madonna Enthroned Ognissanti"),
    ("Giotto", "Giotto Lamentation Arena Chapel"),
    ("Giotto", "Giotto Entry into Jerusalem Arena Chapel"),
    ("Giotto", "Giotto Betrayal of Jesus Arena Chapel"),
    ("Duccio", "Duccio Maestà front"),
    ("Duccio", "Duccio Betrayal of Jesus Maestà"),
    ("Simone Martini", "Simone Martini Annunciation 1333"),
    ("Pietro Lorenzetti", "Pietro Lorenzetti Birth of the Virgin"),
    ("Ambrogio Lorenzetti", "Ambrogio Lorenzetti Allegory Good Government"),
    ("Claus Sluter", "Claus Sluter Well of Moses"),
    ("Limbourg Brothers", "Très Riches Heures January"),
    ("Robert Campin", "Mérode Altarpiece"),
    ("Jan van Eyck", "Ghent Altarpiece open"),
    ("Jan van Eyck", "Arnolfini Portrait"),
    ("Jan van Eyck", "Man in a Red Turban van Eyck"),
    ("Rogier van der Weyden", "Rogier van der Weyden Deposition"),
    ("Rogier van der Weyden", "Rogier van der Weyden Saint Luke Drawing Virgin"),
    ("Dirk Bouts", "Dirk Bouts Last Supper"),
    ("Hugo van der Goes", "Portinari Altarpiece"),
    ("Hans Memling", "Hans Memling Virgin Saints Angels Saint John Altarpiece"),
    ("Jean Fouquet", "Melun Diptych"),
    ("Konrad Witz", "Konrad Witz Miraculous Draft Fish"),
    ("Veit Stoss", "Veit Stoss Assumption Virgin Kraków"),
    ("Martin Schongauer", "Schongauer Saint Anthony Tormented Demons"),
    ("Brunelleschi", "Brunelleschi Sacrifice Isaac competition"),
    ("Ghiberti", "Ghiberti Sacrifice Isaac competition"),
    ("Donatello", "Donatello Saint Mark Orsanmichele"),
    ("Donatello", "Donatello Saint George Orsanmichele"),
    ("Donatello", "Donatello Feast of Herod Siena"),
    ("Ghiberti", "Gates of Paradise Florence Baptistery"),
    ("Donatello", "Donatello David bronze"),
    ("Verrocchio", "Verrocchio David bronze"),
    ("Pollaiuolo", "Pollaiuolo Hercules Antaeus bronze"),
    ("Donatello", "Donatello Gattamelata Padua"),
    ("Verrocchio", "Verrocchio Bartolomeo Colleoni Venice"),
    ("Gentile da Fabriano", "Gentile da Fabriano Adoration Magi"),
    ("Masaccio", "Masaccio Tribute Money Brancacci"),
    ("Masaccio", "Masaccio Expulsion Adam Eve Brancacci"),
    ("Masaccio", "Masaccio Holy Trinity Santa Maria Novella"),
    ("Fra Angelico", "Fra Angelico Annunciation San Marco"),
    ("Andrea del Castagno", "Castagno Last Supper"),
    ("Paolo Uccello", "Uccello Battle San Romano"),
    ("Fra Filippo Lippi", "Fra Filippo Lippi Madonna Child Angels"),
    ("Piero della Francesca", "Piero della Francesca Resurrection"),
    ("Ghirlandaio", "Ghirlandaio Birth Virgin Santa Maria Novella"),
    ("Botticelli", "Botticelli Primavera"),
    ("Botticelli", "Birth of Venus Botticelli"),
    ("Perugino", "Perugino Christ Delivering Keys Sistine"),
    ("Signorelli", "Signorelli Damned Cast Hell Orvieto"),
    ("Piero della Francesca", "Piero della Francesca Flagellation"),
    ("Piero della Francesca", "Piero della Francesca Battista Sforza Federico Montefeltro"),
    ("Brunelleschi", "Ospedale degli Innocenti Florence"),
    ("Brunelleschi", "San Lorenzo interior Florence Brunelleschi"),
    ("Alberti", "Sant'Andrea Mantua Alberti"),
    ("Mantegna", "Mantegna Camera degli Sposi ceiling oculus"),
    ("Mantegna", "Mantegna Lamentation Dead Christ foreshortened"),
    ("Giovanni Bellini", "Giovanni Bellini Saint Francis Desert"),
    ("Leonardo", "Leonardo Madonna Rocks"),
    ("Leonardo", "Leonardo Last Supper Milan"),
    ("Leonardo", "Mona Lisa Leonardo"),
    ("Raphael", "Raphael Marriage Virgin Sposalizio"),
    ("Raphael", "Raphael Madonna Meadows"),
    ("Raphael", "Raphael School Athens Vatican"),
    ("Raphael", "Raphael Galatea Villa Farnesina"),
    ("Michelangelo", "Michelangelo Pietà Saint Peters"),
    ("Michelangelo", "Michelangelo David Florence"),
    ("Michelangelo", "Michelangelo Moses San Pietro Vincoli"),
    ("Michelangelo", "Michelangelo Tomb Giuliano Medici"),
    ("Michelangelo", "Sistine Chapel ceiling Michelangelo"),
    ("Michelangelo", "Michelangelo Last Judgment Sistine"),
    ("Bramante", "Bramante Tempietto San Pietro Montorio"),
    ("Michelangelo", "Saint Peter's Basilica dome Michelangelo"),
    ("Michelangelo", "Laurentian Library vestibule Michelangelo"),
    ("Giovanni Bellini", "Giovanni Bellini San Zaccaria Altarpiece"),
    ("Giorgione", "Giorgione Tempest painting"),
    ("Titian", "Titian Assumption Virgin Frari"),
    ("Titian", "Titian Pesaro Madonna"),
    ("Titian", "Titian Venus Urbino"),
    ("Correggio", "Correggio Assumption Virgin Parma Cathedral"),
    ("Pontormo", "Pontormo Deposition Entombment"),
    ("Parmigianino", "Parmigianino Madonna Long Neck"),
    ("Parmigianino", "Parmigianino Self-Portrait Convex Mirror"),
    ("Bronzino", "Bronzino Venus Cupid Folly Time"),
    ("Bronzino", "Bronzino Eleonora Toledo"),
    ("Sofonisba Anguissola", "Sofonisba Anguissola Portrait Sisters Brother"),
    ("Tintoretto", "Tintoretto Last Supper San Giorgio"),
    ("Veronese", "Veronese Feast House Levi"),
    ("Cellini", "Cellini Saltcellar Francis"),
    ("Giambologna", "Giambologna Abduction Sabine Women"),
    ("Giulio Romano", "Giulio Romano Palazzo Te Fall Giants"),
    ("Palladio", "Villa Rotonda Palladio"),
    ("Palladio", "San Giorgio Maggiore Palladio Venice"),
    ("Vignola", "Il Gesù Rome facade"),
    ("El Greco", "El Greco Burial Count Orgaz"),
    ("El Greco", "El Greco View Toledo"),
    ("Dürer", "Albrecht Dürer Self-Portrait 1500"),
    ("Dürer", "Dürer Adam Eve Fall Man engraving"),
    ("Dürer", "Dürer Melencolia I"),
    ("Dürer", "Dürer Four Apostles"),
    ("Grünewald", "Grünewald Isenheim Altarpiece crucifixion"),
    ("Holbein", "Holbein Ambassadors painting"),
    ("Holbein", "Holbein Henry VIII portrait"),
    ("Bruegel", "Bruegel Hunters Snow"),
    ("Maderno", "Carlo Maderno Santa Susanna facade Rome"),
    ("Maderno", "Saint Peter's Basilica facade Maderno"),
    ("Bernini", "Bernini colonnade Saint Peter's Square"),
    ("Bernini", "Bernini Baldacchino Saint Peters"),
    ("Bernini", "Bernini David sculpture"),
    ("Bernini", "Bernini Ecstasy Saint Teresa"),
    ("Bernini", "Bernini Fountain Four Rivers Piazza Navona"),
    ("Borromini", "Borromini San Carlo Quattro Fontane"),
    ("Borromini", "Borromini Sant'Ivo Sapienza"),
    ("Guarini", "Guarini Chapel Holy Shroud Turin dome"),
    ("Carracci", "Annibale Carracci Flight Egypt landscape"),
    ("Carracci", "Annibale Carracci Palazzo Farnese ceiling"),
    ("Caravaggio", "Caravaggio Calling Saint Matthew"),
    ("Caravaggio", "Caravaggio Conversion Saint Paul"),
    ("Gentileschi", "Artemisia Gentileschi Judith Slaying Holofernes"),
    ("Gentileschi", "Artemisia Gentileschi Self-Portrait Allegory Painting"),
    ("Gaulli", "Gaulli Triumph Name Jesus ceiling Gesù"),
    ("Pozzo", "Andrea Pozzo Glorification Saint Ignatius ceiling"),
    ("Ribera", "Jusepe Ribera Martyrdom Saint Philip"),
    ("Zurbarán", "Zurbarán Saint Serapion"),
    ("Velázquez", "Velázquez Water Carrier Seville"),
    ("Velázquez", "Velázquez Surrender Breda"),
    ("Velázquez", "Las Meninas Velázquez"),
    ("Murillo", "Murillo Immaculate Conception Escorial"),
    ("Claesz", "Pieter Claesz Vanitas Still Life"),
    ("Rubens", "Rubens Elevation Cross Antwerp"),
    ("Rubens", "Rubens Consequences War"),
    ("Rubens", "Rubens Arrival Marie Medici Marseilles"),
    ("Van Dyck", "Anthony van Dyck Charles I Hunt"),
    ("Peeters", "Clara Peeters Still Life Flowers Goblet"),
    ("Ter Brugghen", "Ter Brugghen Calling Saint Matthew"),
    ("Honthorst", "Honthorst Supper Party painting"),
    ("Hals", "Frans Hals Archers Saint Hadrian"),
    ("Hals", "Frans Hals Women Regents Old Men Home"),
    ("Leyster", "Judith Leyster Self-Portrait"),
    ("Rembrandt", "Rembrandt Anatomy Lesson Dr Tulp"),
    ("Rembrandt", "Rembrandt Night Watch"),
    ("Rembrandt", "Rembrandt Return Prodigal Son"),
    ("Rembrandt", "Rembrandt Self-Portrait 1660"),
    ("Rembrandt", "Rembrandt Hundred Guilder Print"),
    ("Cuyp", "Aelbert Cuyp Distant View Dordrecht"),
    ("Ruisdael", "Ruisdael View Haarlem Dunes Overveen"),
    ("Vermeer", "Vermeer Woman Holding Balance"),
    ("Vermeer", "Vermeer Art Painting Allegory"),
    ("Steen", "Jan Steen Feast Saint Nicholas"),
    ("Kalf", "Willem Kalf Still Life Ming Ginger Jar"),
    ("Ruysch", "Rachel Ruysch Flower Still Life"),
    ("Rigaud", "Hyacinthe Rigaud Louis XIV portrait"),
    ("Poussin", "Poussin Et in Arcadia Ego"),
    ("Poussin", "Poussin Landscape Saint John Patmos"),
    ("Claude Lorrain", "Claude Lorrain Landscape Cattle Peasants"),
    ("Le Nain", "Louis Le Nain Family Country People"),
    ("Callot", "Jacques Callot Hanging Tree Miseries War"),
    ("La Tour", "Georges La Tour Adoration Shepherds"),
    ("Inigo Jones", "Inigo Jones Banqueting House Whitehall"),
    ("Wren", "Christopher Wren Saint Paul Cathedral London"),
    ("Versailles", "Palace Versailles aerial"),
    ("Hall of Mirrors", "Galerie Glaces Hall Mirrors Versailles"),
    ("Girardon", "Girardon Apollo Nymphs Thetis Versailles"),
    ("Hardouin-Mansart", "Église Dôme Invalides Paris"),
    ("Louvre", "East facade Louvre colonnade Perrault"),
    ("Versailles Chapel", "Royal Chapel Versailles interior"),
]

results = {}
for i, (artist, query) in enumerate(artworks):
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded}&srnamespace=6&srlimit=1&format=json"
        req = urllib.request.Request(url, headers={"User-Agent": "ARTH201StudyGuide/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            if data.get("query", {}).get("search"):
                file_title = data["query"]["search"][0]["title"]
                # Get the actual image URL
                url2 = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(file_title)}&prop=imageinfo&iiprop=url&iiurlwidth=600&format=json"
                req2 = urllib.request.Request(url2, headers={"User-Agent": "ARTH201StudyGuide/1.0"})
                with urllib.request.urlopen(req2, timeout=5) as resp2:
                    data2 = json.loads(resp2.read())
                    pages = data2.get("query", {}).get("pages", {})
                    for page in pages.values():
                        ii = page.get("imageinfo", [{}])[0]
                        thumb = ii.get("thumburl", ii.get("url", ""))
                        if thumb:
                            results[f"{artist}|{query}"] = thumb
                            print(f"[{i+1}/{len(artworks)}] OK: {artist}", file=sys.stderr)
                        else:
                            # Try commons directly
                            url3 = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={encoded}&srnamespace=6&srlimit=1&format=json"
                            req3 = urllib.request.Request(url3, headers={"User-Agent": "ARTH201StudyGuide/1.0"})
                            with urllib.request.urlopen(req3, timeout=5) as resp3:
                                data3 = json.loads(resp3.read())
                                if data3.get("query", {}).get("search"):
                                    file_title3 = data3["query"]["search"][0]["title"]
                                    url4 = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(file_title3)}&prop=imageinfo&iiprop=url&iiurlwidth=600&format=json"
                                    req4 = urllib.request.Request(url4, headers={"User-Agent": "ARTH201StudyGuide/1.0"})
                                    with urllib.request.urlopen(req4, timeout=5) as resp4:
                                        data4 = json.loads(resp4.read())
                                        pages4 = data4.get("query", {}).get("pages", {})
                                        for p4 in pages4.values():
                                            ii4 = p4.get("imageinfo", [{}])[0]
                                            thumb4 = ii4.get("thumburl", ii4.get("url", ""))
                                            if thumb4:
                                                results[f"{artist}|{query}"] = thumb4
                                                print(f"[{i+1}/{len(artworks)}] OK (commons): {artist}", file=sys.stderr)
                                            else:
                                                results[f"{artist}|{query}"] = ""
                                                print(f"[{i+1}/{len(artworks)}] MISS: {artist}", file=sys.stderr)
                                else:
                                    results[f"{artist}|{query}"] = ""
                                    print(f"[{i+1}/{len(artworks)}] MISS: {artist}", file=sys.stderr)
            else:
                results[f"{artist}|{query}"] = ""
                print(f"[{i+1}/{len(artworks)}] MISS: {artist}", file=sys.stderr)
    except Exception as e:
        results[f"{artist}|{query}"] = ""
        print(f"[{i+1}/{len(artworks)}] ERROR: {artist} - {e}", file=sys.stderr)
    time.sleep(1.0)

# Output as JSON
print(json.dumps(results, indent=2))
