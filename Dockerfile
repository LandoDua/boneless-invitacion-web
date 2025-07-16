# Usar Python 3.11 slim como imagen base
FROM python:3.11-slim

# Establecer información del mantenedor
LABEL maintainer="orlando.dua2@gmail.com"
LABEL description="Servidor web para la página de invitacion a Boneless"

# Establecer el directorio de trabajo
WORKDIR /app

# Crear un usuario no privilegiado para mayor seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copiar los archivos de la aplicación
COPY server.py .

# Cambiar el propietario de los archivos
RUN chown -R appuser:appuser /app

# Cambiar al usuario no privilegiado
USER appuser

# Exponer el puerto 3033
EXPOSE 3033

# Comando para ejecutar la aplicación
CMD ["python", "server.py"]
