from flask import Flask, render_template, jsonify
import sqlite3
from command_data import commands_by_category  # Import your category dictionary

app = Flask(__name__, template_folder='templates', static_folder='static')

def get_commands_from_db():
    conn = sqlite3.connect('commands.db')
    cursor = conn.cursor()
    all_commands = []

    try:
        for table_name in commands_by_category.keys():  # Only query tables in your dictionary
            display_name = table_name.replace('_', ' ').title()  # Create display name
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            for row in rows:
                command_data = {
                    'command': row[1],
                    'description': row[2],
                    'syntax': row[3],
                    'example': row[4],
                    'category': display_name
                }
                all_commands.append(command_data)
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()
    
    return all_commands

@app.route('/')
def index():
    commands = get_commands_from_db()
    
    # Organize commands by category
    commands_by_display_category = {}
    for category_key, category_table in commands_by_category.items():
        display_name = category_key.replace('_', ' ').title()
        filtered_commands = [cmd for cmd in commands if cmd['category'] == display_name]  # Fixed line
        commands_by_display_category[display_name] = filtered_commands

    print("Categories to Render:", commands_by_display_category)  # Debugging line
    return render_template('index.html', categories=commands_by_display_category)

@app.route('/api/commands')
def api_commands():
    return jsonify(get_commands_from_db())


if __name__ == '__main__':
    app.run(debug=True)
