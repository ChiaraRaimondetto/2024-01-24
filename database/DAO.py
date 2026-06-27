from database.DB_connect import DBConnect
from model.arco import Arco
from model.metodo import Metodo
from model.prodotto import Prodotto


class DAO():
    @staticmethod
    def getMetodi():
        conn=DBConnect.get_connection()

        result=[]

        cursor=conn.cursor(dictionary=True)
        query="""select distinct gm.Order_method_type ,gm.Order_method_code 
                from go_methods gm  """

        cursor.execute(query)
        for row in cursor:
            result.append(Metodo(**row))
        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getAllNodes(anno,metodo):
        conn=DBConnect.get_connection()

        result=[]

        cursor=conn.cursor(dictionary=True)
        query="""
                     
            select distinct gp.*
            from go_products gp ,go_daily_sales gds 
            where gp.Product_number =gds.Product_number and gds.Order_method_code=%s and year(gds.`Date`)=%s 
         """

        cursor.execute(query,(metodo.Order_method_code,anno))
        for row in cursor:
            result.append(Prodotto(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(anno, metodo,idMap,s):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            
            select t1.Product_number as p1 ,t2.Product_number as p2
            from ( 
            select  gp.*, sum(gds.Quantity * gds.Unit_sale_price ) as ricavi
            from go_products gp ,go_daily_sales gds 
            where gp.Product_number =gds.Product_number and gds.Order_method_code=%s and year(gds.`Date`)=%s 
            group by gp.Product_number ) t1,
            ( 
            select  gp.*, sum(gds.Quantity * gds.Unit_sale_price ) as ricavi
            from go_products gp ,go_daily_sales gds 
            where gp.Product_number =gds.Product_number and gds.Order_method_code=%s and year(gds.`Date`)=%s 
            group by gp.Product_number ) t2
            where t2.ricavi>=((1+%s)*t1.ricavi)

             
         """

        cursor.execute(query, (metodo.Order_method_code, anno,metodo.Order_method_code, anno,s))
        for row in cursor:
            result.append(Arco(idMap[row["p1"]],idMap[row["p2"]]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRicavi(anno,metodo,o):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
         select  sum(gds.Quantity * gds.Unit_sale_price ) as ricavi
            from go_products gp ,go_daily_sales gds 
            where gp.Product_number =gds.Product_number and gds.Order_method_code=%s and year(gds.`Date`)=%s and gds.Product_number =%s
            group by gp.Product_number 
         """

        cursor.execute(query,(metodo.Order_method_code,anno,o))
        for row in cursor:
            result.append(float(row["ricavi"]))
        cursor.close()
        conn.close()
        return result

