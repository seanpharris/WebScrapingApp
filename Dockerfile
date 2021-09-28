FROM node:alpine
COPY . /ORNL_Interview_App
WORKDIR /ORNL_Interview_App
CMD node ORNL_Interview_App.js