from django.db import connections

from datetime import datetime


class Etl:

    def __init__(self) -> None:
        self.cursor = connections['etl'].cursor()
        self.anos = [i for i in range(
            int(datetime.now().year) - 6, int(datetime.now().year) + 1)]

    def secure_input(self, *args):
        proibidos = ['--', ';', '.', 'select', 'delete', 'update',
                     'from', 'insert', 'table', '*', "''", "/*", "'*\'", "'\'"]
        for caracter in proibidos:
            for entrada in args:
                str(entrada).lower()
                if caracter in entrada:
                    return False
        return True

    def pega_dados_por_ano(self, coluna, order_by='', where='', anos=''):
        try:
            if self.secure_input(coluna, order_by, where, anos):
                args = []
                select = f"SELECT p.{coluna}"
                _from = f'FROM graduacoes g'
                join = f'JOIN pessoas p ON g.numero_usp = p.numero_usp'
                group_by = f'GROUP BY p.{coluna}'

                if where:
                    args = [where, ]
                    where = "WHERE g.nome_curso = %s"

                if order_by:
                    order_by = f"ORDER BY {order_by}"

                sum = []
                for ano in anos:
                    sum.append(
                        f", SUM(CASE WHEN ({ano} >= YEAR(data_inicio_vinculo)) AND ({ano} <= YEAR(data_fim_vinculo) OR data_fim_vinculo IS NULL) THEN 1 END) AS '{ano}'")
                sum = "".join(sum)

                query = f"""
                            {  select  }
                            {   sum    }
                            {  _from   }
                            {  join    }
                            {  where   }
                            { group_by }
                            { order_by }
                        """

                self.cursor.execute(query, args)
                return self.cursor.fetchall()
            raise Exception("SQLInjection Detected")
        except Exception as e:
            self.cursor.close()
            raise Exception("Não foi possivel realizar a query:" + e)

    def conta_pessoa_por_categoria(self, tabela, situacao):
        try:
            if self.secure_input(tabela, situacao):
                self.cursor.execute(
                    f"SELECT COUNT(*) FROM {tabela} WHERE situacaoCurso = %s", [situacao])
                return self.cursor.fetchall()
            raise Exception("SQLInjection Detected")
        except Exception as e:
            raise Exception("Não foi possivel realizar a query:" + e)

    def relaciona_dados_em_determinado_ano(self, *args, **kwargs):
        try:
            if self.secure_input(args):
                args = [kwargs.get('data_inicio'), kwargs.get('data_fim')]
                select = f"""
                            SELECT 
                                y.{kwargs.get('column_1')},
                                y.{kwargs.get('column_2')},
                                COUNT(*)
                            FROM {kwargs.get('table_1')} x
                        """
                join = f"JOIN {kwargs.get('table_2')} y ON x.numero_usp = y.numero_usp"
                where = """
                                WHERE 
                                YEAR(x.data_inicio_vinculo) >= %s AND YEAR(x.data_fim_vinculo) <= %s
                                OR YEAR(x.data_fim_vinculo) IS NULL
                            """
                if kwargs.get('departamento'):
                    where = where + "AND x.nome_curso = %s"
                    args.append(kwargs.get('departamento'))

                group_by = f"GROUP BY y.{kwargs.get('column_1')}, y.{kwargs.get('column_2')}"
                order_by = f"ORDER BY y.{kwargs.get('column_1')}"
                
                query = f"""
                            {select}
                            {join}
                            {where}
                            {group_by}
                            {order_by}
                        """

                self.cursor.execute(query, args)
                return self.cursor.fetchall()
            raise Exception("SQLInjection Detected")
        except Exception as e:
            raise Exception("Não foi possivel realizar a query:" + e)
        
    def soma_por_ano(self, anos, coluna, where = ""):
        try:
            if self.secure_input(anos):
                args = []

                sum = []
                for ano in anos:
                    if ano == anos[0]:
                        sum.append(
                            f"SUM(CASE WHEN YEAR({coluna}) = {ano} THEN 1 ELSE 0 END) as total")
                    else:
                        sum.append(
                            f", SUM(CASE WHEN YEAR({coluna}) = {ano} THEN 1 ELSE 0 END) as total")
                sum = "".join(sum)

                if where:
                    args.append(where)
                    where = "WHERE nome_curso = %s"

                query = f"SELECT {sum} FROM graduacoes {where};"
                self.cursor.execute(query, args)
                return self.cursor.fetchall()
            raise Exception("SQLInjection Detected")
        except Exception as e:
            raise Exception("Não foi possivel realizar a query:" + e)
