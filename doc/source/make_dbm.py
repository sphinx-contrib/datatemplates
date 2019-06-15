import dbm.dumb

with dbm.dumb.open("sampledbm", "c") as db:
    db[b"Hi"] = b"Hello"
    db[b"Bye"] = b"Goodbye"
