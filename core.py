from numpy import mean, gcd
from datetime import date
import string, random
from verovio import toolkit
import xml.etree.ElementTree as ET
from IPython import display
import reference

class Note:
    def __init__(self, pitch: int, length: int):
        self.pitch = pitch #0-88
        self.length = length #number of ratoms, or rhythmic atoms. e.g. if the rhythmic atom is a semiquaver, a crotchet has length 16.

    def transpose(self, interval: int):
        out = self.copy()
        out.pitch += interval
        return out

    def __str__(self):
        return f"{self.pitch}({self.length})"

    def copy(self):
        return Note(self.pitch, self.length)

class NotePlus(Note):
    def __init__(self, pitch: int, length: int, tie=False):
        super().__init__(pitch, length)
        self.tie = tie

    def copy(self):
        return NotePlus(self.pitch, self.length, self.tie)

    def __str__(self):
        return super().__str__() + self.tie * "t"

class Piece:
    def __init__(self, notes=None, nvoices=0, ratom=16, metadata={}, vertical = False):
        self.metadata = metadata # e.g {"composer":"JS Bach", "title":"Chorale from Meine Seel erhebt den Herren", "opus": "BWV 10.7"}
        self.notes = notes if notes is not None else [[[]] for _ in range(nvoices)]
        self.bars = [] # e.g if a ratom is a semiquaver and the first bar is a crotchet long: [{"length":4, "n":1},{"length":12, "n":15},{"length":8, "n":1}]
        self.keysigs = [] # e.g. [{"ks":2s, "nbars":16}] for a 16 bar piece in D major with no key changes
        self.timesigs = [] # e.g. [{"ts":[4,4],"nbars":16}]
        self.annotations = {} # e.g. {"fermata":[[48,120],[48,120],[48,120],[48,120]], "dynamics":[{"f":0, "p":4, "dim":[0,4]},{...},{...},{...}], with an object for each part referring to indices of ratoms to which they are assigned
        self.ratom = ratom # the rhythmic atom, i.e. the smallest rhythmic unit used. The numbers are as used in time signatures, i.e. 16 is a semiquaver.
        self.clefs = [] # e.g. [{"shape":"G", "line":2},...]
        self.harm_key = {} # e.g. {"tonic":"g", "mode":"major"}
        self.intervallic = False
        self.vertical = vertical
    
    def copyattribs(self, source):
        self.bars = [bar.copy() for bar in source.bars]
        self.keysigs = [keysig.copy() for keysig in source.keysigs]
        self.harm_key = self.harm_key.copy()
        self.timesigs = [timesig.copy() for timesig in source.timesigs]
        self.clefs = [clef.copy() for clef in source.clefs]
        self.annotations = {k: [item.copy() for item in v] for k, v in source.annotations.items()}
        self.metadata = source.metadata.copy()
        self.ratom = source.ratom
        self.intervallic = source.intervallic
        self.vertical = source.vertical

    def transpose(self, interval: int):
        out = self.copy()
        out.copyattribs(self)
        for i,voice in enumerate(out.notes):
            for j, unit in enumerate(voice):
                for k, note in enumerate(unit):
                    note = self.notes[i][j][k].transpose(interval)
        return out

    def __str__(self):
        out = []
        for i, voice in enumerate(self.notes):
            out.append([])
            for j, sec in enumerate(voice):
                out[i].append([])
                for k, note in enumerate(sec):
                    out[i][j].append(str(note))
        return str(out)

    def copy(self):
        notescopy = [[[note.copy() for note in unit] for unit in voice] for voice in self.notes]
        out = Piece(notescopy)
        out.copyattribs(self)
        return out

    def getlength(self):
        total = 0
        for sec in self.notes[0]:
            for note in sec:
                total += note.length
        return total

    def getkeysigs(self):
        #placeholder: improve later to manage pieces with key signature changes
        out = "0s"
        maxratio = 0
        for ks in reference.diatonics:
            inorout = [0,0]
            for voice in self.notes:
                for unit in voice:
                    for note in unit:
                        if note.pitch in reference.diatonics[ks]:
                            inorout[0] +=1
                        else:
                            inorout[1] +=1
            inoutratio = inorout[0]/inorout[1]
            if inoutratio > maxratio:
                out = ks
                maxratio = inoutratio
        return [{"ks":out,"nbars":100}] #nbars arbitrary, as we assume there is only one key signature for this piece.

    def gettimesigs(self, ratom=16):
        #placeholder: improve later to work out more sensibel time signatures and manage piece with time signature changes
        if len(self.bars) == 0:
            barlength = sum([n.length for n in self.notes[0][1]]) if len(self.notes[0])>1 else sum([n.length for n in self.notes[0][0]])
        elif len(self.bars) == 1 or self.bars[0]["nbars"] != 1:
            barlength = self.bars[0]["length"]
        else:
            barlength = self.bars[1]["length"]
        ts = [barlength,ratom]
        while ts[1] > 4 and gcd(ts[0],ts[1]) > 1:
            ts = [ts[0] // 2,ts[1] // 2]
        return [{"ts":ts,"nbars":100}] #nbars again arbitrary.

    def getclefs(self):
        clefs = []
        for voice in self.notes:
            if mean([mean([n.pitch for n in unit]) for unit in voice]) < 42:
                clefs.append({"shape":"F", "line":4})
            else:
                clefs.append({"shape":"G", "line":2})
        return clefs

    def quantise(self, unitlength=4):
        notescopy = [[[note.copy() for note in unit] for unit in voice] for voice in self.notes]
        for i, voice in enumerate(notescopy):
            while len(voice) > 1:
                voice[0] += voice.pop(1)
            notescopy[i] = voice[0]
        quantised = []
        for i, voice in enumerate(notescopy):
            quantised.append([])
            unit, remainder = [], unitlength
            while len(voice) > 0:
                if voice[0].length == 0:
                    voice.pop(0)
                else:
                    length_to_add = min(remainder, voice[0].length)
                    tied = voice[0].tie if isinstance(voice[0],NotePlus) else voice[0].length > remainder
                    if isinstance(voice[0], NotePlus):
                        tied = voice[0].tie
                    if voice[0].length > remainder:
                        tied = True
                    if len(unit) > 0 and unit[-1].tie:
                        unit[-1].length += length_to_add
                        unit[-1].tie = tied
                    else:
                        unit.append(NotePlus(voice[0].pitch,length_to_add,tied))
                    remainder -= length_to_add
                    voice[0].length -= length_to_add
                    if remainder == 0:
                        quantised[i].append(unit)
                        unit, remainder = [], unitlength
            if sum([n.length for n in quantised[i][-1]]) < remainder:
                unit.append(NotePlus(0,remainder))
                quantised[i].append(unit)
                
        out = Piece(quantised)
        out.copyattribs(source=self)
        return out

    def concat(self, *args):
        out = self.copy()
        for piece in args:
            for i, voice in enumerate(piece.notes):
                self.notes[i].extend([[note.copy() for note in unit] for unit in voice])
        return out

    def addbars(self, bars=None):
        if bars is None:
            bars = self.bars
        quantised = self.quantise(1)
        out = Piece(nvoices=len(self.notes))
        startnote = 0
        for i, section in enumerate(bars):
            endnote = startnote+(section["length"]*section["nbars"])
            curr = Piece([[[note.copy() for note in unit] for unit in voice[startnote:endnote]] for voice in quantised.notes])
            curr = curr.quantise(section["length"])
            startnote = endnote
            if len(out.notes[0][0]) == 0:
                out = curr
            else:
                out.concat(curr)
        out.copyattribs(self)
        return out

    def to_mei(self,ratom=16):
        random.seed(str(self))
        def _idgen(): #generates a random string as an id for each element
            return 'id' + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    
        bars = self.bars if len(self.bars) > 0 else [{"length":sum([n.length for n in self.notes[0][0]]),"nbars":1}]    
        title = "" if "title" not in self.metadata else self.metadata["title"]
        composer = "" if "composer" not in self.metadata else self.metadata["composer"]
        clefs = self.clefs if len(self.clefs) > 0 else getclefs(self)
        keysigs = self.keysigs if len(self.keysigs) > 0 else getkeysigs(self)
        timesigs = self.timesigs if len(self.timesigs) > 0 else gettimesigs(self,ratom)
        harm_key = self.harm_key if len(self.harm_key) > 0 else {"tonic":reference.sigtokeymap[keysigs[0]["ks"]][0],"mode":"major"}
        ties = [False for _ in self.notes]
        
        out = f"""<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://music-encoding.org/schema/5.0/mei-all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<?xml-model href="https://music-encoding.org/schema/5.0/mei-all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"?>
<mei xmlns="http://www.music-encoding.org/ns/mei" meiversion="5.0">
    <meiHead xml:id="{_idgen()}">
        <fileDesc xml:id="{_idgen()}">
            <titleStmt xml:id="{_idgen()}">
                <title>{title}</title>
                <composer>{composer}</composer>
            </titleStmt>
            <pubStmt xml:id="{_idgen()}">
                <date>isodate="{str(date.today())}"></date>
            </pubStmt>
        </fileDesc>
        <encodingDesc xml:id="{_idgen()}">
            <appInfo xml:id="{_idgen()}">
                <application xml:id="{_idgen()}">
                    <name xml:id="{_idgen()}">Dunstaple</name>
                </application>
            </appInfo>
        </encodingDesc>
    </meiHead>
    <music>
        <body>
            <mdiv xml:id="{_idgen()}">
                <score xml:id="{_idgen()}">
                    <scoreDef xml:id="{_idgen()}">
                        <staffGrp xml:id="{_idgen()}" bar.thru="true">
                            <grpSym xml:id="{_idgen()}" symbol="bracket" />"""

        for i, voice in enumerate(self.notes):
            out += f"""
                            <staffDef xml:id="{_idgen()}" n="{i+1}" lines="5">
                                <clef xml:id="{_idgen()}" shape="{clefs[i]["shape"]}" line="{clefs[i]["line"]}" />
                                <keySig xml:id="{_idgen()}" sig="{keysigs[0]["ks"]}" />
                                <meterSig xml:id="{_idgen()}" count="{timesigs[0]["ts"][0]}" unit="{timesigs[0]["ts"][1]}" />
                            </staffDef>"""

        out += f"""
                        </staffGrp>
                    </scoreDef>
                    <section xml:id="{_idgen()}">
                        <pb xml:id="{_idgen()}" />"""
    
        bar_count = 0 if bars[0]["length"] < (ratom // timesigs[0]["ts"][1]) * timesigs[0]["ts"][0] else 1
        for i, bar in enumerate(self.notes[0]):
            currks=keysigs[0]["ks"]
            endbar = """right="end" """ if i == len(self.notes[0])-1 else ""
            out += f"""
                        <measure xml:id="{_idgen()}" {endbar}n="{bar_count}">"""
            for j, voice in enumerate(self.notes):
                out += f"""
                            <staff xml:id="{_idgen()}" n="{j+1}">
                                <layer xml:id="{_idgen()}" n="1">"""
                for k, note in enumerate(voice[i]):
                    if not isinstance(note, NotePlus):
                        note = NotePlus(note.pitch,note.length)
                    [pname,oct,accidges] = pitch_to_scientific(note.pitch).values()
                    [dur,dots] = lentodur(note.length).values()
                    tie_str = """tie="i" """ * note.tie + """tie="t" """ * ties[j]
                    ties[j] = note.tie
                    if note.pitch == 0:
                        out += f"""
                                    <rest xml:id="{_idgen()}" dots="{dots}" dur="{dur}" />"""
                        continue
                    accidges_str, accid_str = "", "/>"
                    need_accid, need_accidges = False, False
                    enharm = enharmonic({"pname":pname,"accid":accidges},ks=currks,mode=harm_key["mode"])
                    pname, accidges = enharm["pname"],enharm["accid"]
                    if (accidges == "s" and currks in reference.all_keysigs["flats"]) or (accidges =="f" and currks in reference.all_keysigs["sharps"]):
                        need_accid = True
                    elif (accidges == "s" and currks in reference.all_keysigs["sharps"]):
                        if pname not in reference.all_keysigs["sharps"][currks]:
                            need_accid = True
                        else:
                            need_accidges = True
                    elif (accidges == "f" and currks in reference.all_keysigs["flats"]):
                        if pname not in reference.all_keysigs["flats"][currks]:
                            need_accid = True
                        else:
                            need_accidges = True
                    elif (accidges == "n" and currks in reference.all_keysigs["flats"]):
                        if pname in reference.all_keysigs["flats"][currks]:
                            need_accid = True
                    elif (accidges == "n" and currks in reference.all_keysigs["sharps"]):
                        if pname in reference.all_keysigs["sharps"][currks]:
                            need_accid = True

                    if need_accidges:
                        accidges_str = f"""accid.ges="{accidges}" """
                    if need_accid:
                        accid_str = f""">
                                        <accid xml:id="{_idgen()}" accid="{accidges}" />
                                    </note>"""
                    out += f"""
                                    <note xml:id="{_idgen()}" dots="{dots}" dur="{dur}" oct="{oct}" pname="{pname}" {tie_str}{accidges_str}{accid_str}"""
                out += f"""
                                </layer>
                            </staff>"""
            out += f"""
                        </measure>"""
        out += f"""
                    </section>
                </score>
            </mdiv>
        </body>
    </music>
</mei>"""

        return out

    def displaysvg(self, bars=None, scale=30, page=1):
        out = self
        if bars is not None:
            out = self.copy().addbars(bars)
        tk = toolkit()
        tk.loadData(to_mei(out))
        tk.setScale(scale)
        return(display.SVG(tk.renderToSVG(page)))

    def getbars(self):
        #assumes at least one bar
        length = sum([n.length for n in self.notes[0][0]])
        out = [{"length": length, "nbars": 1}]
        for unit in self.notes[0]:
            runningtotal = 0
            for note in unit:
                runningtotal += note.length
            if runningtotal == out[-1]["length"]:
                out[-1]["nbars"] += 1
            else:
                out.append({"length":runningtotal, "nbars":1})
        return out

    def to_vertical(self):
        working = self
        if self.intervallic:
            working = self.from_intervallic()
        quantised = working.quantise(1)
        out = []
        for i, unit in enumerate(quantised.notes[0]):
            out.append([])
            for j, note in enumerate(unit):
                out[i].append([quantised.notes[v][i][j] for v in range(len(quantised.notes))])
        piece = Piece(out)
        piece.copyattribs(self)
        piece.vertical = True
        piece.intervallic = False
        return piece

    def to_horizontal(self):
        out = []
        for i, voice in enumerate(self.notes[0][0]):
            out.append([])
            for j, unit in enumerate(self.notes):
                out[i].append([])
                for k, chord in enumerate(unit):
                    out[i][j].append(chord[i].copy())
        piece = Piece(out)
        piece.copyattribs(self)
        piece.vertical = False
        piece.intervallic = False
        return piece

    def to_intervallic(self):
        out = self.copy()
        if self.vertical == False:
            for i, voice in enumerate(out.notes):
                prev_pitch = 0
                for j, unit in enumerate(voice):
                    for k, note in enumerate(unit):
                        if note.pitch == 0:
                            note.pitch = 100
                        else:
                            note.pitch, prev_pitch = note.pitch - prev_pitch, note.pitch
        else:
            nvoices = len(out.notes[0][0])
            for i, unit in enumerate(out.notes):
                for j, chord in enumerate(unit):
                    root = 0
                    for k in range(nvoices-1,-1,-1):
                        if chord[k].pitch == 0:
                            chord[k].pitch = 100
                        elif root == 0:
                            root = chord[k].pitch
                        else:
                            chord[k].pitch = chord[k].pitch - root
                    
        out.intervallic = True
        return out

    
    def from_intervallic(self):
        out = self.copy()
        if self.vertical == False:
            for i, voice in enumerate(out.notes):
                prev_pitch = 0
                for j, unit in enumerate(voice):
                    for k, note in enumerate(unit):
                        if note.pitch == 100:
                            note.pitch = 0
                        else:
                            note.pitch = prev_pitch + note.pitch
                            prev_pitch = note.pitch
        else:
            nvoices = len(out.notes[0][0])
            for i, unit in enumerate(out.notes):
                for j, chord in enumerate(unit):
                    root = 0
                    for k in range(nvoices-1,-1,-1):
                        if chord[k].pitch == 100:
                            chord[k].pitch = 0
                        elif root == 0:
                            root = chord[k].pitch
                        else:
                            chord[k].pitch = root + chord[k].pitch
        out.intervallic = False
        return out




def pitch_from_scientific(note,oct,accid = "n"):
    # translates to the number counting up from A1
    if note == "x":
        return 0
    map = {"c":4, "d":6, "e":8, "f":9, "g":11, "a":13, "b":15}
    basepitch = (oct-1)*12 + map[note]
    if accid == "n":
        return basepitch
    if accid == "s":
        return basepitch + 1
    if accid == "f":
        return basepitch - 1
    if accid == "ss":
        return basepitch + 2
    if accid == "ff":
        return basepitch - 2

def pitch_to_scientific(pitch):
    
    oct = (pitch + 8) // 12
    pname = reference.presumed_chr_scale[(pitch) % 12][0]
    accid = reference.presumed_chr_scale[(pitch) % 12][1]
    return {"pname":pname,"oct":oct,"accid":accid}

def durtolen(dur,dots=0,ratom=16):
    length = ratom * 2 if dur == 0 else ratom // dur
    duplength = length
    for _ in range(dots):
        duplength = duplength // 2
        length += duplength
    return length

def lentodur(note_len,ratom=16):
    if note_len == ratom * 2:
        return {"dur":0, "dots":0}
    dots = 0
    i, n = 0, ratom
    while n >=1:
        if note_len == n:
            break
        if note_len >= n:
            note_len -= n
            dots += 1
        i +=1
        n = n // 2
    dur = ratom // (n * 2 ** dots)                    
    return {"dur": dur,"dots": dots}

def from_mei(path,ratom=16):
    namespace = "{http://www.music-encoding.org/ns/mei}" #all tags will by default have the namespace attached at the front.
    tree = ET.parse(path)
        
    def _reststonotes(tree):
        # changes rests to notes with pname and oct 'x'
        for rest in tree.iter(namespace + 'rest'):
            rest.tag = namespace + 'note'
            rest.set("pname","x")
            rest.set("oct","-1")

    def _addaccidges(tree):
            for note in tree.iter(namespace+'note'):
                accid = note.find(namespace+'accid')
                if accid is not None:
                    val = accid.get('accid')
                    note.set('accid.ges', val)
           
    def _piecefromtree(tree):
        # yet to add functionality for reading metadata from mei
        nvoices=0
        for _ in tree.iter(namespace + 'staffDef'):
            nvoices += 1
        piece = Piece(nvoices=nvoices)
        ties = [False for _ in range(nvoices)]
        for ts in tree.iter(namespace + 'meterSig'):# Hacky. To be changed at some point to deal with pieces with more than one time signature.
            barlength = int(ts.get('count')) * ratom // int(ts.get('unit'))
            break
        rpts = [] #to keep track of repeats in order to copy out repeated notes twice
        for staffn in range(nvoices):
            rpts.append([])
            rptstart = 0
            for measure in tree.iter(namespace + 'measure'):
                if staffn == 0 and measure.get('left') == "rptstart":
                    rptstart = len(piece.notes[staffn][0])
                barrest = True
                for staff in measure.iter(namespace + 'staff'):
                    if int(staff.get('n')) == staffn + 1:
                        for note in staff.iter(namespace + 'note'):
                            barrest = False
                            dots = int(note.get('dots')) if note.get('dots') else 0
                            if ties[staffn]:
                                piece.notes[staffn][0][-1] += durtolen(int(note.get('dur')),dots,ratom)
                                ties[staffn] = False
                            else:
                                accid = note.get('accid.ges') if note.get('accid.ges') else "n"
                                newpitch = pitch_from_scientific(note.get('pname'), int(note.get('oct')), accid)
                                newlength = durtolen(int(note.get('dur')),dots,ratom)
                                piece.notes[staffn][0].append(Note(newpitch,newlength))
                            for tie in measure.iter(namespace + 'tie'):
                                if tie.get('startid') == note.get('id'):
                                    ties[staffn] = True
                                    break
                if measure.get('right') == "rptend":
                    rptendbarend = len(piece.notes[staffn][0])
                    rpts[staffn].append([rptstart, rptendbarend])
                if barrest:
                    piece.notes[staffn][0].append(Note(0, barlength))
        # Duplicate notes in repeated sections
        for i, voice in enumerate(piece.notes):
            for rpt_sec in rpts[i]:
                rpt_endindx = rpt_sec[1]
                voice[0][rpt_endindx:rpt_endindx] = [note.copy() for note in voice[0][rpt_sec[0]:rpt_endindx]]
            
        return piece
    _reststonotes(tree)
    _addaccidges(tree)
    return _piecefromtree(tree)

def enharmonic(sci_pitch,ks,mode="major"):
   
    guessed_tonic = reference.sigtokeymap[ks][0] if mode == "major" else reference.sigtokeymap[ks][1]
    out = dict(sci_pitch)
    note_tuple = (sci_pitch["pname"],sci_pitch["accid"])
    for eq_tuple in reference.enharm_equivs:
        if note_tuple in eq_tuple:
            if reference.leadingnotemap[guessed_tonic] in eq_tuple:
                out["pname"], out["accid"] = reference.leadingnotemap[guessed_tonic][0],reference.leadingnotemap[guessed_tonic][1]
                return out
    if ks in reference.all_keysigs["sharps"]:
        if sci_pitch["accid"] == "f":
            for eq_tuple in reference.enharm_equivs:
                if note_tuple in eq_tuple:
                    ind = eq_tuple.index(note_tuple) - 1
                    out["pname"], out["accid"] = eq_tuple[ind][0], eq_tuple[ind][1]
                    return out
        else:
            return out
    elif ks in reference.all_keysigs["flats"]:
        if sci_pitch["accid"] == "s":
            for eq_tuple in enharm_equivs:
                if note_tuple in eq_tuple:
                    ind = eq_tuple.index(note_tuple) + 1
                    out["pname"], out["accid"] = eq_tuple[ind][0], eq_tuple[ind][1]
                    return out
    return out

