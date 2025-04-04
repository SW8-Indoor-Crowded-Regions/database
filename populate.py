from db.models.room import Room
from db.models.sensor import Sensor
from db.database import Database

db = Database()

# Example adjacency (doors/openings) for the middle rooms from the floor plan.
# Extend as needed for the rest of the rooms on your floor plan.
ROOM_ADJACENCY = {

    # ------------ first floor ------------
    # -- ring wing --
    "RW1": [("T2", (55.688712259492036, 12.579272941514384)), ("T3", (55.68851201358618, 12.57926931660573)), ("KAFETERIA", (55.68850792692439, 12.579062696814656)), ("101", (55.688630526593116, 12.579133382532655)), ("107", (55.68873437832467, 12.579127152387455))],
    "KAFETERIA": [("RW1", (55.68850792692439, 12.579062696814656)), ("HALL", (55.68851232949047, 12.578533085218316))],
    "107": [("RW1", (55.68873437832467, 12.579127152387455)), ("106", (55.688735403124475, 12.579019350623497))],
    "106": [("107", (55.688735403124475, 12.579019350623497)), ("105", (55.688734798352385, 12.578931374167817))],
    "105": [("104", (55.688734798352385, 12.578844470595719)), ("106", (55.688734798352385, 12.578931374167817))],
    "104": [("103", (55.688735403124475, 12.578755421256417)), ("105", (55.688734798352385, 12.578844470595719))],
    "103": [("102", (55.68873419358027, 12.57866959056794)), ("104", (55.688735403124475, 12.578755421256417))],
    "102": [("103", (55.68873419358027, 12.57866959056794)), ("HALL", (55.688735403124475, 12.578558010672939))],
    "101": [("RW1", (55.688630526593116, 12.579133382532655)), ("HALL", (55.688612634195536, 12.578537625884438))],

    # -- middle --
    "HALL": [("T1", (55.68857313325573, 12.57839827681376))],

    # -- left wing --
    "109": [("HALL", (55.688734881889985, 12.577982992731433)), ("LW1", (55.688688919182795, 12.577988357149463))],
    "108": [("HALL", (55.68860969386331, 12.57801410635599)), ("LW1", (55.688613322507386, 12.577483028971043))],
    "SHOP": [("HALL", (55.68850990601874, 12.578011960588787)), ("LW1", (55.68850990601874, 12.577540964685788))],
    "LW1": [("108", (55.688613322507386, 12.577483028971043)), ("109", (55.688688919182795, 12.577988357149463)), ("SHOP", (55.68850990601874, 12.577540964685788))],

    # -- left new building
    "114": [("115", (55.688856828859166, 12.577298768627701))],
    "115": [("113", (55.688867714721646, 12.577603467571818)), ("114", (55.688856828859166, 12.577298768627701)), ("STAGE", (55.68895062337016, 12.57779497007591))],
    "117": [("STAGE", (55.68895062337016, 12.57779497007591))],

    # -- middle new building --
    "STAGE": [("113", (55.68892960883672, 12.578261079263918)), ("115", (55.68895062337016, 12.57779497007591)), ("AUDITORIUM", (55.6890293489383, 12.578597040173408)), ("117", (55.68895062337016, 12.57779497007591))],
    "113": [("HALL", (55.68879832705051, 12.578268737790008)), ("AUDITORIUM", (55.68892895739559, 12.578695745465149)), ("STAGE", (55.68892960883672, 12.578261079263918)), ("115", (55.688867714721646, 12.577603467571818))],

    # -- right new building
    "AUDITORIUM": [("113", (55.68892895739559, 12.578695745465149)), ("STUDYROOM", (55.68894931069138, 12.579027336239466)), ("STAGE", (55.6890293489383, 12.578597040173408))],
    "STUDYROOM": [("T4", (55.68895052022894, 12.579130333065654)), ("AUDITORIUM", (55.68894931069138, 12.579027336239466)), ("113", (55.68886766681934, 12.579027336239466))],

    # ------------ second floor ------------
    # -- Ring wing 2nd floor--
    "201A": [("201B", (55.6886877396403, 12.578685706318554)), ("211B", (55.68869591292594, 12.578569709242808)), ("202", (55.68854777185887, 12.578589646240223)), ("P1", (55.68862848326846, 12.57853708506529))],
    "201B": [("201A", (55.6886877396403, 12.578685706318554)), ("201C", (55.68858557342589, 12.578830702663206))],
    "201C": [("201B", (55.68858557342589, 12.578830702663206)), ("201D", (55.68862133163129, 12.578854264569232))],
    "201D": [("201E", (55.68862133163129, 12.579055446997428)), ("209", (55.68869591292594, 12.579097133446481))],
    "201E": [("201D", (55.68862133163129, 12.579055446997428)), ("204", (55.68854572852991, 12.579098945900828))],
    "202": [("203", (55.68850635390497, 12.578733933320946)), ("201A", (55.68854777185887, 12.578589646240223)), ("P1", (55.68850837916865, 12.578535128578796))],
    "203": [("202", (55.68850635390497, 12.578733933320946)), ("204", (55.688507028992866, 12.578931540444172))],
    "204": [("203", (55.688507028992866, 12.578931540444172)), ("201E", (55.68854572852991, 12.579098945900828)), ("205", (55.688507028992866, 12.579131542805241))],
    "211B": [("201A", (55.68869591292594, 12.578569709242808)), ("211A", (55.68874330904517, 12.578648902377019))],
    "211A": [("211B", (55.68874330904517, 12.578648902377019)), ("210B", (55.6887406087098, 12.578743514272379))],
    "210B": [("211A", (55.6887406087098, 12.578743514272379)), ("210A", (55.68874195887752, 12.578833335692043))],
    "210A": [("209", (55.68874263396135, 12.578927947587397)), ("210B", (55.68874195887752, 12.578833335692043))],
    "208B": [("209", (55.6887406087098, 12.579135135662055)), ("208A", (55.68874195887752, 12.579220166605982)), ("205", (55.68869605314893, 12.579269268982026))],
    "209": [("210A", (55.68874263396135, 12.578927947587397)), ("208B", (55.6887406087098, 12.579135135662055)), ("201D", (55.68869591292594, 12.579097133446481))],
    "208A": [("208B", (55.68874195887752, 12.579220166605982)), ("207", (55.68869605314893, 12.5793806475424)), ("205", (55.688695378064295, 12.579270466600992))],
    "207": [("208A", (55.68869605314893, 12.5793806475424)), ("206", (55.688486101262264, 12.579381845161326)), ("T2", (55.68867242517941, 12.579339928498825)), ("T3", (55.688513104783524, 12.579337533260976))],
    "206": [("207", (55.688486101262264, 12.579381845161326)), ("205", (55.688486101262264, 12.579269268982026))],
    "205": [("206", (55.688486101262264, 12.579269268982026)), ("204", (55.688507028992866, 12.579131542805241)), ("208B", (55.68869605314893, 12.579269268982026)), ("208A", (55.688695378064295, 12.579270466600992))],
    "T2": [("207", (55.68867242517941, 12.579339928498825)), ("RW1", (55.68867242517941, 12.579339928498825))],
    "T3": [("207", (55.688513104783524, 12.579337533260976)), ("RW1", (55.68867242517941, 12.579339928498825))],

    # -- middle passage etc --
    "P1": [("201A", (55.68862848326846, 12.57853708506529)), ("202", (55.68850837916865, 12.578535128578796)), ("212", (55.68869672823357, 12.578501595248802)), ("P2", (55.68867310026443, 12.578493211916298)), ("P3", (55.68848880161522, 12.578493211916298))], #right side of the hall 2nd floor
    "P2": [("P1", (55.68867310026443, 12.578493211916298)), ("P4", (55.68867310026443, 12.578046500055915))], # upper middle of hall 2nd floor
    "P3": [("P1", (55.68848880161522, 12.578493211916298)), ("P4", (55.6884834009091, 12.578047697674839))], # lower middle of hall 2nd floor
    "P4": [("P3", (55.6884834009091, 12.578047697674839)), ("P2", (55.68867310026443, 12.578046500055915)), ("229", (55.68851175460791, 12.57801536196377)), ("217A", (55.68867130762893, 12.578014389939987)), ("216", (55.688696285768444, 12.578052713745718))], # left side of hall 2nd floor
    "212": [("P1", (55.68869672823357, 12.578501595248802)), ("213", (55.68874219149673, 12.57845511370575))],
    "213": [("212", (55.68874219149673, 12.57845511370575)), ("214", (55.688740166245154, 12.578335351812868))],
    "214": [("213", (55.688740166245154, 12.578335351812868)), ("215", (55.68874084132903, 12.578215589920026))],
    "215": [("214", (55.68874084132903, 12.578215589920026)), ("216", (55.68874084132903, 12.578093432789293))],
    "216": [("P4", (55.688696285768444, 12.578052713745718)), ("215", (55.68874084132903, 12.578093432789293))],
    "T1": [("HALL", (12.578438347040734)), ("P1", (55.68861595061425, 12.578464694657182))],

    # -- left wing --
    "217A": [("218A", (55.68869696085306, 12.577956904231435)), ("229", (55.688558568260184, 12.577955706612512)), ("217B", (55.68856869456407, 12.577856304241417)), ("P4", (55.68867130762893, 12.578014389939987))],
    "229": [("217A", (55.688558568260184, 12.577955706612512)), ("P4", (55.68851175460791, 12.57801536196377)), ("228", (55.68851671284295, 12.577810794722144))],
    "228": [("229", (55.68851671284295, 12.577810794722144)), ("227", ())],
    "227": [("228", (55.68851671284295, 12.577617978074615)), ("217F", (55.68855476390886, 12.577450610244458)), ("221", (55.68851560883868, 12.577419472152357))],
    "217F": [("217E", (55.68856826564813, 12.577564384042683)), ("220", (55.68869653193854, 12.577449412625535)), ("227", (55.68855476390886, 12.577450610244458))],
    "217E": [("217F", (55.68856826564813, 12.577564384042683)), ("217D", (55.68862564798797, 12.577691331649149))],
    "217D": [("217E", (55.68862564798797, 12.577691331649149)), ("217C", (55.68868640566773, 12.577711691170938))],
    "217C": [("217D", (55.68868640566773, 12.577711691170938)), ("217B", (55.68862564798797, 12.577727260217031))],
    "217B": [("217C", (55.68862564798797, 12.577727260217031)), ("217A", (55.68856869456407, 12.577856304241417))],
    "218A": [("218B", (55.68874513800182, 12.57790570543735)), ("217A", (55.68869696085306, 12.577956904231435))],
    "218B": [("218A", (55.68874513800182, 12.57790570543735)), ("219", (55.688747838336894, 12.577809895923068))],
    "219": [("218B", (55.688747838336894, 12.577809895923068)), ("220", (55.68874648816937, 12.577621869751278))],
    "220": [("219", (55.68874648816937, 12.577621869751278)), ("217F", (55.68869653193854, 12.577449412625535)), ("P7", (55.688719484809276, 12.577418274533434))],
    "P7": [("220", (55.688719484809276, 12.577418274533434)), ("221", (55.6886958568539, 12.577390729298058)), ("222", (55.68871745955653, 12.577323662638033))],
    "222": [("P7", (55.68871745955653, 12.577323662638033)), ("223", (55.68869855719238, 12.57719192455591))],
    "223": [("221", (55.68868708075257, 12.5772542007402)), ("222", (55.68869855719238, 12.57719192455591)), ("224", (55.68864455038733, 12.577194319793758))],
    "224": [("223", (55.68864455038733, 12.577194319793758)), ("225", (55.68853721164086, 12.577194319793758))],
    "225": [("226", (55.68848117934799, 12.577194319793758)), ("221", (55.68849468111268, 12.577256595978046)), ("224", (55.68853721164086, 12.577194319793758))],
    "221": [("P7", (55.6886958568539, 12.577390729298058)), ("225", (55.68849468111268, 12.577256595978046)), ("223", (55.68868708075257, 12.5772542007402)), ("227", (55.68851425866314, 12.577418274533434))],
    "226": [("225", (55.68848117934799, 12.577194319793758))],

    # -- left new building --
    "P5": [("218A", (55.68875998984243, 12.57795001733774)), ("P8", (55.68894482519272, 12.57791918828427)), ("P9", (55.68894545640952, 12.577986376482954))],
    "P8": [("270B", (55.688932832071394, 12.577835203035875)), ("270A", (55.688932832071394, 12.57761460178341)), ("262", (55.688960605609935, 12.577835203035875)), ("272", (55.688936619373294, 12.577331291545498)), ("261", (55.68895934317679, 12.577406318367414)), ("P5", (55.68894482519272, 12.57791918828427))],
    "T7": [("115", (55.68895871196022, 12.577275301379917)), ("P8", (55.68895871196022, 12.577275301379917))],
    "T6": [("P5", (55.688989010344834, 12.57795054277699)), ("113", (55.688989010344834, 12.57795054277699))],
    "270B": [("P8", (55.688932832071394, 12.577835203035875))],
    "270A": [("P8", (55.688932832071394, 12.57761460178341))],
    "262": [("P8", (55.688960605609935, 12.577835203035875)), ("261", (55.688971336289995, 12.577511579878722))],
    "261": [("P8", (55.68895934317679, 12.577406318367414)), ("262", (55.688971336289995, 12.577511579878722))],
    "272": [("P8", (55.688936619373294, 12.577331291545498)), ("260", (55.68900923026165, 12.577196759546757))],
    "260": [("272", (55.68900923026165, 12.577196759546757))],

    # -- middle new building --
    "P9": [("269A", (55.688927803341805, 12.578110519049302)), ("269B", (55.688927803341805, 12.578485653158799)), ("263B", (55.68895936418357, 12.57811499826254)), ("263C", (55.68895936418357, 12.57842854318984)), ("P6", (55.68894547741635, 12.578565159193912)), ("P5", (55.688948002283496, 12.577988460488285))],
    "269A": [("P9", (55.688927803341805, 12.578110519049302))],
    "269B": [("P9", (55.688927803341805, 12.578485653158799))],
    "263B": [("263C", (55.68897009486398, 12.578302005415585)), ("P9", (55.688927803341805, 12.578485653158799))],
    "263C": [("P9", (55.68895936418357, 12.57842854318984)), ("263B", (55.68897009486398, 12.578302005415585)), ("263A", (55.6890982315847, 12.577992939701522))],
    "263A": [("263C", (55.6890982315847, 12.577992939701522))],

    # -- right new building
    "P6": [("P9", (55.68894547741635, 12.578565159193912)), ("P10", (55.68894769823031, 12.578638891943779)), ("211B", (55.688759595180734, 12.578600818631156))],
    "P10": [("P6", (55.68894769823031, 12.578638891943779)), ("268A", (55.68893318024196, 12.578762070308086)), ("268B", (55.68893128659089, 12.578917722968406)), ("264", (55.688959691347094, 12.578909884345256)), ("267", (55.68893128659089, 12.579058818185757)), ("265", (55.68895263158437, 12.579060948824262)), ("266", (55.68893254103456, 12.579210412838828))],
    "T5": [("P6", (55.6889902203272, 12.578601059548681)), ("113", (55.6889902203272, 12.578601059548681))],
    "T4": [("P10", (55.68896688938762, 12.57925755148957)), ("STUDYROOM", (55.68896688938762, 12.57925755148957))],
    "268A": [("P10", (55.68893318024196, 12.578762070308086))],
    "268B": [("P10", (55.68893128659089, 12.578917722968406))],
    "264": [("P10", (55.688959691347094, 12.578909884345256)), ("264A", (55.68904012256791, 12.578640150137128))],
    "264A": [("264", (55.68904012256791, 12.578640150137128))],
    "267": [("P10", (55.68893128659089, 12.579058818185757))],
    "265": [("P10", (55.68895263158437, 12.579060948824262)), ("266", (55.6890012377105, 12.579109237198203))],
    "266": [("P10", (55.68893254103456, 12.579210412838828)), ("265", (55.6890012377105, 12.579109237198203))],

    # ------------ third floor ------------
    "300": [("300A", (55.6889073960974, 12.577596421279386)), ("300B", (55.68890841775245, 12.577697918720638)), ("300C", (55.68890943940748, 12.577801228616197)), ("T7", (55.6889543922024, 12.577299178772858)), ("T6", (55.68899219337628, 12.577957099686728))],
    "301": [("301A", (55.6889073960974, 12.578125657937365)), ("301B", (55.68890841775245, 12.578227155378576)), ("301C", (55.68890841775245, 12.578330465274174)), ("301D", (55.68890943940748, 12.578435587624039))],
    "302": [("302A", (55.6889073960974, 12.57875276712794)), ("302B", (55.68890841775245, 12.578854264569232)), ("302C", (55.6889073960974, 12.578957574464752)), ("T5", (55.6889901500705, 12.578609583237638)), ("T4", (55.6889758469272, 12.579238504882518))],
    "300A": [("300", (55.6889073960974, 12.577596421279386))],
    "300B": [("300", (55.68890841775245, 12.577697918720638))],
    "300C": [("300", (55.68890943940748, 12.577801228616197))],
    "301A": [("301", (55.6889073960974, 12.578125657937365))],
    "301B": [("301", (55.68890841775245, 12.578227155378576))],
    "301C": [("301", (55.68890841775245, 12.578330465274174))],
    "301D": [("301", (55.68890943940748, 12.578435587624039))],
    "302A": [("302", (55.6889073960974, 12.57875276712794))],
    "302B": [("302", (55.68890841775245, 12.578854264569232))],
    "302C": [("302", (55.6889073960974, 12.578957574464752))],
    "T7": [("300", (55.6889543922024, 12.577299178772858))],
    "T6": [("300", (55.68899219337628, 12.577957099686728))],
    "T5": [("302", (55.6889901500705, 12.578609583237638))],
    "T4": [("302", (55.6889758469272, 12.579238504882518))],
}

def create_rooms_and_sensors():
    """
    Creates Room documents for each labeled room in ROOM_ADJACENCY,
    and creates Sensor documents for each doorway/opening between rooms.
    """

    # Dictionary to store {room_name: Room_object} after creation
    room_objects = {}

    # 1) Create Room objects in the database
    for room_name in ROOM_ADJACENCY.keys():
        # Example dummy data - adjust as needed
        room = Room(
            name=room_name,
            type="EXHIBITION",      # or LOBBY, OFFICE, etc.
            crowd_factor=0.3,      # dummy crowd factor
            area=50.0,             # dummy area
            longitude=0.0,         # dummy coordinates
            latitude=0.0
        ).save()

        room_objects[room_name] = room

    # 2) Create Sensor objects for each pair of adjacent rooms
    #    We'll keep track of pairs we've already processed to avoid duplicates.
    created_pairs = set()
    for room_name, neighbors in ROOM_ADJACENCY.items():
        for neighbor_name in neighbors:
            # Sort the pair so (201B, 201C) is the same as (201C, 201B)
            pair = tuple(sorted([room_name, neighbor_name]))

            if pair not in created_pairs:
                sensor_name = f"Sensor_{pair[0]}_{pair[1]}"
                sensor = Sensor(
                    name=sensor_name,
                    rooms=[room_objects[pair[0]], room_objects[pair[1]]]
                )
                sensor.save()

                created_pairs.add(pair)

    print("Rooms and sensors created successfully!")

create_rooms_and_sensors()
