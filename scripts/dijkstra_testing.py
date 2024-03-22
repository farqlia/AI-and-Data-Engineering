from ai_data_eng.searching.dijkstra import dijkstra

test_cases = [
    {
        "start_stop": "PL. GRUNWALDZKI", "goal_stop": "most Grunwaldzki", "leave_hour": "20:32:00"
    },
    {
        "start_stop": "KLECINA", "goal_stop": "OSIEDLE SOBIESKIEGO", "leave_hour": "20:00:00"
    },
    {
        "start_stop": "Broniewskiego", "goal_stop": "Uniwersytet Ekonomiczny", "leave_hour": "10:15:00"
    },
    {
        "start_stop": "POŚWIĘTNE", "goal_stop": "Młodych Techników", "leave_hour": "15:30:00"
    },
    {
        "start_stop": "Śliczna", "goal_stop": "Marchewkowa", "leave_hour": "23:50:00"
    },
    {
        "start_stop": "PL. GRUNWALDZKI", "goal_stop": "Renoma", "leave_hour": "08:00:00"
    },
    {
        "start_stop": "KOSZAROWA (Szpital)", "goal_stop": "Buforowa-Rondo", "leave_hour": "02:35:00"
    },
    {
        "start_stop": "Wilczyce - Dębowa", "goal_stop": "Marszowicka", "leave_hour": "23:00:00"
    },
    {
        "start_stop": "Zabrodzie - pętla", "goal_stop": "Wiślańska", "leave_hour": "19:52:00"
    },
    {
        "start_stop": "Maślicka (Osiedle)", "goal_stop": "Iwiny - Kolejowa", "leave_hour": "16:07:00"
    },
    {
        "start_stop": "Babimojska", "goal_stop": "Biegasa", "leave_hour": "16:58:00"
    },
    {
        "start_stop": "Małkowice - Główna", "goal_stop": "Kiełczów - Zgodna", "leave_hour": "10:39:00"
    },
    {
        "start_stop": "Brzezia Łąka - Główna", "goal_stop": "Arkady (Capitol)", "leave_hour": "11:15:00"
    },
    {
        "start_stop": "rondo Św. Ojca Pio", "goal_stop": "Sowia", "leave_hour": "17:16:00"
    },
    {
        "start_stop": "Pisarzowice - Graniczna", "goal_stop": "KARŁOWICE", "leave_hour": "05:10:00"
    },
    {
        "start_stop": "Marchewkowa", "goal_stop": "Kominiarska", "leave_hour": "00:08:00"
    },
    {
        "start_stop": "Szymanów (Widawska)", "goal_stop": "Strumykowa", "leave_hour": "00:35:00"
    },
    {
        "start_stop": "Miękinia Cegielnia", "goal_stop": "Rdestowa", "leave_hour": "09:09:00"
    }
]

for test_case in test_cases:
    dijkstra(**test_case)

