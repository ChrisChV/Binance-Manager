import bd
import pg_simple

def test2():
    db = bd.BD.getConn()
    db = bd.BD.getConn()
    db = bd.BD.getConn()
    db = bd.BD.getConn()

    boy = db.fetchone('test', fields=["id", "nombre"], where=('id=0', None))
    print(boy['nombre'])

    #db.insert('test', {'id': 1, 'nombre': 'Chris1'})
    #db.commit()

    boys = db.fetchall('test')
    print(boys)