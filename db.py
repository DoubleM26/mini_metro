import sqlite3


class DB:
    def __init__(self):
        self.records = []
        self.con = sqlite3.connect("data/records.db")
        self.cur = self.con.cursor()
        self.get_records()

    def get_records(self):
        result = self.cur.execute("SELECT record FROM records").fetchall()
        self.records = []
        for i in range(4):
            self.records.append(result[i][0])
        # self.moscow_record = result[0][0]
        # self.peter_record = result[1][0]
        # self.novgorod_record = result[2][0]
        # self.samara_record = result[3][0]

    def update_record(self, id, new_record):
        result = self.cur.execute("SELECT record FROM records WHERE id == ?", [id]).fetchall()[0][0]
        if new_record > result:
            self.cur.execute("UPDATE records SET record = ? WHERE id == ?", [new_record, id])
            self.con.commit()

    def close(self):
        self.con.close()
