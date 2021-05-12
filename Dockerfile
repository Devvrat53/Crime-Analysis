FROM python:3.8.5
# Copy all the files in the container
COPY . .
# Setting working directory for the app
WORKDIR /
# Install dependencies
RUN pip3 install -r requirements.txt
# Port number where the container is expose
EXPOSE 8501
# Run the command
ENTRYPOINT [ "streamlit", "run" ]
CMD [ "main.py" ]