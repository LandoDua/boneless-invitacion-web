import http.server
import socketserver
import os
import signal
import sys
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
            return
        
        return super().do_GET()
    
    def log_message(self, format, *args):
        # Log personalizado para Docker
        sys.stdout.write(f"[{self.log_date_time_string()}] {format % args}\n")
        sys.stdout.flush()

def create_index_html():
    """Crear el archivo index.html con el contenido de la página"""
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>¿Quieres salir por boneless?</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Arial', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow-x: auto;
        }

        .container {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }

        .question {
            font-size: 2.5em;
            margin-bottom: 40px;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            font-weight: bold;
        }

        .buttons-container {
            display: flex;
            gap: 20px;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
        }

        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px 0 rgba(31, 38, 135, 0.2);
        }

        .btn-si {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            font-size: 1.2em;
            transition: all 0.5s ease;
        }

        .btn-si:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px 0 rgba(238, 90, 36, 0.4);
        }

        .btn-no {
            background: linear-gradient(45deg, #a4b0be, #747d8c);
            color: white;
        }

        .btn-no:hover {
            background: linear-gradient(45deg, #747d8c, #57606f);
            transform: translateY(-2px);
        }

        .result {
            display: none;
            text-align: center;
        }

        .result h1 {
            font-size: 3em;
            color: white;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            animation: bounce 2s infinite;
        }

        .result img {
            max-width: 400px;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(0,0,0,0.3);
        }

        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-10px);
            }
            60% {
                transform: translateY(-5px);
            }
        }

        @media (max-width: 768px) {
            .question {
                font-size: 2em;
            }
            .container {
                padding: 20px;
                margin: 10px;
            }
            .btn {
                padding: 12px 24px;
                font-size: 1em;
            }
            .result h1 {
                font-size: 2em;
            }
            .result img {
                max-width: 300px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="question-section">
            <h1 class="question">¿Quieres salir por boneless?</h1>
            <div class="buttons-container">
                <button id="btn-si" class="btn btn-si">Sí</button>
                <button id="btn-no" class="btn btn-no">No</button>
            </div>
        </div>

        <div id="result-section" class="result">
            <h1>¡Sabía que dirías que sí!</h1>
            <img src="https://media.giphy.com/media/MDJ9IbxxvDUQM/giphy.gif" alt="Gato enamorado">
        </div>
    </div>

    <script>
        const btnSi = document.getElementById('btn-si');
        const btnNo = document.getElementById('btn-no');
        const questionSection = document.getElementById('question-section');
        const resultSection = document.getElementById('result-section');

        const respuestasNo = [
            "¿Estás segura?",
            "¿En serio?",
            "Piénsalo bien... Andale...",
            "¿Qué no tienes hambre?",
            "Andales, di que sí",
            "Los boneless están ricos",
            "De lemmon-peper... Piensalo",
            "¡Porfissss!",
            "¿Y si vamos por una pizza?",
            "De pepperoni",
            "Solo esta vez",
            "¿Prefieres nuggets con papas?",
            "Última oportunidad",
            "¿En serio no quieres?",
            "Está bien, pero piénsalo"
        ];

        let contador = 0;
        let tamaño = 1.2;

        btnNo.addEventListener('click', function() {
            if (contador < respuestasNo.length) {
                btnNo.textContent = respuestasNo[contador];
                tamaño += 0.8;
                btnSi.style.fontSize = tamaño + 'em';
                btnSi.style.padding = (15 + contador * 3) + 'px ' + (30 + contador * 5) + 'px';
                contador++;
            } else {
                
                btnNo.textContent = 'No acepto un NO 8)';
            }
        });

        btnSi.addEventListener('click', function() {
            mostrarResultado();
        });

        function mostrarResultado() {
            questionSection.style.display = 'none';
            resultSection.style.display = 'block';
            document.body.style.background = 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%)';
            startHeartAnimation();
        }

        function createHeart() {
            const heart = document.createElement('div');
            heart.innerHTML = '💖';
            heart.style.position = 'fixed';
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.top = '100vh';
            heart.style.fontSize = '2em';
            heart.style.pointerEvents = 'none';
            heart.style.animation = 'float 3s linear forwards';
            
            document.body.appendChild(heart);
            
            setTimeout(() => {
                heart.remove();
            }, 3000);
        }

        const style = document.createElement('style');
        style.textContent = `
            @keyframes float {
                to {
                    transform: translateY(-100vh) rotate(360deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);

        let heartInterval;
        
        function startHeartAnimation() {
            heartInterval = setInterval(createHeart, 2000);
        }
    </script>
</body>
</html>"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Archivo index.html creado exitosamente")

def signal_handler(sig, frame):
    print('\n🛑 Servidor detenido por señal del sistema')
    sys.exit(0)

def start_server():
    """Iniciar el servidor HTTP"""
    PORT = 3033
    HOST = "0.0.0.0"  # Escuchar en todas las interfaces para Docker
    
    # Registrar manejador de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Crear el archivo HTML si no existe
    if not os.path.exists('index.html'):
        print("📄 Creando archivo index.html...")
        create_index_html()
    
    Handler = CustomHTTPRequestHandler
    
    try:
        with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
            print(f"🚀 Servidor iniciado en {HOST}:{PORT}")
            print(f"📂 Sirviendo archivos desde: {os.getcwd()}")
            print(f"🌐 Disponible en: http://localhost:{PORT}")
            print(f"⚡ Healthcheck: http://localhost:{PORT}/health")
            print("⏹️  Usa Ctrl+C o SIGTERM para detener")
            print("-" * 50)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except OSError as e:
        if e.errno == 98:
            print(f"❌ Error: El puerto {PORT} ya está en uso")
        else:
            print(f"❌ Error al iniciar el servidor: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    print("🎉 Iniciando servidor para página de Boneless")
    print("=" * 50)
    start_server()
