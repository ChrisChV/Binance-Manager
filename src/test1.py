import bd
import pg_simple

def test1():
    db = pg_simple.PgSimple(bd.BD.getPool(), nt_cursor=False)

    db = pg_simple.PgSimple(bd.BD.getPool(), nt_cursor=False)
    db = pg_simple.PgSimple(bd.BD.getPool(), nt_cursor=False)
    db = pg_simple.PgSimple(bd.BD.getPool(), nt_cursor=False)

    boy = db.fetchone('test', fields=["id", "nombre"], where=('id=0', None))
    print(boy['nombre'])

    #db.insert('test', {'id': 1, 'nombre': 'Chris1'})
    #db.commit()

    boys = db.fetchall('test')
    print(boys)