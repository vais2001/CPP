import pandas
import io
import pandas as pd

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils import generate_table_html, ListOfDotDicts



class GetAllTablesNames(APIView):

    def get(self, request):
        cursor = request.db_connection.cursor()

        query = """
                SELECT json_agg(row_to_json(row)) AS result FROM (
                                    SELECT * from poc.model_details
                                ) row;
                """
        cursor.execute(query)
        model_details_result = cursor.fetchone()[0]


        query = """SELECT json_agg(row_to_json(row)) AS result
                FROM (
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'poc'
                ) row;"""
        cursor.execute(query)
        result_data = cursor.fetchone()[0]
        column_names = result_data[0].keys()
        print(column_names)
        print("#####")
        print(result_data)
        dot_data = ListOfDotDicts(result_data)
        
        table_thead_html, table_tbody_html = generate_table_html(result_data, 'all_table', None)

        # return render(request, 'table.html', {"columns": column_names, "data": result_data, "model_details": model_details_result, 'thead_html': table_thead_html, 'tbody_html': table_tbody_html})
        return render(request, 'table.html', {"columns": column_names, "data": dot_data, "model_details": model_details_result})


class GetAllDataSpecificTable(APIView):

    def get(self, request, table_name):
        model_id = request.GET.get('model_id')
        print(model_id,111111111111111)
        if not model_id:
            model_id=1

        cursor = request.db_connection.cursor()


        query = f"""SELECT json_agg(row_to_json(row)) AS result
                FROM (
                    SELECT * from poc.{table_name} where model_id={model_id}
                ) row;"""
        
        # print(query)
        cursor.execute(query)
        data = cursor.fetchone()[0]
        toGetColumns=data[0]
        a = pd.DataFrame.from_dict(data)
        a.to_csv("newdata.csv",index=False)
        column_names = list(toGetColumns.keys())
        # for key in toGetColumns.keys:
        #     column_names=column_names.append(key)
        print(column_names,777777777777777777777777777777777)
        # table_thead_html, table_tbody_html = generate_table_html(data, 'table_detail', table_name)
        # print(table_name,"Table Name")
        # print("table_thead_html",table_thead_html)

        # return render(request, 'table_detail.html', {"data": data, 'table_name': table_name, 'thead_html': table_thead_html, 'tbody_html': table_tbody_html})
        return render(request, 'table_detail.html',{"data":data,"colmn_names":column_names,"table_name":table_name})

   


@method_decorator(csrf_exempt, name='dispatch')
class UpdateDataSpecificTableViaUniqueIdentification(APIView):
    def post(self, request):
        update_values = request.data.get('data', '("7", "case 1", "Description 1", "false", "2023-05-31T14:36:15.526+05:30", "null")')
        condition = request.data.get('condition', 'id = 1')
        

        connection = request.db_connection
        cursor = connection.cursor()
        # query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{request.GET.get('table_name', 'pdi_app_case')}';"
        # cursor.execute(query)

        
        set_values = update_values
        sql_query = f"UPDATE poc.{request.data.get('table_name', 'pdi_app_case')} SET {set_values} WHERE {condition};"
        cursor.execute(sql_query)

        connection.commit()
        print("Rows updated successfully!")
        return JsonResponse({"data": "Updated"}, safe=False)

class UpdateDataSpecificTableViaFile(APIView):
    def post(self, request):
        # connection = request.db_connection
        cursor = request.db_connection.cursor()

        query = f"SELECT column_name FROM information_schema.columns where table_name = '{request.GET.get('table_name', 'pdi_app_case')}';"
        cursor.execute(query)
        table_columns = [row[0] for row in cursor.fetchall()]

        excel_data = request.FILES.get('File')

        excel_data = excel_data.read()
        df = pandas.read_csv(io.BytesIO(excel_data))
        dataframe = df.to_json(orient='records')

        value_list = dataframe.values.tolist()
        for value in value_list:
            query

        # for index, row in dataframe.iterrows():
        #     values = {}
        #     for i in zip(list(index),list(row)):
        #         values[i[0]] = i[1]
        #     print(values)

@method_decorator(csrf_exempt, name='dispatch')
class delete_table(APIView):
    def post(self, request):
        table_name = request.POST.get("table_name")
        connection = request.db_connection
        cursor = connection.cursor()
        cursor.execute(f'DELETE FROM "{table_name}";')
        # cursor.close()
        connection.commit()
        return GetAllTablesNames().get(request)
    
@method_decorator(csrf_exempt, name='dispatch')
class DeleteCaseAPI(APIView):
    def post(self, request):
        case_id=request.POST.get("case_id")
        table_name=request.POST.get("table_name")
        print(case_id,8888888888888888888888888888888888888888)
        print(table_name,33333333333333333333)
        connection = request.db_connection
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM poc.{table_name} WHERE id = {case_id}")
        connection.commit()
        return GetAllTablesNames().get(request)
    
@method_decorator(csrf_exempt, name='dispatch')
class update_entry(APIView):
    def post(self, request):
        table_name=request.POST.get("table_name")
        connection = request.db_connection
        cursor = connection.cursor()
        query = f"SELECT column_name FROM information_schema.columns where table_name = '{table_name}';"
        cursor.execute(query)
        table_columns = [row[0] for row in cursor.fetchall()]
        print(table_columns)
        # column_names = [colmn[0] for colmn in cursor.fetchall()]
        # index=column_names.index('id')
        insertion_data=''
        for column in table_columns :
        # index=column_names.index('id')column_names = [colmn[0] for colmn in cursor.fetchall()]
        # index=column_names.index('id')s:
            temp = request.POST.get(f"{column}")
            if column == "id":
                pass
            elif insertion_data:
                insertion_data = insertion_data + ',' + column + '=' + "'" + temp + "'"
            else:
                insertion_data = column + '=' +  "'" + temp + "'"
        cursor.execute(f"UPDATE {table_name} SET {insertion_data} WHERE id = {id};")

        connection.commit()
        return GetAllDataSpecificTable().get(request,table_name)
            
# class CSVUploadView(APIView):
#     def post(self, request):
#         model_id = request.GET.get('model_id')
#         print(model_id, 111111111111111)
#         csv_file = request.FILES.get('csvFile')
#         print(csv_file,1111111111111111111111111111111111111111111)
#         table_name=request.POST.get('table_name')
#         # print(csv_file,18888888888888888888)
#         # print(table_name,333333333333333333333333333333)

#         if not csv_file.name.endswith('.csv'):
#             return Response({'error': 'File must bemodel_details a CSV file'})

#         # data_frame = pd.read_csv('/home/ongraph/Downloads/nba.csv')
#         data_frame = pd.read_csv(csv_file)
#         print(data_frame,"dTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
#         connection = request.db_connection
#         cursor = connection.cursor()
#         cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
#         table_columns = [column[0] for column in cursor.fetchall()]   
#         table_columns.remove('id')     
#         print(table_columns,4444444444444444444444444444444444444444) 
#         columns = [col for col in data_frame.columns if col in table_columns]
#         data_frame = data_frame[columns]
#         print(columns,444444444444444444444444444)

#         for row in data_frame:
#                     row=tuple(row)
#                     insert_query = f"INSERT INTO poc.{table_name} ({', '.join(columns)}) VALUES {row}"
#                     cursor.execute(insert_query)
                        
#                     connection.commit()
#                     # return JsonResponse({"status":"success"})
#         return GetAllDataSpecificTable().get(request,table_name)      


class CSVUploadView(APIView):
    def post(self, request):
        try:
            table_name = request.POST.get("table_name")
            csv_file = request.FILES.get("csvFile")

            if not table_name:
                return Response({"message": "Table name is required"}, status=400)

            if not csv_file:
                return Response({"message": "CSV file is required"}, status=400)

        
            df = pd.read_csv(csv_file)

            with request.db_connection.cursor() as cursor:
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
                table_columns = [column[0] for column in cursor.fetchall()]

                table_columns.remove('id')
                if table_columns:
                    common_columns = []

                    for col_name in df.columns: 
                        if col_name in table_columns:
                            common_columns.append(col_name)
                        else:
                            df.drop([col_name], axis=1, inplace=True)

    
                    if all(col in df.columns for col in table_columns):
                
                        for row in df.itertuples(index=False):
                            print(row,11111111111111111111)
                            non_nan_data = {col_name: col_value for col_name, col_value in zip(df.columns, row) if not pd.isna(col_value)}
                            column_key = list(non_nan_data.keys())
                            column_val = tuple(non_nan_data.values())
                            insert_query = f"INSERT INTO poc.{table_name} ({', '.join(column_key)}) VALUES {column_val}"
                            cursor.execute(insert_query)
                        request.db_connection.commit()
                        return Response({"message": "DataFrame data inserted into the database successfully"})
                    else:
                        return Response({"message": "No common columns found for insertion"}, status=400)

                return Response({"message": "Table columns not found in the database"}, status=400)

        except Exception as e:
            return Response({"message": str(e)}, status=500)    