def webpage(random_value, state):
    html = f"""
       <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pico Web Server</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    display: flex;
                    height: 100vh;
                    justify-content: center;
                    align-items: center;
                    background-color: #f0f2f5;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                    box-sizing: border-box;
                }}
                .container {{
                    background: #fff;
                    border-radius: 20px;
                    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
                    padding: 40px;
                    width: 100%;
                    max-width: 380px;
                    text-align: center;
                }}
                h1, h2 {{
                    color: #2196F3;
                }}
                form {{
                    margin: 20px 0;
                }}
                input[type="submit"] {{
                    background-color: #2196F3;
                    color: #fff;
                    border: none;
                    border-radius: 30px;
                    padding: 15px 25px;
                    width: 100%;
                    font-size: 16px;
                    font-family: inherit;
                    cursor: pointer;
                    transition: background 0.3s ease;
                }}
                input[type="submit"]:hover {{
                    background-color: #1976D2;
                }}
                p {{
                    margin-top: 15px;
                    background-color: #E3F2FD;
                    padding: 12px;
                    border-radius: 12px;
                    border: 1px solid #2196F3;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Raspberry Pi Pico Web Server</h1>
                <h2>LED Control</h2>
                <form action="./lighton">
                    <input type="submit" value="Light On" />
                </form>
                <form action="./lightoff">
                    <input type="submit" value="Light Off" />
                </form>
                <p>LED state: {state}</p>
            </div>
        </body>
        </html>
        """
    return str(html)