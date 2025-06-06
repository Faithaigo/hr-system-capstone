#Use official python runtime image
FROM python:3.12

#Create app directory
RUN mkdir /app

#Set the working directory inside the container
WORKDIR /app

#Set environment variables
#Prevents python from writing pyc files to the disk
ENV PYTHONDONTWRITEBYTECODE=1

#Prevents python from buffering stout and stderr
ENV PYTHONUNBUFFERED=1

#Upgrade pip
RUN pip install --upgrade pip

#Copy the django project and install dependencies
COPY requirements.txt /app/

#Run this commandd to install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy the Django project to the container
COPY . /app/

#Expose the django port
EXPOSE 8000

#Run Django's development server
CMD ["python","manage.py","runserver","0.0.0.0:8000"]