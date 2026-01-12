from database.DB_connect import DBConnect
from model.nodes import Prodotti
from model.edges import Edges
class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_years():
        cnx = DBConnect.get_connection()
        if cnx is None:
            raise RuntimeError("Connessione al DB fallita: controlla database/connector.cnf e import di GOsales.sql")

        cursor = cnx.cursor(dictionary=True)

        query = """
                SELECT DISTINCT YEAR(`Date`) as year
                from go_daily_sales gds 
                """
        cursor.execute(query)
        res = [row["year"] for row in cursor.fetchall()]
        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_colors():
        cnx = DBConnect.get_connection()
        if cnx is None:
            raise RuntimeError("Connessione al DB fallita: controlla database/connector.cnf e import di GOsales.sql")

        cursor = cnx.cursor(dictionary=True)

        query = """
                    SELECT DISTINCT Product_color as color
                    from go_products gp 
                    """
        cursor.execute(query)
        res = [row["color"] for row in cursor.fetchall()]
        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def get_nodes(idMap, color):
        cnx = DBConnect.get_connection()
        if cnx is None:
            raise RuntimeError("Connessione al DB fallita: controlla database/connector.cnf e import di GOsales.sql")
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT DISTINCT * 
                    from go_products gp 
                    WHERE Product_color = %s
                    """
        cursor.execute(query, (color,))
        for row in cursor:
            idMap[row["Product_number"]] = Prodotti(**row)
        cursor.close()
        cnx.close()
        return idMap
    @staticmethod
    def getAllEdges(idMap, year, color):
        cnx = DBConnect.get_connection()
        if cnx is None:
            raise RuntimeError("Connessione al DB fallita: controlla database/connector.cnf e import di GOsales.sql")
        cursor = cnx.cursor(dictionary=True)
        result = []
        query = """SELECT DISTINCT t1.p1 as p1, t1.p2 as p2, SUM(t1.n) as n 
                    From (SELECT DISTINCT gds.Product_number as p1, gds2.Product_number as p2, gds.Retailer_code, COUNT(*) as n 
                    FROM go_daily_sales gds , go_daily_sales gds2 , go_products gp , go_products gp2 
                    WHERE gds.`Date` = gds2.`Date` AND YEAR(gds2.`Date`) = %s AND gds2.Retailer_code =  gds.Retailer_code
                    AND gp2.Product_number = gds2.Product_number and gp.Product_number = gds.Product_number 
                    AND gp.Product_color = gp2.Product_color AND gp.Product_color = %s
                    AND gds2.Product_number > gds.Product_number
                    GROUP By gds.Retailer_code, gds.Product_number, gds2.Product_number) t1
                    GROUP BY t1.p1, t1.p2
                    """

        cursor.execute(query, (year, color))

        for row in cursor:
            result.append(Edges(idMap[row['p1']],
                               idMap[row['p2']],
                               row['n']))

        cursor.close()
        cnx.close()
        return result
