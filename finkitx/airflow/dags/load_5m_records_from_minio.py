def fetch_and_insert():
    import boto3
    import io
    import pandas as pd
    import psycopg2

    # S3 (MinIO) connection
    s3 = boto3.client('s3',
                      endpoint_url='http://minio:9000',
                      aws_access_key_id='minioadmin',
                      aws_secret_access_key='minioadmin')
    
    obj = s3.get_object(Bucket='datasets', Key='customers_5m.csv')
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    # Connect to Postgres
    conn = psycopg2.connect(
        dbname="finkit",
        user="admin",
        password="admin123",
        host="postgres",
        port=5432
    )
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone_number TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            registration_date DATE
        );
    """)
    conn.commit()

    # Write CSV to memory buffer
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, header=False)
    csv_buffer.seek(0)

    # Copy data from buffer into Postgres
    cur.copy_expert("""
        COPY customers (id, first_name, last_name, email, phone_number, address, city, state, zip_code, registration_date)
        FROM STDIN WITH CSV
    """, csv_buffer)

    conn.commit()
    cur.close()
    conn.close()