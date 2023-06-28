from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://fru1fygudtvf4m501jgt:pscale_pw_eTrbwOGzfihxPHHTIP5K9LAHaW0GlAlifRdnnokm5gr@aws.connect.psdb.cloud/tiu_course_catalogue?charset=utf8mb4"

engine = create_engine(
  db_connection_string, 
  connect_args ={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  } )

with engine.connect() as conn:
  result = conn.execute(text("select + from courses"))
  print(results.all())