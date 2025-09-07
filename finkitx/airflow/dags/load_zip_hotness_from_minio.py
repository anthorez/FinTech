def ingest_from_minio_to_postgres():
    import boto3
    import psycopg2
    import pandas as pd
    import io

    s3 = boto3.client(
        's3',
        endpoint_url='http://minio:9000',
        aws_access_key_id='minioadmin',
        aws_secret_access_key='minioadmin',
    )

    # Get the CSV file from MinIO
    obj = s3.get_object(Bucket='datalake', Key='RDC_Inventory_Hotness_Metrics_Zip_History.csv')
    body = io.BytesIO(obj['Body'].read())

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="finkit",
        user="admin",
        password="admin123",
        host="postgres",
        port=5432
    )
    cur = conn.cursor()

    # Create table (if not exists)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS zip_hotness (
            month_date_yyyymm INTEGER,
            postal_code TEXT,
            zip_name TEXT,
            hh_rank FLOAT,
            hotness_rank INTEGER,
            hotness_rank_mm INTEGER,
            hotness_rank_yy FLOAT,
            hotness_score FLOAT,
            supply_score FLOAT,
            demand_score FLOAT,
            median_days_on_market FLOAT,
            median_days_on_market_mm FLOAT,
            median_dom_mm_day FLOAT,
            median_days_on_market_yy FLOAT,
            median_dom_yy_day FLOAT,
            median_dom_vs_us FLOAT,
            page_view_count_per_property_mm FLOAT,
            page_view_count_per_property_yy FLOAT,
            page_view_count_per_property_vs_us FLOAT,
            median_listing_price FLOAT,
            median_listing_price_mm FLOAT,
            median_listing_price_yy FLOAT,
            median_listing_price_vs_us FLOAT,
            quality_flag INTEGER
        );
    """)
    conn.commit()

    # Process CSV in chunks
    chunksize = 5000
    for chunk in pd.read_csv(body, chunksize=chunksize):
        for _, row in chunk.iterrows():
            cur.execute("""
                INSERT INTO zip_hotness VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(row))

    conn.commit()
    cur.close()
    conn.close()