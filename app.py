from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration
DB_HOST = 'db-zhamshid.clyucs4e44b4.ap-northeast-2.rds.amazonaws.com'
DB_NAME = 'db_zhamshid'  # Should be db_yourname
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_PORT = 5432
TABLE_NAME = 'tbl_zhamshid_clean_jobs' # Table name

def get_db_connection():
    """Create and return a database connection"""
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

@app.route('/schema', methods=['GET'])
def get_schema():
    """Get dataset schema and information"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Get column information
        cur.execute(f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = '{TABLE_NAME}'
            ORDER BY ordinal_position
        """)
        columns = []
        for col in cur.fetchall():
            columns.append({
                'name': col['column_name'],
                'type': col['data_type'],
                'required': col['is_nullable'] == 'NO'
            })

        # Get record count
        cur.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        record_count = cur.fetchone()[0]

        cur.close()
        conn.close()

        return jsonify({
            'table_name': TABLE_NAME,
            'record_count': record_count,
            'columns': columns,
            'description': f"Kaggle dataset imported into {TABLE_NAME}"
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preview', methods=['GET'])
def get_preview():
    """Get a preview of the dataset (first 10 records)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Get first 10 records
        cur.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 10")
        records = cur.fetchall()

        # Convert to list of dictionaries
        result = []
        for record in records:
            result.append(dict(record))

        cur.close()
        conn.close()

        return jsonify({'records': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add', methods=['POST'])
def add_record():
    """Add a new record to the dataset"""
    try:
        data = request.json

        conn = get_db_connection()
        cur = conn.cursor()

        # Extract column names and values
        columns = list(data.keys())
        values = list(data.values())

        # Prepare SQL query for INSERT
        placeholders = ', '.join(['%s'] * len(columns))
        column_names = ', '.join(columns)

        # Execute INSERT query
        cur.execute(
            f"INSERT INTO {TABLE_NAME} ({column_names}) VALUES ({placeholders}) RETURNING id",
            values
        )

        # Get the ID of the newly inserted record
        record_id = cur.fetchone()[0]

        # Commit the transaction
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({'success': True, 'id': record_id})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete a record from the dataset by ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Execute DELETE query
        cur.execute(f"DELETE FROM {TABLE_NAME} WHERE id = %s", (record_id,))

        # Check if any row was affected
        if cur.rowcount == 0:
            cur.close()
            conn.close()
            return jsonify({'error': f"Record with ID {record_id} not found"}), 404

        # Commit the transaction
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
