
from flask import Response
import json

def send_response(response_data,status:str,status_code:int):
   if status == 'success' and not type(response_data) == str:
      return Response(json.dumps({"data":response_data,"status":status,"status code":status_code}), content_type='application/json', status=status_code)
   else:
      return Response(json.dumps({"message":response_data,"status":status,"status code":status_code}), content_type='application/json', status=status_code)

def check_url_date_args(argsList):

   start_date = argsList.get('start') #(i.e. ?start=YYYY-MM-DD)
   end_date = argsList.get('end')     #(i.e. &end=YYYY-MM-DD)

   if (start_date is None or end_date is None) or (start_date > end_date):     #(+check if start date is smaller than end date)
      print("Argument not provided")
      return send_response("Arguments not found","error",404)
   return [start_date,end_date]