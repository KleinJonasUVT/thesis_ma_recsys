from sqlalchemy import create_engine
from sqlalchemy import text

db_connection_string = "mysql+pymysql://4d4s0sla66rtzfp8i224:pscale_pw_kImC2I0w789a3zQG0z86EM5NiupE9NJv6brWMzssxHs@aws.connect.psdb.cloud/tiu_course_catalogue?charset=utf8mb4"

engine = create_engine(
  db_connection_string,
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
  }
)

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM courses"))
    
    result_dicts = []
    columns = result.keys()
    
    for row in result:
        result_dict = {column: value for column, value in zip(columns, row)}
        result_dicts.append(result_dict)

print(result_dicts)

  
